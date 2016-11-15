import subprocess, collections

## RIP/EDIT from old assignment
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

## Runs host commands and returns their output
def checkHost(ID):
    result = subprocess.check_output("host " + ID, shell = True)
    result = str(result,'utf-8').split('\n')
    return result

domainsDict = read_domains()
del domainsDict[0] ## CLEANUP for header row in file

## COLLECTORS for file outputs
tString = ""
idDicts = collections.OrderedDict() #allows sorting dictionary
ridDicts = collections.OrderedDict() #allows sorting dictionary

## ITER for domains
dDict = {}
for i in range(len(domainsDict)):
    currD = domainsDict[i]['domain']
    print(currD) ## NOTIFY FOR DOING THINGS
    dDict[currD] = []

    ## CATCH no IPs for domain
    try:
        holder = checkHost(currD)
    except:
        holder = ""

    ## ITER for all IPs
    ipDict = {}
    for IPs in [line for line in holder if "has address" in line]:
        ## Isolate ip
        tIPs = IPs.split(' ')
        ip = tIPs[len(tIPs)-1]
        ## CREATE dDicts
        ipDict[ip] = []

        ## FILEIN ipEdges.tsv
        if ip in idDicts.keys():
            idDicts[ip].append(currD)
        else:
            idDicts[ip] = [currD]

        ## CATCH no pointers for ip
        try:
            ipContainer = checkHost(ip)
        except:
            ipContainer = [""]

        ## CLEANUP
        if ipContainer[len(ipContainer)-1] == '':
            del ipContainer[len(ipContainer)-1]

        ## ITER for all ptrs
        for ptr in ipContainer:
            ## Isolate ptr
            tptr = ptr.split(' ')
            reverseIP = tptr[len(tptr)-1]

            if reverseIP == " ": ## CLEANUP bad returns
                pass
            elif reverseIP.count('.') < 2: ## CLEANUP bad returns
                pass
            else:
                ## CREATE dDicts
                ipDict[ip].append(reverseIP)

                ## FILEIN edges.tsv
                tString += (currD + '\t' + ip + '\t' + reverseIP + '\n')

                ## FILEIN ripEdges.tsv
                if reverseIP in ridDicts.keys():
                    ridDicts[reverseIP].append(currD)
                else:
                    ridDicts[reverseIP] = [currD]
    ## CREATE dDicts
    dDict[currD].append(ipDict)

## INFO dDicts contains dictionary of all results
## INFO idDicts contains domains that use specific IP's
## INFO ridDicts contains domains that use specific reverseIP's

## WRITE BLOCK
with open('edges.tsv','wt') as wtp:
    wtp.write(tString)
    wtp.close()

with open('ipEdges.tsv','wt') as wtp:
    tString = ""
    tDict = collections.OrderedDict(sorted(idDicts.items(),key=lambda t: t[0]))
    for key, value in tDict.items():
        tString += key + "\t" + str(value) + '\n'
    wtp.write(tString)
    wtp.close()

with open('ripEdges.tsv','wt') as wtp:
    tString = ""
    tDict = collections.OrderedDict(sorted(ridDicts.items(),key=lambda t: t[0]))
    for key, value in tDict.items():
        tString += key + "\t" + str(value) + '\n'
    wtp.write(tString)
    wtp.close()
