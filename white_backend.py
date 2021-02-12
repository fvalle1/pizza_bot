import logging
log = logging.getLogger("pizza_bot")

contacts = {}
chats = {}

def update_contact_list(message):
    id = message["message"]["from"]["id"]
    if id not in  contacts.keys():
        contacts[id] = {"state": 0, "message":message}
    
def get_key(id, key):
    return contacts[id][key]

def set_key(id, key, value):
    contacts[id][key] = value

def get_state(id):
    return get_key(id,"state")

def set_state(id, state):
    set_key(id,"state", state)



