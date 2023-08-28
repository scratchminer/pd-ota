from json import dumps
from os import env
from sys import argv

print(dumps({
  "md5": argv[1],
  "url": "https://scratchminer.github.io/pd-ota/static/ota_payload.bin",
  "version": env["VERSION"],
  "notes": "",
  "decryption_key": None
}))
