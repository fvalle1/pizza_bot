# pizza_bot

Bot per avere le dosi per una perfetta pizza o focaccia!

Use this bot and cook the perfect pizza..!

# Run
First create a bot and insert the key in the code
```julia
url = "https://api.telegram.org/"
key={YOUR_KEY_HERE}
```

It can be run with two different *backends*

## Postgres
Clone this repo and run with docker
```bash
git clone https://github.com/fvalle1/pizza_bot.git
cd pizza_bot
docker-compose up -d
```

## with a dictionary as backend
```bash
git clone https://github.com/fvalle1/pizza_bot.git
cd pizza_bot
```

Edit *pizza_bot.jl* and comment the right backend
```julia
include("white_backend.jl")
#include("psql_backend.jl")
```
then simply run Julia

```bash
julia pizza_bot.jl
```

#License
See [LICENSE](LICENSE)
