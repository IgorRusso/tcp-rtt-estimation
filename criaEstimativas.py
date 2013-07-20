import csv
from matplotlib.pylab import *
import array

#Vetor para guardar os RTTs medidos pelo script captura.py
RTT = array.array('f')

#Vetores para as estimativas calculadas
SRTT1 = array.array('f')
SRTT1.append(0)
SRTT2 = array.array('f')
SRTT2.append(0)

#Vetores para os timeouts calculados
RTO1 = array.array('f')
RTO2 = array.array('f')

A = 0.85
B = 2

def carregaRTTS():
    #abre o arquivo de capturas para obter os valores medidos
    ifile  = open('rttSamplesLocal.csv', "rb")
    reader = csv.reader(ifile)

    #carrega os valores medidos no vetor RTT
    for row in reader:
        rtt = float(row[0])
        RTT.append(rtt)   

    ifile.close()

def calcRTTEstimado1(i):
    estimativa_proximo_rtt = (A)*SRTT1[i] + (1-A)*RTT[i]
    SRTT1.append(estimativa_proximo_rtt)
    proximo_rto= B * estimativa_proximo_rtt
    RTO1.append(proximo_rto)    

def calcRTTEstimado2(i):
    
    if (i==0):
       estimativa_proximo_rtt = 0
    else:
        k = i-1;     
        
        t1 = float(k)
        t2 = t1+1
        estimativa_proximo_rtt = (t1/t2)*SRTT2[k] + (1.0/t2)*RTT[k+1]
        #print k,SRTT2[k],RTT[k+1],estimativa_proximo_rtt

    SRTT2.append(estimativa_proximo_rtt)
    proximo_rto= B * estimativa_proximo_rtt
    RTO2.append(proximo_rto)


def main():
    carregaRTTS()
    print len(RTT)
    for i in range(0, len(RTT)):        
        calcRTTEstimado1(i)
        calcRTTEstimado2(i)

    SRTT1.remove(0)
    SRTT2.remove(0)

    t = zeros(len(RTT))
    for i in range(0,len(t)):
        t[i] = i

    #figure(figsize=(20, 8))

    plot(t, RTT, 'r-')
    hold('on')
    plot(t, SRTT1, 'bo')
    hold('on')
    plot(t, RTO1, 'b-')

    xlabel('t')
    ylabel('y')

    legend(['RTT','SRTT','TIMEOUT SRTT'])
    savefig('srttLocal.png')
    
    figure()
    
    subplot(1,1,1)

    plot(t, RTT, 'r-')
    hold('on')
    plot(t, SRTT2, 'go')
    hold('on')  
    plot(t, RTO2, 'b-')

    xlabel('t')
    ylabel('y')

    legend(['RTT','ARTT','TIMEOUT ARTT'])
    savefig('arttsLocal.png') # produce PNG

    show()

main()