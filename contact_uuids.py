import json
from uuid import uuid1

with open('contacts.json', 'r') as f:
    contacts = json.load(f)

for contact in contacts:
    uuid = str(uuid1())
    contact.update({'uuid': uuid})

with open('contacts.json', 'w+') as f:
    json.dump(contacts, f)
