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
D = array.array('f')
D.append(0)



A = 0.85
B = 2

def carregaRTTS():
    #abre o arquivo de capturas para obter os valores medidos
    ifile  = open('rttSamples.csv', "rb")
    reader = csv.reader(ifile)

    #carrega os valores medidos no vetor RTT
    for row in reader:    
        rtt = float(row[0])
        RTT.append(rtt)   

    ifile.close()

def calcRTTEstimadoKarns(i):
    estimativa_proximo_rtt = (A)*SRTT1[i] + (1-A)*RTT[i]
    SRTT1.append(estimativa_proximo_rtt)
    proximo_rto= B * estimativa_proximo_rtt
    RTO1.append(proximo_rto)    

def calcRTTEstimadoJacobs(i):
    g = 0.125
    h = 0.25
    erro = RTT[i] - SRTT2[i];    
    estimativa_proximo_rtt = SRTT2[i] + g*erro
    SRTT2.append(estimativa_proximo_rtt);
    proximo_d = D[i] + h*(abs(erro)- D[i])
    D.append(proximo_d);

    proximo_rto = estimativa_proximo_rtt +4*proximo_d;
    RTO2.append(proximo_rto);


def main():
    carregaRTTS()
    #print RTT

    for i in range(0, len(RTT)):        
        calcRTTEstimadoKarns(i)
        calcRTTEstimadoJacobs(i)

        #print 'RTT:',RTT[i],' ; estimativa1: ', SRTT1[i], ', estimativa2: ', SRTT2[i]

    SRTT1.remove(0)
    SRTT2.remove(0)

    print len(RTT), len(SRTT1)


    t = zeros(len(RTT))
    for i in range(0,len(t)):
        t[i] = i

    #plot(t, RTT)
    plot(t, RTT, 'r-')
    hold('on')
    plot(t, SRTT1, 'go')
    hold('on')
    plot(t, SRTT2, 'bo')


    xlabel('t')
    ylabel('y')  
    legend(['RTT'])
    savefig('rtts.png') # produce PNG
    show()

main()