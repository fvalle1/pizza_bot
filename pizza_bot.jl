using Printf
using HTTP
using JSON

#include("white_backend.jl")
include("psql_backend.jl")
using Main.Backend

url = "https://api.telegram.org/"
key={YOUR_KEY_HERE}

function send_message(params)
    req = HTTP.request("POST",string(url,key,"/sendMessage"),["Content-Type" => "application/json"],JSON.json(params))
end

function send_welcome(contact)
    id = contact["id"]
    name = contact["first_name"]
    if "language_code" in keys(contact)
        lc = contact["language_code"]
    else
        lc = "it"
    end
    if lc=="it"
        params = Dict("chat_id"=>id, "text"=>string("Benvenuto ", name, "! \nQuando sei pronto clicca /pizza!"))
    else
        params = Dict("chat_id"=>id, "text"=>string("Welcome ", name, " \nClick /pizza to begin.."))
    end
    send_message(params)
end

function ask_program(contact)
    id = contact["id"]
    buttons = [Dict("text"=>"pizza"), Dict("text"=>"focaccia")]
    reply_markup = Dict("keyboard"=>[buttons], "one_time_keyboard"=>true)
    params = Dict("chat_id"=>id, "text"=>"Cosa vuoi fare?", "reply_markup"=>reply_markup)
    send_message(params)
end

function ask_people(message)
    id = message["from"]["id"]
    program = message["text"]
    params = Dict("chat_id"=>id, "text"=>string("Bene allora ti darò istruzioni per fare la ", program))
    send_message(params)
    params = Dict("chat_id"=>id, "text"=>string("per quante persone vuoi fare la ", program, "?"))
    send_message(params)
    return program
end

function read_people(message, state)
    id = message["from"]["id"]
    people = message["text"]
    program = get_key(id, "program")
    try
        people = parse(Int, people)
        send_recipe(message, people)
        return state + 1
    catch
        params = Dict("chat_id"=>id, "text"=>string("Non ho capito. Per quante persone?"))
        send_message(params)
        return state
    end
end

function send_recipe(message, people)
    id = message["from"]["id"]
    program = get_key(id, "program")
    if program == "pizza"
        send_pizza(id, people)
    elseif program == "focaccia"
        send_focaccia(id, people)
    end
end

function send_pizza(id, people)
    pizza_recipe = [1 100 500]
    recipe = pizza_recipe / 4. * people
    params = Dict("chat_id"=>id, "text"=>string("Ecco la ricetta per $(people) persone:\n
    $(@sprintf("%.1f", recipe[1])) Kg di farina\n
    $(@sprintf("%.1f", recipe[2])) ml di olio\n
    $(@sprintf("%.1f", recipe[3])) ml di acqua\n
    lievito q.b\n
    sale q.b.\n"))
    send_message(params)
end

function send_focaccia(id, people)
    focaccia_recipe = [0.660 50 440]
    recipe = focaccia_recipe / 4. * people

    rectangular, circular = get_teglia(sum(recipe))

    params = Dict("chat_id"=>id, "text"=>string("Ecco la ricetta per $(people) persone:\n
    $(@sprintf("%.1f", recipe[1])) Kg di farina di Manitoba (W=280)\n
    $(@sprintf("%.1f", recipe[2])) g di olio\n
    $(@sprintf("%.1f", recipe[3])) ml di acqua\n
    lievito q.b\n
    sale q.b.\n\n
    Puoi usare una teglia circolare di diametro: $(@sprintf("%.1f", circular))cm\n
    oppure una teglia rettangolare $(@sprintf("%.1f", rectangular[1])) cm X $(@sprintf("%.1f", rectangular[2])) cm"))
    send_message(params)
end

function get_teglia(impasto)
    area = impasto / 0.60
    rapp = 35 / 28
    h = sqrt(area / rapp)
    b = area / h
    rectangular = [b h]
    circular = sqrt(area/pi)*2

    return (rectangular, circular)
end

function send_bye(contact)
    id = contact["id"]
    name = contact["first_name"]
    if "language_code" in keys(contact)
        lc = contact["language_code"]
    else
        lc = "it"
    end
    if lc=="it"
        params = Dict("chat_id"=>id, "text"=>string("Buon appetito ", name, "!"))
    else
        params = Dict("chat_id"=>id, "text"=>string("Enjoy your meal ", name, "!"))
    end
    send_message(params)
end

function parse_message(message)
    id = message["message"]["from"]["id"]
    update_contact_list(message)
    state = get_state(id)

    if (state == 0) | (message["message"]["text"]=="/start")
        send_welcome(message["message"]["from"])
        set_state(id, 1)
    elseif (state == 1) | (message["message"]["text"]=="/pizza")
        ask_program(message["message"]["from"])
        set_state(id, 2)
    elseif state == 2
        program = ask_people(message["message"])
        set_state(id, 3)
        set_key(id,"program",program)
    elseif state == 3
        new_state = read_people(message["message"], 3)
        state = new_state
        set_state(id, state)
    end

    if state == 4
        send_bye(message["message"]["from"])
        set_state(id, 1)
    end
end

function run()
    offset = -1

    println("ready!")
    while true
    #for i in 1:100
        if offset >= 0
            params = Dict("offset"=>offset)
        else
            params = Dict()
        end
        req = HTTP.request("GET", string(url,key,"/getUpdates"), ["Content-Type" => "application/json"],JSON.json(params))
        body = String(req.body)
        result = JSON.Parser.parse(body)

        if length(result["result"]) < 1
            continue
        end
        offset = result["result"][end]["update_id"] + 1
        for message in result["result"]
           parse_message(message)
        end
        sleep(0.1)
    end
end


init_db()
conn = get_conn()

run()

@sync close(conn)
