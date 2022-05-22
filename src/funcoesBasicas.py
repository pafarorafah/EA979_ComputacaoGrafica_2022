import math
from PIL import Image
import numpy as np

def convertNumpy(img):
    array = np.array(img)
    return array

def openImage(path):
    img = Image.open(path)
    Image._show(img)
    return convertNumpy(img)

#Utiliza os coeficientes
def gerarMatrizCoeficentesDCT(N):
    DCT = []
    for h in range(N):
        DCTline = np.zeros(N)
        DCT.append(DCTline)
    for x in range(N):
        for y in range(N):
            if x == 0:
                DCT[x][y] = 1/math.sqrt(N)
            else:
                DCT[x][y] = math.sqrt(2/N) * math.cos((2*y+1)*x*math.pi/(2*N))
    return DCT

def converterParaYCbCr(Imagem):
    novaImagem = Imagem.copy()
    for i in range(len(Imagem)):
        for j in range(len(Imagem[0])):
            novaImagem[i][j] = Imagem[i][j] - 128
    return novaImagem

def gerarMatrizQuantizacao2(fator):
    Q = [
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ]
    if fator > 50 :
        for i in range(8):
            for j in range(8):
                Q[i][j] = round(Q[i][j] * (100 - fator)/50)
                if(Q[i][j] > 255):
                    Q[i][j] = 255
    elif(fator < 50):
        for i in range(8):
            for j in range(8):
                Q[i][j] = round(Q[i][j] * 50/fator)
                if(Q[i][j] > 255):
                    Q[i][j] = 255
    return Q

def DivideByQuantizationMatrix(D,Q):
    C = []
    for i in range(len(Q)):
        CLine = np.zeros(len(Q))
        C.append(CLine)
    for i in range(len(Q)):
        for j in range(len(Q)):
            C[i][j] = round(D[i][j]/Q[i][j])
    return C





