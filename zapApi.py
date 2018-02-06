#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL
import time
import os
from pprint import pprint
from zapv2 import ZAPv2

  
docker = 'http://IPdocker'
port = 'PORT' #ex (typical 8080)
#target = 'http://demo.testfire.net' #ex1 - testing webs
#target = 'http://testphp.vulnweb.com' #ex2  - testing webs
target = 'http://your.target.com'
apikey = 'YOUR_ZAP_API_KEY' # Change to match the API key set in ZAP, or use None if the API key is disabled
#
# By default ZAP API client will connect to port 8080
# zap = ZAPv2(apikey=apikey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
zap = ZAPv2(apikey=apikey, proxies={'http': docker + ':' + port , 'https': docker + ':' + port})

# Proxy a request to the target so that ZAP has something to deal with
print('Accessing target {}'.format(target))
zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

print('Spidering target {}'.format(target))
scanid = zap.spider.scan(target)
# Give the Spider a chance to start
time.sleep(2)
while (int(zap.spider.status(scanid)) < 100):
    # Loop until the spider has finished
    print('Spider progress %: {}'.format(zap.spider.status(scanid)))
    time.sleep(2)

print ('Spider completed')

while (int(zap.pscan.records_to_scan) > 0):
      print ('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
      time.sleep(2)

print ('Passive Scan completed')

print ('Active Scanning target {}'.format(target))
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    # Loop until the scanner has finished
    print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
    time.sleep(5)

print ('Active Scan completed')

#function to allow generate a report
def chooseTypeReport(typeOfReport):
	if typeOfReport == "xml":
		print ('Generating XMLReport')
		return zap.core.xmlreport(apikey)
	elif typeOfReport == "html":
		print ('Generating HTMLReport')
		return zap.core.htmlreport(apikey)
	elif typeOfReport == "json":
		print ('Generating JSONReport')
		return zap.core.jsonreport(apikey)
	else: 
		print ('Ups.. you should to introduce a valid type of report')

typeOfReport = input('Select the type of report that you prefer: xml, html or json:')
report = chooseTypeReport(typeOfReport)

#funtion to allow save a report in a particular path
def saveReport(report,target,typeOfReport,path):
	if not os.path.exists(path): 
		os.makedirs(path)
		os.chdir(path)
		open(target.replace('http://','') +'.'+ typeOfReport,'w').write(report)
	else: #if exist
		os.chdir(path)
		open(target.replace('http://','') +'.'+ typeOfReport,'w').write(report)	

pathToSave = input("Introduce path to save the report: ")
saveReport(report,target,typeOfReport,pathToSave)
print("Saved report in: " + pathToSave)

# Report the results in console
#print ('Hosts: {}'.format(', '.join(zap.core.hosts)))
#print ('Alerts: ')
#pprint (zap.core.alerts())


