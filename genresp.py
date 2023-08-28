
from hashlib import md5
from json import dumps
from os import env
from sys import argv

content = None
with open("static/ota_payload.bin", "rb") as f:
	content = f.read()

print(dumps({
	"md5": md5(content).hexdigest(),
	"url": "https://scratchminer.github.io/pd-ota/static/ota_payload.bin",
 	"version": env["VERSION"],
	"notes": "",
	"decryption_key": None
}))
