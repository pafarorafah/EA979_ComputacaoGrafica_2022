import math
import numpy as np

def gerarMatrizDCT(N,Pixel):
    DCT = []
    for h in range(N):
        DCTline = np.zeros(N)
        DCT.append(DCTline)
    for i in range(N):
        for j in range(N):
            temp = 0.0
            for x in range(N) :
                for y in range(N) :
                    temp += math.cos((2*x + 1)*i*math.pi/(2*N)) * math.cos((2*y + 1)*j*math.pi/(2*N)) * Pixel[x][y]
            temp *= math.sqrt(2 * N) * verCoef(i)*verCoef(j)
            DCT[i][j] = int(temp)
    return DCT


def verCoef(x):
    if x == 0:
        return 1/math.sqrt(2)
    return 1


def converterParaYCbCr(Imagem):
    novaImagem = Imagem.copy()
    for i in range(len(Imagem)):
        for j in range(len(Imagem[0])):
            novaImagem[i][j] = Imagem[i][j] - 128
    return novaImagem

def gerarMatrizQuantizacao(fator):
    Q = []
    for i in range(8):
        Q.append(np.zeros(8))
    for i in range(8):
        for j in range(8):
            Q[i][j] = 1 + (1+i+j)*fator
    return Q