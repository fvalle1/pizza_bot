from pizza_bot import parse_message
import json

def main(params):
	parse_message(params)
	return {"body": ["OK", params],
		"headers":{"Content-Type":"application/json"}
		}
