# pip install requests
from requests import get

from sys import argv, exit

FIRMWARE_API = f"https://play.date/api/v2/firmware/?current_version=2.0.2"

r = get(FIRMWARE_API, headers={
	"Authorization": f"Token {argv[1]}"
})

if r.status_code == 204:
	print("No content")
elif r.status_code == 200:
	print(r.json()["version"])
else:
	print("Error")
