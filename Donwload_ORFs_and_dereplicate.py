# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:07:03 2023

@author: dl923 / leadbot
"""

from bs4 import BeautifulSoup
import urllib
from Bio import SeqIO

target_url='' 
outfastafile=''

#send http request, read the html content
html = urllib.request.urlopen(target_url).read()
##create beutiful soup object to parse html content
soup = BeautifulSoup(html, 'html.parser')
#scrape all visible text
text = soup.get_text()

text=text.strip('\n\nEMBOSS: output\n\n\n\nEMBOSS explorer\n\n\n\nOutput file \xa0\n        outseq\n')
####write as fasta

f=open(outfastafile, 'w')
f.write(text)
f.close()



###Dreplication
import time
import matplotlib.pyplot as plt
###Dreplication FAST
c=0
u=0
seqs=[]
tic=time.perf_counter()
times=[]

seen=set()
records=[]

for record in SeqIO.parse(outfastafile, 'fasta'):
     c+=1
     if record.seq not in seen:
          seen.add(record.seq)
          records.append(record)
          u+=1
     if c%5000==0:
          tok=time.perf_counter()
          print("Iterated over %a sequences" % c)
          print('Len unique list: ' + str(u)) 
          t=tok-tic
          print(f"This batch of sequences took {tok - tic:0.4f} seconds to search")
          tic=time.perf_counter()
          times.append(t)
     if c%100000==0:
          plt.plot(list(range(0, len(times))), times)
          plt.show()


SeqIO.write(records,outfastafile.strip('.faa').strip('.fasta')+'_Dereplicated.faa', 'fasta')