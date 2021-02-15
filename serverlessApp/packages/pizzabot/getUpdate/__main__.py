import json
from pizza_bot import parse_message

def main(params):
	parse_message(params)
	return {"message": json.dumps(params),
		"status": 400}
