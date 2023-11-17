# pip install cryptography
# pip install requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from requests import get

from argparse import ArgumentParser
from base64 import b64decode
from hashlib import md5
from os import mkdir
from os.path import join
from re import search, escape, DOTALL
from shutil import rmtree
from sys import argv, exit
from zipfile import ZipFile

FIRMWARE_API = "https://play.date/api/v2/firmware/?current_version=2.1.0"

def quit():
	try: rmtree(".pdpatcher", ignore_errors=True)
	except FileNotFoundError: pass
	exit()

if __name__ == "__main__":
	parser = ArgumentParser(prog="PDPatcher", description="A Playdate firmware patcher by scratchminer")
	parser.add_argument("-t", help="access token for a registered device", dest="token", required=True)
	parser.add_argument("-p", help="unlock key, sometimes called the password, for a registered device", dest="pw", metavar="PASSWORD", required=True)
	parser.add_argument("--no-patch", "-n", action="store_const", const=True, default=False, help="don't patch the firmware at all, just dump it", dest="no_patch")
	parser.add_argument("-o", default="ota_payload", help="output directory", dest="out_dir")
	args = parser.parse_args()
	
	try: mkdir(".pdpatcher")
	except FileExistsError: pass
	
	try: mkdir(args.out_dir)
	except FileExistsError: pass
	
	print("Requesting firmware from Panic servers...")
	r = get(FIRMWARE_API, headers={
		"Authorization": f"Token {args.token}"
	})
	
	if r.status_code != 200:
		print("There was an error obtaining the firmware download link. Full response below:")
		print(r.text)
		quit()
	
	j = r.json()
	
	url = j["url"]
	print(f"Downloading {j['version']}...")
	s = get(url, stream=True)
	
	with open(f".pdpatcher/ota_payload.bin", "wb") as f:
		for part in s.iter_content(512):
			f.write(part)
	
	print(f"Decrypting key for {j['version']}...")
	base64_data = b64decode(j["decryption_key"])
	
	iv = base64_data[:12]
	data = base64_data[12:]
	
	key_aes = AESGCM(bytes(args.pw, "utf-8"))
	try: key = key_aes.decrypt(iv, data, None)
	except:
		print("The password and access token provided do not match. Please ensure your data is correct.")
		quit()
	
	print(f"Extracting {j['version']}...")
	with ZipFile(f".pdpatcher/ota_payload.bin", "r") as bundle:
		pdx_name = bundle.namelist()[0].split("/", 1)[0]
		bundle.extractall(path=".pdpatcher")
		bundle.extractall(path=args.out_dir)
	
	print(f"Decrypting {j['version']}...")

	decrypted_file = None
	with open(f".pdpatcher/boot", "rb") as boot:
		boot.read(4)
		aes = AESGCM(key)
		decrypted_file = aes.decrypt(boot.read(12), boot.read(), None)
	with open(join(args.out_dir, "boot"), "wb") as boot:
		boot.write(decrypted_file)
	
	dec_header = None
	decrypted = None
	with open(f".pdpatcher/pdfw", "rb") as pdfw:
		pdfw.read(4)
		aes = AESGCM(key)
		decrypted_file = aes.decrypt(pdfw.read(12), pdfw.read(), None)
		decrypted = decrypted_file[32:]
		dec_header = decrypted_file[:32]
	with open(join(args.out_dir, "pdfw"), "wb") as pdfw:
		if not args.no_patch:
			print(f"Patching {j['version']}...")
			# change the function telling whether Lua has system privilege
			decrypted = decrypted.replace(
				b"\x02\x4b\x18\x78\x00\xf0\x01\x00\x70\x47",
				b"\x02\x4b\x18\x78\x40\xf0\x01\x00\x70\x47"
			)
			# change the function telling whether C has system privilege
			decrypted = decrypted.replace(
				b"\xef\xf3\x05\x80\x00\x28\x1c\xbf\x01\x20\x70\x47\xef\xf3\x14\x80\x10\xf0\x01\x0f\x1a\xbf\x00\x20\x02\xdf\x01\x20\x70\x47",
				b"\xef\xf3\x05\x80\x00\x28\x1c\xbf\x01\x20\x70\x47\xef\xf3\x14\x80\x10\xf0\x01\x0f\x1a\xbf\x01\x20\x02\xdf\x01\x20\x70\x47"
			)
			# change the function telling whether to include the authorization header
			m = search(
				b"..".join([escape(b"\x38\xb5\x04\x46\x0d\x46\x01\x46\x0c\x48\x32\xf0"), escape(b"\x50\xb1\x20\x46\x32\xf0"), escape(b"\x0a\x28\x0e\xd9\x0a\x38\x08\x49\x20\x44\x32\xf0"), escape(b"\x40\xb9\x05\x22\x06\x49\x28\x46\x32\xf0"), escape(b"\xb0\xfa\x80\xf0\x40\x09\x38\xbd\x00\x20\xfc\xe7")])
			, decrypted, flags=DOTALL)
			idx = m.start()
			match = m[0]
			decrypted = decrypted[:idx] + \
				match + \
				(0x08010000 + len(decrypted)).to_bytes(4, byteorder="little") + \
				decrypted[idx + 0x40:] + \
				b"sydh.date\x00"
		md5_hash = md5(decrypted).digest()[:8]
		pdfw.write(dec_header[:8])
		pdfw.write((len(decrypted)).to_bytes(4, byteorder="little"))
		pdfw.write(dec_header[12:24])
		pdfw.write(md5_hash)
		pdfw.write(decrypted)
	quit()
