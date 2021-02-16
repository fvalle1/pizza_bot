import json
import requests
import os, sys
import math
import time
import logging
log = logging.getLogger("pizza_bot")
hdl = logging.StreamHandler()
log.addHandler(hdl)
log.setLevel(logging.DEBUG)

from nimbella_backend import *

url = "https://api.telegram.org/"
key = os.environ["TELEGRAM_KEY"]

def send_message(params):
    req = requests.post(url+key+"/sendMessage", data = params)
    log.debug(req.json())
    log.debug(params)

def send_welcome(contact):
    id = contact["id"]
    name = contact["first_name"]
    if "language_code" in contact.keys():
        lc = contact["language_code"]
    else:
        lc = "it"

    if lc=="it":
        params = {"chat_id":id, "text":"Ciao "+name+"""! Sono Pizzabot\n
        Ti aiuterò a preparare pizze e focacce favolose!
        Digita /cuciniamo per iniziare e poi segui le istruzioni.

        Buon lavoro e buon appetito!!"""}
    else:
        params = {"chat_id":id, "text":"Welcome "+name+" \nClick /cuciniamo to begin.."}
    send_message(params)

def ask_program(contact):
    id = contact["id"]
    buttons = [[{"text":"pizza"}, {"text":"focaccia"}]]
    reply_markup = {"keyboard":buttons, "one_time_keyboard":True}
    params = {"chat_id":id, "text":"Cosa vuoi cucinare? (pizza o focaccia)", "reply_markup":json.dumps(reply_markup)}
    send_message(params)

def ask_people(message):
    id = message["from"]["id"]
    program = message["text"]

    if program not in ["pizza", "focaccia"]:
        program = "pizza"

    params = {"chat_id":id, "text":"Bene allora ti darò istruzioni per fare la "+program}
    send_message(params)
    params = {"chat_id":id, "text":"per quante persone vuoi fare la "+program+"?"}
    send_message(params)
    return program


def read_people(message, state):
    id = message["from"]["id"]
    people = message["text"]
    program = get_key(id, "program")
    try:
        people = int(people)
        if people <= 0:
            raise ValueError("too few people")
        send_recipe(message, people)
        return state + 1
    except:
        log.debug(*sys.exc_info())
        params = {"chat_id":id, "text":"Non ho capito. Per quante persone?"}
        send_message(params)
        return state
   
def send_recipe(message, people):
    id = message["from"]["id"]
    program = get_key(id, "program")
    log.debug("\n\n\n\nPROGRAM"+program)
    if "pizza" in program:
        send_pizza(id, people)
    elif "focaccia" in program:
        send_focaccia(id, people)
    
def send_pizza(id, people):
    pizza_recipe = [1000, 100, 500]
    recipe = [el / 4. * people for el in pizza_recipe]
    params = {"chat_id":id, "text":f"""Ecco le dosi per {people} persone:\n
    {recipe[0]/1000} Kg di farina\n
    {recipe[1]} ml di olio\n
    {recipe[2]} ml di acqua\n
    lievito q.b.\n
    sale q.b.\n"""}
    send_message(params)

def send_focaccia(id, people):
    focaccia_recipe = [660, 50, 440]
    recipe = [el / 4. * people for el in focaccia_recipe]
    number, rectangular_str, circular_str, rectangular, circular = get_teglia(sum(recipe))

    params = {"chat_id":id, "text":f"""Ecco le dosi per {people} persone:\n
    {recipe[0]/1000} Kg di farina di Manitoba (W=280)\n
    {recipe[1]} g di olio\n
    {recipe[2]} ml di acqua\n
    lievito q.b.\n
    sale q.b.\n\n
    Puoi usare {circular_str} di diametro: {circular}cm\n
    oppure {rectangular_str} {rectangular[0]} cm X {rectangular[1]} cm"""}
    send_message(params)

def get_teglia(impasto):
    area = impasto / 0.60
    rapp = 42 / 35
    area_max = 42 * 35
    number = int(round(math.floor(area/area_max) + 1))

    area = area / number # area singola teglia

    h = round(math.sqrt(area / rapp))
    b = round(area / h)
    rectangular = [b, h]
    circular = round(math.sqrt(area/math.pi)*2,1)

    if number > 1:
        rectangular_str = f"{number} teglie rettangolari"
        circular_str = f"{number} teglie circolari"
    else:
        rectangular_str = "una teglia rettangolare"
        circular_str = "una teglia circolare"

    return (number, rectangular_str, circular_str, rectangular, circular)

def send_bye(contact):
    id = contact["id"]
    name = contact["first_name"]
    if "language_code" in contact.keys():
        lc = contact["language_code"]
    else:
        lc = "it"
    
    if lc=="it":
        params = {"chat_id":id, "text":"Buon appetito "+name+"!"}
    else:
        params = {"chat_id":id, "text":"Enjoy your meal "+name+"!"}
    
    send_message(params)


def parse_message(message):
    id = message["message"]["from"]["id"]
    update_contact_list(message)
    state = get_state(id)

    if (state == 0) | (message["message"]["text"]=="/start"):
        send_welcome(message["message"]["from"])
        set_state(id, 1)
    elif (state == 1) | (message["message"]["text"]=="/cuciniamo"):
        ask_program(message["message"]["from"])
        set_state(id, 2)
    elif state == 2:
        program = ask_people(message["message"])
        set_state(id, 3)
        set_key(id,"program",program)
    elif state == 3:
        new_state = read_people(message["message"], 3)
        state = new_state
        set_state(id, state)

    if state == 4:
        send_bye(message["message"]["from"])
        set_state(id, 1)
   
def run():
    offset = -1

    log.info("ready!")
    while True:
    #for i in 1:100
        if offset >= 0:
            params = {"offset":offset}
        else:
            params = {}
        
        log.debug(params)

        req = requests.get(url+key+"/getUpdates", params = params)
        result = req.json()
        log.debug(result)
        if len(result["result"]) < 1:
            continue

        offset = int(result["result"][len(result["result"])-1]["update_id"]) + 1
        log.debug(f"offset {offset}")
        log.debug(result["result"])
        log.debug(len(result["result"]))
        for message in result["result"]:
           parse_message(message)
        
        time.sleep(.5)


if __name__ == "__main__":
	run()
