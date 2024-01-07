from json import dumps
from sys import argv

md5 = None
with open("static/ota_payload/md5.txt", "r") as f:
	md5 = f.read(32)

print(dumps({
	"stock_md5": md5,
	"dvt1": f"https://github.com/scratchminer/pd-ota/releases/download/{argv[1]}/Playdate-dvt1.pdfw",
	"h7d1": f"https://github.com/scratchminer/pd-ota/releases/download/{argv[1]}/Playdate-h7d1.pdfw",
 	"version": argv[1],
	"notes": "",
	"decryption_key": None
}))
