# pip install beautifulsoup4

from bs4 import BeautifulSoup
from requests import get

from sys import argv, exit

r = get("https://sdk.play.date/changelog/")
if r.status_code != 200:
	print(f"Changelog page returned status code {r.status_code}")
	exit(1)

soup = BeautifulSoup(r.text, "html.parser")
for child in soup.find_all(class_="sect1"):
	release = [s for s in child.contents if s != "\n"]
	if release[0].string == argv[1]:
		print(release[1])
		exit(0)

print(f"Version {argv[1]} not found")
exit(1)
