from unittest.mock import patch
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from administration.models import User, Church, Person, Concept
from .models import Entry, Item, EntryHistory


class EntryHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='editor', name='Usuario editor', created_by='test')
        self.creator = User.objects.create(username='creator', name='Creador', created_by='test')
        self.church = Church.objects.create(global_title='Iglesia anterior')
        self.new_church = Church.objects.create(global_title='Iglesia nueva')
        self.person = Person.objects.create(first_name='Ana', last_name='Perez')
        self.concept = Concept.objects.create(description='20% al Concilio')
        self.entry = Entry.objects.create(church=self.church, period_year=2026, period_month=11,
                                          total_amount=100, created_by=self.creator)
        self.item = Item.objects.create(entry=self.entry, concept=self.concept, amount=100,
                                       period_year=2026, period_month=11)
        self.client = APIClient()
        self.client.credentials(HTTP_X_ENTRY_USER=str(self.user.pk))

    def header_url(self):
        return f'/api/v1/entries/{self.entry.pk}/'

    def item_url(self):
        return f'/api/v1/entries/{self.entry.pk}/items/{self.item.pk}/'

    def test_header_changes_null_clear_and_noop(self):
        response = self.client.patch(self.header_url(), {'church_id': self.new_church.pk,
                                     'person_id': self.person.pk, 'note': 'Nueva nota'}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        event = EntryHistory.objects.get()
        changes = {c['field']: c for c in event.changes}
        self.assertEqual(changes['church']['old']['name'], 'Iglesia anterior')
        self.assertEqual(changes['church']['new']['name'], 'Iglesia nueva')
        self.assertEqual(event.actor_id, self.user.pk)
        self.assertEqual(event.actor_name, 'Usuario editor')
        self.assertIsNotNone(event.changed_at)
        self.client.patch(self.header_url(), {'note': 'Nueva nota'}, format='json')
        self.assertEqual(EntryHistory.objects.count(), 1)
        response = self.client.patch(self.header_url(), {'church_id': None, 'person_id': None}, format='json')
        self.assertEqual(response.status_code, 200)
        self.entry.refresh_from_db()
        self.assertIsNone(self.entry.church_id)
        self.assertIsNone(self.entry.person_id)
        self.assertEqual(self.entry.created_by_id, self.creator.pk)

    def test_detail_changes_add_delete_and_history_isolation(self):
        response = self.client.patch(self.item_url(), {'amount': '125.50', 'method': 'D',
                                     'reference': 'Banco', 'period_month': 12}, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        changes = {c['field']: c for c in EntryHistory.objects.get().changes}
        self.assertEqual(changes['amount']['old'], '100.00')
        self.assertEqual(changes['amount']['new'], '125.50')
        self.assertEqual(changes['method']['new'], 'D')
        self.client.patch(self.item_url(), {'amount': '125.5'}, format='json')
        self.assertEqual(EntryHistory.objects.count(), 1)
        response = self.client.post(f'/api/v1/entries/{self.entry.pk}/items/', {
            'concept_id': self.concept.pk, 'amount': '50', 'period_year': 2026, 'period_month': 11,
            'method': 'C'}, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(EntryHistory.objects.filter(action='added').exists())
        self.assertEqual(self.client.delete(self.item_url()).status_code, 204)
        self.assertTrue(EntryHistory.objects.filter(action='deleted', concept='20% al Concilio').exists())
        EntryHistory.objects.create(entry_id=99999, action='updated', actor_name='Otro', changes=[])
        response = self.client.get(self.header_url() + 'history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['action'], 'deleted')
        self.assertTrue(self.client.get(self.header_url()).data['has_history'])
        self.assertEqual(self.client.post(self.header_url() + 'history/', {}, format='json').status_code, 405)

    def test_no_history_before_change_and_invalid_user(self):
        self.assertFalse(self.client.get(self.header_url()).data['has_history'])
        self.client.credentials(HTTP_X_ENTRY_USER='invalid')
        self.assertEqual(self.client.patch(self.item_url(), {'amount': '150'}, format='json').status_code, 400)
        self.item.refresh_from_db()
        self.assertEqual(self.item.amount, Decimal('100'))
        self.assertEqual(EntryHistory.objects.count(), 0)

    def test_audit_failure_rolls_back_modification(self):
        with patch('entries.audit.record', side_effect=RuntimeError('audit unavailable')):
            with self.assertRaises(RuntimeError):
                self.client.patch(self.item_url(), {'amount': '200'}, format='json')
        self.item.refresh_from_db()
        self.assertEqual(self.item.amount, Decimal('100'))

    def test_browser_put_preserves_creator_and_unchanged_details(self):
        response = self.client.put(self.header_url(), {
            'church_id': self.church.pk, 'person_id': None, 'note': '',
            'period_year': 2026, 'period_month': 11, 'total_amount': '100.00',
        }, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        response = self.client.put(self.item_url(), {
            'concept_id': self.concept.pk, 'amount': '100.00', 'reference': '',
            'type': 'E', 'method': 'E', 'period_year': 2026, 'period_month': 11,
        }, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(EntryHistory.objects.count(), 0)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.created_by_id, self.creator.pk)

    def test_deleted_entry_keeps_audit(self):
        self.assertEqual(self.client.delete(self.header_url()).status_code, 204)
        self.assertTrue(EntryHistory.objects.filter(entry_id=self.entry.pk, action='deleted').exists())
