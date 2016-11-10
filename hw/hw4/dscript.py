import os
import subprocess

from functools import lru_cache
import csv
memoize = lru_cache(1)
@memoize
def read_domains():
    cols = ['site','domain','alexia','similarweb','type','country']
    with open('domains.tsv','rt') as rfp:
        reader = csv.DictReader(rfp,cols,delimiter='\t')
        domains = list(reader)
    return domains

domainsDict = read_domains()
del domainsDict[0]
print(domainsDict[0])

#holder = os.system("host "+domainsDict[0]['domain'])
dHolder = domainsDict[0]['domain']
holder = subprocess.check_output("host "+dHolder,shell=True)
holder = str(holder,'utf-8').split('\n')
containing = [line for line in holder if "has address" in line]
print(containing)
for item in containing:
    tItem = item.split(' ')
    ip = tItem[len(tItem)-1]
    print(ip)
    try:
        test = subprocess.check_output("host "+ip,shell=True)
    except:
        test = b""
    ipContainer = str(test,'utf-8').split('\n')
    print(ipContainer)
    for item2 in ipContainer:
        tItem2 = item2.split(' ')
        reverseIP = tItem2[len(tItem2)-1]
        print(reverseIP)
