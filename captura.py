import csv
from subprocess import Popen, PIPE
import re
import time
import array

hostname = "www.ufjf.br"

RTT = array.array('f')

def run(host):

    p = proc=Popen(['ping',host,'-n', '1','-w','10000'], stdout=PIPE)
    ret =  p.stdout.read()
    m = re.search('tempo=(.*)ms', ret)
  
    if m:
        rttMedido = float(m.group(1))
        print rttMedido
        RTT.append(rttMedido)        

    else: 
        print 'Timeout'        

for i in range(0,1000):
    run(hostname)
    time.sleep(1.0)
    print 'Ping',i

fileName = 'rttSamples.csv'
ofile  = open(fileName, "wb")
writer = csv.writer(ofile)

for row in zip(RTT):    
    writer.writerow(row)

ofile.close()