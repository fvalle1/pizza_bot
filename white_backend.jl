module Backend

export contacts, chats, update_contact_list, get_key, set_key, get_state, set_state

contacts = Dict()
chats = Dict()

function update_contact_list(message)
    id = message["message"]["from"]["id"]
    if !(id in  keys(contacts))
        contacts[id] = Dict("state"=> 0, "message"=>message)
    end
end

function get_key(id, key)
    return contacts[id][key]
end

function set_key(id, key, value)
    contacts[id][key] = value
end

function get_state(id)
    return get_key(id,"state")
end

function set_state(id, state)
    set_key(id,"state", state)
end

end
