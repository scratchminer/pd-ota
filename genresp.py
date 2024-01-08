from hashlib import md5
from json import dumps
from sys import argv

md5 = None
md5_a = None
md5_b = None

with open("static/ota_payload/md5.txt", "r") as f:
	md5 = f.read(32)

content_a = None
content_b = None
with open("static/Playdate-dvt1.pdfw", "rb") as f:
	content_a = f.read()
with open("static/Playdate-h7d1.pdfw", "rb") as f:
	content_b = f.read()

print(dumps({
	"stock_md5": md5,
	"dvt1_md5": md5(content_a).hexdigest(),
	"h7d1_md5": md5(content_b).hexdigest(),
	"dvt1": f"https://github.com/scratchminer/pd-ota/releases/download/{argv[1]}/Playdate-dvt1.pdfw",
	"h7d1": f"https://github.com/scratchminer/pd-ota/releases/download/{argv[1]}/Playdate-h7d1.pdfw",
 	"version": argv[1],
	"notes": "",
	"decryption_key": None
}))
