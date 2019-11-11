print("Checking for Flashpoint Infinity Nightly update...")

import urllib.request, os, zipfile, json
from datetime import datetime

#next 2 lines adapted from https://stackoverflow.com/a/29327717
req = urllib.request.Request("https://unstable.life/flashpoint-nightly/Infinity-Stage1-nightly.zip", method="HEAD")
resp = urllib.request.urlopen(req)

update = False

try:
	data = json.loads(open("updatercfg.json", "r").read())
	#Thanks http://strftime.org/, though I'm not sure if all of these numbers are zero-padded
	if (datetime.strptime(resp.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z') > datetime.strptime(data['last-updated'], '%a, %d %b %Y %H:%M:%S %Z')):
		update = True
except:
	data = {'last-updated': ''}
	update = True
	
if update:
	print("Update found!")
	print("Downloading update...")
	urllib.request.urlretrieve("https://unstable.life/flashpoint-nightly/Infinity-Stage1-nightly.zip", "Infinity-Stage1-nightly.zip")
	
	print("Extracting update...")
	#next 2 lines adapted from https://stackoverflow.com/a/3451150
	with zipfile.ZipFile("Infinity-Stage1-nightly.zip", 'r') as zip_ref:
		zip_ref.extractall() #extract to current directory

print("Flashpoint Infinity Nightly is up to date!")
print("Launching now...")
os.system("cd Infinity-Stage1-nightly//Launcher && FlashpointLauncher.exe") #this line might be Windows-specific

if update:	
	print("Cleaning up...")
	data['last-updated'] = resp.headers['Last-Modified']
	open("updatercfg.json", "w").write(json.dumps(data))
	os.remove("Infinity-Stage1-nightly.zip")