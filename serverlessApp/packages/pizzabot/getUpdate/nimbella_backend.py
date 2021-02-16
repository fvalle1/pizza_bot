import logging
log = logging.getLogger("pizza_bot")
import json
import nimbella
client = nimbella.redis()

def update_contact_list(message):
    id = message["message"]["from"]["id"]
    if client.get(id) is None:
        client.set(id,json.dumps({"state": 0, "message":message}))

def get_key(id, key):
    log.debug(client.get(id))
    log.debug(json.loads(client.get(id)))
    return json.loads(client.get(id))[key]

def set_key(id, key, value):
    user = json.loads(client.get(id))
    user[key]=value
    client.set(id, json.dumps(user))

def get_state(id):
    return get_key(id,"state")

def set_state(id, state):
    set_key(id,"state", state)



