import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

ARQ_ENT = "Out_TimeDomain.csv"
DELIMITADOR = " "

def testFFT():

    tf = 40
    incremento =0.001

    # Generating a signal 
    t = np.arange(0,tf,incremento) # A domain from 0 o 100 equally spaced made by 100 points
    y = 3.797*np.sin(2*np.pi * 3.5 * t) + 4*np.cos(2*np.pi * 9 * t) + 1.*np.sin(2*np.pi* 1 * t) # Generating a sin shape signal ( 3 Hz )

    # Ploting the signal
    plt.plot(t, y, color = "red")
    plt.plot([0, 10], [0, 0], color="black")
    plt.title("Signal (sinoidal)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude [m]")
    plt.axis()
    plt.xlim(0, 10)
    #plt.ylim(-1.25, 1.25)
    plt.show()

    # Generating the FFT
    FFT = np.fft.fft(y)/(tf / (incremento * 2) )

    # OBS.: 'd' is the sample space (the inverse of the sample frequency). When is not given, the default is 1
    freq = np.fft.fftfreq( t.shape[-1], d=incremento )

    # Limiting the axis and te data
    N_dados = t.shape[-1]

    freq_pos = freq[ 0:int(N_dados/2)]
    FFT_pos = FFT[ 0:int(N_dados/2)]

    with open(ARQ_ENT, "w") as saida:
        arquivo = csv.writer(saida, delimiter=DELIMITADOR)

        for i in range(len(t)):
            arquivo.writerow([t[i], y[i]])

    # Ploting the data (Let it beaultiful, baby)
    plt.plot(freq_pos, np.abs(FFT_pos))
    plt.xlim(min(freq_pos), 40)

    plt.show()

def aplicaFFT(t, y):
    incremento = t[1] - t[0]
    tf = t[-1]

    # Generating the FFT
    FFT = np.fft.fft(y)/(tf / (incremento * 2) )

    # OBS.: 'd' is the sample space (the inverse of the sample frequency). When is not given, the default is 1
    freq = np.fft.fftfreq( t.shape[-1], d=incremento )

    # Limiting the axis and te data
    N_dados = t.shape[-1]

    freq_pos = freq[ 0:int(N_dados/2)]
    FFT_pos = FFT[ 0:int(N_dados/2)]

    with open(ARQ_ENT, "w") as saida:
        arquivo = csv.writer(saida, delimiter=DELIMITADOR)

        for i in range(len(t)):
            arquivo.writerow([t[i], y[i]])

    return freq_pos, np.abs(FFT_pos)

def readCSV():

    t = []
    y = []
    dy = []

    try:
        with open(ARQ_ENT, "r") as entrada:
            csv_f = csv.reader(entrada, delimiter=DELIMITADOR)

            # Jumping the reader
            entrada.readline()

            # Counting lines
            nLin = 0
            for i in csv_f:
                nLin += 1
            
            entrada.seek(0)

            # Jumping the reader
            entrada.readline()

            t = np.zeros(nLin)
            y = np.zeros(nLin)
            dy = np.zeros(nLin)

            var = 0
            for i in csv_f:
                t[var] = i[0]
                y[var] = i[1]
                var += 1

        return t, y, dy
    
    except:
        print("Erro abrindo o arquivo \'", ARQ_ENT, "\'. Verifique sua existência!")
        
        return [], [], []

def execFFT():
    t, y, dy = readCSV()

    # Ploting the signal
    plt.plot(t, y, color = "red")
    plt.plot([0, 10], [0, 0], color="black")
    plt.title("Signal (sinoidal)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude [m]")
    plt.axis()
    plt.xlim(0, 10)
    plt.show()


    frequencia, amplitude = aplicaFFT(t, y)

    # Ploting the data (Let it beaultiful, baby)
    plt.plot(frequencia, amplitude)

    plt.show()

if "-G" in sys.argv:
    testFFT()


if "-FFT" in sys.argv:
    execFFT()

else:
    print(f"Missing command line arguments\nOptions:\n\t-G\t:\t Generates a signal for testing\n\t-FFT\t:\tApply FFT in the data \
saved in a file called \"{ARQ_ENT}\"\n")
    
