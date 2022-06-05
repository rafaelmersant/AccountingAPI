#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accounting.settings")

import django
django.setup()

from administration.models import Person, Church

def add_new_person(name, church_id):
    name = name.strip()

    person = Person()
    person.first_name = name
    person.last_name = " "
    person.church = Church.objects.get(id=church_id)
    person.save()
    print("*** obrero: ", name, ' -> added!')
    
# Main Process        
with open('nuevosObreros.csv', newline='') as csvfile:
    obreros = csv.reader(csvfile, delimiter=',', quotechar='|')
    for index, row in enumerate(obreros):
        add_new_person(row[0], row[1])