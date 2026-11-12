from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError
from administration.models import User
from .models import Entry, Item, EntryHistory

ENTRY_FIELDS = {
    'church': 'Iglesia', 'person': 'Obrero', 'note': 'Nota',
    'period_year': 'Año', 'period_month': 'Mes', 'total_amount': 'Total',
    'created_by': 'Creado por',
}
ITEM_FIELDS = {
    'concept': 'Concepto', 'amount': 'Monto', 'reference': 'Referencia',
    'period_year': 'Año', 'period_month': 'Mes', 'type': 'Tipo', 'method': 'Método',
}


def snapshot(instance):
    fields = ENTRY_FIELDS if isinstance(instance, Entry) else ITEM_FIELDS
    result = {}
    for field in fields:
        value = getattr(instance, field)
        if field in ('church', 'person', 'concept', 'created_by'):
            if value is None:
                value = None
            else:
                label = {'church': 'global_title', 'person': 'full_name',
                         'concept': 'description', 'created_by': 'name'}[field]
                value = {'id': value.pk, 'name': getattr(value, label)}
        elif isinstance(value, Decimal):
            value = format(value, '.2f')
        elif field == 'reference':
            value = value or ''
        result[field] = value
    return result


def record(instance, before, after, actor, action):
    fields = ENTRY_FIELDS if isinstance(instance, Entry) else ITEM_FIELDS
    changes = [{'field': field, 'label': label, 'old': before.get(field),
                'new': after.get(field)} for field, label in fields.items()
               if before.get(field) != after.get(field)]
    if not changes and action == 'updated':
        return
    concept = (after.get('concept') or before.get('concept') or {}).get('name', '')
    EntryHistory.objects.create(
        entry_id=instance.pk if isinstance(instance, Entry) else instance.entry_id,
        item_id=instance.pk if isinstance(instance, Item) else None,
        action=action, concept=concept, actor_id=actor.pk if actor else None,
        actor_name=actor.name if actor else 'Usuario no identificado (cliente anterior)',
        changes=changes,
    )


class EntryAuditMixin:
    def audit_actor(self):
        # The legacy login does not issue a server session/token. Never confuse
        # the record creator with the user currently editing the record.
        user_id = self.request.headers.get('X-Entry-User')
        if not user_id:
            return None
        try:
            return User.objects.get(pk=int(user_id))
        except (ValueError, User.DoesNotExist):
            raise ValidationError({'user': 'Usuario de modificación inválido.'})

    @transaction.atomic
    def perform_update(self, serializer):
        actor = self.audit_actor()
        instance = type(serializer.instance).objects.select_for_update().get(pk=serializer.instance.pk)
        before = snapshot(instance)
        serializer.instance = instance
        saved = serializer.save()
        record(saved, before, snapshot(saved), actor, 'updated')

    @transaction.atomic
    def perform_create(self, serializer):
        actor = self.audit_actor()
        instance = serializer.save()
        if isinstance(instance, Item):
            record(instance, {}, snapshot(instance), actor, 'added')

    @transaction.atomic
    def perform_destroy(self, instance):
        actor = self.audit_actor()
        instance = type(instance).objects.select_for_update().get(pk=instance.pk)
        record(instance, snapshot(instance), {}, actor, 'deleted')
        instance.delete()
