import numpy as np 
from scipy.io import loadmat
from matplotlib import pyplot as plt
#from ecgdetectors import Detectors
from scipy.signal import find_peaks
import statistics


'''*******************************************************
   3. CARGA DE SEÑALES
*******************************************************'''

#cargar los datos previamente almacenados en la carpeta
data1 = loadmat("100m (8).mat")
data2 = loadmat("203m (1).mat")
data3 = loadmat("223m (7).mat")

#guardar el dataset en una variable
x = data1['val']
x1 = x[0] #almacenar sólo la información de la primera hilera para poder trabajar con ella
print('PRIMERA SENAL', x1)

y = data2['val']
x2 = y[0]
#print(x2)

z = data2['val']
x3 = z[0]
#print(x3)


#gráfica de la primera señal
plt.plot(x1)
plt.show()


'''*******************************************************
   4.   ELIMINAR LÍNEA BASE, VALOR PROMEDIO
       POR MEDIO DE FILTRO PASA ALTAS Y CONV
*******************************************************'''

#Definir los coeficientes para el proceso de convolución
Coef = np.genfromtxt('filtropa.csv', delimiter=',')


#Proceso de convolución para poner en cero la gráfica
Tpa = np.convolve(x1, Coef)
plt.plot(Tpa)
plt.show()


#Quitar las muestras agregadas por la convolución sucia, IMPORTANTE revisar de nuevo el verdadero len de coef
lencoef = len(Coef)
print("lencoef: ", lencoef) 

#conocer el len de la señal
lensign = len(x1)
print("lensign: ", lensign)
lenquitar = lensign - lencoef

#Eliminar los picos quitando las muestras agregadas conociendo el tamaño de la señal
ECGlimpio1 = Tpa[lencoef:len(Tpa)]
ECGlimpio = ECGlimpio1[:lenquitar]


#plt.plot(ECGlimpio1)
plt.plot(ECGlimpio)
plt.show()


'''*******************************************************
   5.     APLICAR FILTRO PASO BANDA CON 
        FRECUENCIAS DE CORTE EN 1HZ Y 20HZ
*******************************************************'''

#Cálculo filtro pasa banda
Coefb = np.genfromtxt('filtropasabanda.csv', delimiter=',')
Tpb = np.convolve(ECGlimpio, Coefb)
plt.plot(Tpb)
plt.show()



'''*******************************************************
   6.     NORMALIZAR LA SEÑAL SOBRE EL VALOR
            MÁXIMO ENCONTRADO DE LA SEÑAL
*******************************************************'''

#Encontrar el valor máximo
picomax = np.max(Tpb)
print(picomax)

#Normalizar
tnorm = Tpb/picomax
print(tnorm)



'''*******************************************************
   7.     MEJORAR LA RELACIÓN SEÑAL/RUIDO
*******************************************************'''

#Elevar la señal al cuadrado
signal = tnorm**2
plt.plot(signal)
plt.show()


'''*******************************************************
   8.     ENCONTRAR LOS PICOS
*******************************************************'''
#
picos, _ = find_peaks(signal, prominence=0.3)
plt.plot(signal)
plt.plot(picos, signal[picos], "x")
plt.plot(np.zeros_like(x), '--', color = "gray")
plt.show()
print('picos:', picos)



'''
ESTAS FUERON PRUEBAS PARA VER SI LA LIBRERÍA ERA DE AYUDA PERO NINGUNA DIO EL RESULTADO BUSCADO
fs = 360
detectors = Detectors(fs)
#r_peaks = detectors.pan_tompkins_detector(signal) #FALLA EN ALGUNOS Y EN OTROS LOS PONE EN MEDIO
#r_peaks = detectors.hamilton_detector(signal) #PONE LOS PICOS HASTA ABAJO
#r_peaks = detectors.christov_detector(signal) #SOLO PONE BIEN 3, LO DEMAS EN MEDIO
#r_peaks = detectors.engzee_detector(signal)#SOLO FALLA EN EL PRIMER PICO y 3 QUE NO IDENTIFICA
#r_peaks = detectors.swt_detector(signal) #FALLA EN TODOS
r_peaks = detectors.two_average_detector(signal) #TODOS EN MEDIO
#r_peaks = detectors.wqrs_detector(signal) #PONE LOS PICOS MUY ABAJO

plt.figure()
plt.plot(signal)
plt.plot(r_peaks, signal[r_peaks], 'ro')
plt.title('Detected R-peaks')
plt.show()
'''

'''*******************************************************
   10.    MEDIR DISTANCIA ENTRE LOS PICOS
                 DE LAS SEÑALES
*******************************************************'''


diff = np.diff(picos)
print('distancias: ', diff)



'''*******************************************************
   11.    ANALIZAR DISTANCIAS ENTRE CICLOS CARDIACOS
         PARA OBTENER VALORES DE ESTADISTICA DESCRIPTIVA
*******************************************************'''

#Media entre picos
media = float(statistics.mean(diff))
print('media', media)

#Desviación estándar
dsvest = float(statistics.stdev(diff))
print('desviación estándar: ', dsvest)

#Valor máximo
val_max = max(diff)
print('valor máximo: ', val_max)

#Valor mínimo
val_min = min(diff)
print('valor mínimo: ', val_min)


'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    REFERENCIAS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

https://stackoverflow.com/questions/1713335/peak-finding-algorithm-for-python-scipy
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
https://www.irjet.net/archives/V6/i4/IRJET-V6I4479.pdf



'''