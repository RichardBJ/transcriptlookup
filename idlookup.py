# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 11:17:08 2019

@author: Richard
"""

'''
DO JUST ONE
import requests, sys
server = "http://rest.ensembl.org"
ext = "/lookup/id/ENSRNOT00000091596?expand=1"

r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

if not r.ok:
  r.raise_for_status()
  sys.exit()

decoded = r.json()
print(decoded["display_name"])
'''

'''DO MANY
10x FSTER BUT THEY DONT MATCH PROPERLY AT THE end!!!!
OK, think it does now, but check with several random samples

'''

import requests, sys, time

idlist= ["ENSRNOT00000091596", "ENSRNOT00000091597"]

def lookupbatch(idlist):
    callstr='{ "ids" :['
    for idi in idlist:
        callstr=callstr+'"'+idi+'",'
        
    #delete last comma
    callstr=callstr[:-1]
    callstr=callstr+']}' 
    #print (callstr)
        
    server = "https://rest.ensembl.org"
    ext = "/lookup/id"
    
    
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    print("running a batch")
    '''setting timeout to None to wait for ever'''
    r = requests.post(server+ext, headers=headers, data=callstr, timeout=None)

    if not r.ok:
        print('had a problem, wating a minute')
        time.sleep(60)
        r = requests.post(server+ext, headers=headers, data=callstr, timeout=None)
        if not r.ok:
            print('had a problem, wating 10 minutes')
            time.sleep(600)
            r = requests.post(server+ext, headers=headers, data=callstr, timeout=None)
     
#    if not r.ok:
#      r.raise_for_status()
#      sys.exit()
     
    decoded = r.json()
#    print(repr(decoded))
    #results=repr(decoded)
    #hit=decoded['ENSRNOT00000091597']
    hits=[]
    
    for code in idlist:
        hit=decoded[code]
        hits.append(hit['display_name'])
#        print(code)
#        print(hit['display_name'])
    return hits


file='Galaxy345-DESeq2.txt'
''' MAKE SURE THERE IS NO HEADER!!!'''
file = open(file,mode='r')
idlist=[]
values=[]
outlines=[]

for line in file:
    tran=line.split('\t')
    if len(tran)>1:
        outlines.append(line)
        tran[0]=tran[0].replace('transcript:',"")
        tran[0]=tran[0].replace('gene:',"")
        idlist.append(tran[0])
        values.append(float(tran[1]))
file.close()
STARTAT=0
k=0
j=0
sizes=10
batch=[]
res=[]
total=0;
print("preparing batches")
for idj in idlist:
    j+=1
    batch.append(idj)
    if j==sizes:
        rtn=lookupbatch(batch)
        for val in rtn:
            res.append(val)
        j=0
        batch=[]
        total=total+sizes
        print('total genes done='+str(total))
#get the last few!
batch=lookupbatch(batch)
for b in batch: 
    res.append(b)

print('So lines ({}) should = genes ({})'.format(len(outlines),len(res)))

output=open('results2.tabular','w')

j=0

for line in outlines:
        do=res[j].replace('-201','')
        do=do.replace('-202','')
        do=do.replace('-203','')
        do=do.replace('-204','')
        do=do.replace('-205','')
        do=do.replace('-206','')
        output.write(line[:-1]+'\t'+res[j].replace('-201','')+'\n')
        j=j+1

output.close()    
    

        
print('success if {} = {}'.format(len(res),len(values)))
      

'''
format is
'{ "ids" : ["rs56116432", "COSM476" ] }'
'''


