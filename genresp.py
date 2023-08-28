from hashlib import md5
from json import dumps
from os import environ
from sys import argv

content = None
with open("static/ota_payload.bin", "rb") as f:
	content = f.read()

print(dumps({
	"md5": md5(content).hexdigest(),
	"url": "https://github.com/scratchminer/pd-ota/releases/download/{argv[1]}/ota_payload.bin",
 	"version": argv[1],
	"notes": "",
	"decryption_key": None
}))
