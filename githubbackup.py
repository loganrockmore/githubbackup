#!/usr/bin/python

import argparse
import base64
import datetime
import json
import os
import subprocess
import sys
import urllib2

parser = argparse.ArgumentParser()
parser.add_argument("--token", help = "Github Personal Access Token. This can be generated at https://github.com/settings/tokens", required=True)
parser.add_argument("--output", help = "Path to the output directory", required=True)
args = parser.parse_args()

headers = {"Authorization" : "token %s" % (args.token)}
request = urllib2.Request('https://api.github.com/user/repos?per_page=100', headers=headers)
responseData = urllib2.urlopen(request)
responseString = responseData.read()
response = json.loads(responseString)

if 100 <= len(response):
	print "ERROR: this script only gets the first 100 repos and it appears that this user has reached that limit. At this point, this script needs to be updated to handle pagination of the Github API."
	sys.exit(999)
	
# make the output directory
todaysDate = datetime.datetime.now().strftime("%Y-%m-%d")
outputDirectoryPath = os.path.join(args.output, todaysDate)
os.mkdir(outputDirectoryPath)

# define git function
def git(*args):
    return subprocess.check_call(['git'] + list(args))

# loop through all repos
for repo in response:
	gitName = repo["name"]
	gitURL = repo["ssh_url"]
	
	formattedJSON = json.dumps(repo, sort_keys=True, indent=4, separators=(',', ': '))
	jsonFilename = os.path.join(outputDirectoryPath, gitName + '.json')
	with open(jsonFilename, 'w') as file:
		file.write(formattedJSON)
	
	repoOutputPath = os.path.join(outputDirectoryPath, gitName)
	git("clone", gitURL, repoOutputPath)
	
	print