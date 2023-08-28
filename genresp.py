
from hashlib import md5
from json import dumps

content = None
with open("static/ota_payload.bin", "rb") as f:
	content = f.read()

print(dumps({
	"md5": md5(content).hexdigest(),
	"url": "https://scratchminer.github.io/pd-ota/ota_payload.bin",
 	"version": env["VERSION"],
	"notes": "",
	"decryption_key": None
}))
