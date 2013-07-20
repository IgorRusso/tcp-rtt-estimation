import csv
import array

#Vetor para guardar os RTTs medidos pelo script captura.py
RTT = array.array('f')

#Vetores para as estimativas calculadas
SRTT1 = array.array('f')
SRTT1.append(0)
SRTT2 = array.array('f')
SRTT2.append(0)

#Vetores para os timeouts calculados
timeout1 = array.array('f');
timeout2 = array.array('f');

a = 0.85

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
    estimativa_proximo_rtt = (a)*SRTT1[i] + (1-a)*RTT[i]
    SRTT1.append(estimativa_proximo_rtt)
    timeout1.append(1)

def calcRTTEstimadoJacobs(i):
    estimativa_proximo_rtt = (a)*SRTT2[i] + (1-a)*RTT[i]
    SRTT2.append(estimativa_proximo_rtt)
    timeout2.append(1)


def main():
    carregaRTTS()
    #print RTT

    for i in range(0, len(RTT)):        
        calcRTTEstimadoKarns(i)
        calcRTTEstimadoJacobs(i)

        print 'RTT:',RTT[i],' ; estimativa1: ', SRTT1[i], ', estimativa2: ',SRTT2[i]





main()