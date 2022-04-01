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
data1 = loadmat(r"C:\Users\moral\Desktop\FENBIOACT2\100m (8).mat")
data2 = loadmat(r"C:\Users\moral\Desktop\FENBIOACT2\203m (1).mat")
data3 = loadmat(r"C:\Users\moral\Desktop\FENBIOACT2\223m (7).mat")

#guardar el dataset en una variable
x = data1['val']
#x1 = x[0] #almacenar sólo la información de la primera hilera para poder trabajar con ella
#print('PRIMERA SENAL', x1)

y = data2['val']
#x1 = y[0]
#print(x2)

z = data3['val']
x1 = z[0]
#print(x3)


#gráfica de la primera señal
plt.plot(x1)
plt.title("Señal Original")
plt.show()


'''*******************************************************
   4.   ELIMINAR LÍNEA BASE, VALOR PROMEDIO
       POR MEDIO DE FILTRO PASA ALTAS Y CONV
*******************************************************'''

#Definir los coeficientes para el proceso de convolución
Coef = np.genfromtxt(r'C:\Users\moral\Desktop\FENBIOACT2\filtropa.csv', delimiter=',')


#Proceso de convolución para poner en cero la gráfica
Tpa = np.convolve(x1, Coef)
plt.plot(Tpa)
plt.title("Eliminación de Línea Base por Medio de Filtro Pasa Altas")
plt.axhline(y=0, color='r', linestyle='-')
plt.show()


#Quitar las muestras agregadas por la convolución sucia, IMPORTANTE revisar de nuevo el verdadero len de coef
lencoef = len(Coef)
#print("lencoef: ", lencoef) 

#conocer el len de la señal
lensign = len(x1)
#print("lensign: ", lensign)
lenquitar = lensign - lencoef

#Eliminar los picos quitando las muestras agregadas conociendo el tamaño de la señal
ECGlimpio1 = Tpa[lencoef:len(Tpa)]
ECGlimpio = ECGlimpio1[:lenquitar]


#plt.plot(ECGlimpio1)
plt.plot(ECGlimpio)
plt.axhline(y=0, color='r', linestyle='-')
plt.title("Picos eliminados")
plt.show()


'''*******************************************************
   5.     APLICAR FILTRO PASO BANDA CON 
        FRECUENCIAS DE CORTE EN 1HZ Y 20HZ
*******************************************************'''

#Cálculo filtro pasa banda
Coefb = np.genfromtxt(r'C:\Users\moral\Desktop\FENBIOACT2\filtropasabanda.csv', delimiter=',')
Tpb = np.convolve(ECGlimpio, Coefb)
plt.plot(Tpb)
plt.axhline(y=0, color='r', linestyle='-')
plt.title("Filtro Pasa Banda 1Hz y 20Hz")
plt.show()



'''*******************************************************
   6.     NORMALIZAR LA SEÑAL SOBRE EL VALOR
            MÁXIMO ENCONTRADO DE LA SEÑAL
*******************************************************'''
#print('NOOORMAAALIIIZAR')
#Encontrar el valor máximo
picomax = np.max(Tpb)
#print(picomax)

#Normalizar
tnorm = Tpb/picomax
#print(tnorm)

plt.plot(tnorm)
plt.title("FUNCION NORMALIZADA")
plt.axhline(y=0, color='r', linestyle='-')
plt.show()



'''*******************************************************
   7.     MEJORAR LA RELACIÓN SEÑAL/RUIDO
*******************************************************'''

#Elevar la señal al cuadrado
signal = tnorm**2
plt.plot(signal)
plt.title("Relación Señal/Ruido Mejorada")
plt.show()


'''*******************************************************
   8.     ENCONTRAR LOS PICOS
*******************************************************'''
#
picos, _ = find_peaks(signal, prominence=0.3)
plt.plot(signal)
plt.plot(picos, signal[picos], "x")
plt.title("Picos")
#plt.plot(np.zeros_like(x), '--', color = "gray")
plt.show()

#print('picos:', picos)



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
#print('distancias: ', diff)



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


'''*******************************************************
   11.                GRÁFICAS
*******************************************************'''
fig, ((ax1), (ax2), (ax3), (ax4), (ax5), (ax6), (ax7)) = plt.subplots(7, 1)
ax1.plot(x1)  #señal original
ax1.set_title("Señal Original")
ax2.plot(Tpa)
ax2.set_title("filtro pasa altas")
ax2.axhline(y=0, color='r', linestyle='-')
ax3.plot(ECGlimpio)
ax3.axhline(y=0, color='r', linestyle='-')
ax3.set_title("Eliminación de picos agregados por filtro pasa altas")
ax4.plot(Tpb)
ax4.axhline(y=0, color='r', linestyle='-')
ax4.set_title("Filtro paso banda")
ax5.plot(tnorm)
ax5.axhline(y=0, color='r', linestyle='-')
ax5.set_title("Señal Normalizada")
ax6.plot(signal)
ax6.axhline(y=0, color='r', linestyle='-')
ax7.set_title("Relción señal/ruido")
ax7.plot(signal)
ax7.axhline(y=0, color='r', linestyle='-')
ax7.plot(picos, signal[picos], "x")
ax7.set_title("Picos")
plt.show()

'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    REFERENCIAS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

https://stackoverflow.com/questions/1713335/peak-finding-algorithm-for-python-scipy
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
https://www.irjet.net/archives/V6/i4/IRJET-V6I4479.pdf



'''