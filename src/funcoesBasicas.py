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

def reshapeImage(ImagemArray): 
    newImage = ImagemArray.copy()
    row,cols = newImage.shape
    newRows = int(row/8) * 8
    newCols = int(cols/8) * 8
    return newImage.reshape((newRows,newCols))

def calculateOutMatrix(ImagemArray,fator):
    newImagemArray = ImagemArray.copy()
    newImagemArray = converterParaYCbCr(newImagemArray)
    newImagemArray = reshapeImage(newImagemArray)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = gerarMatrizQuantizacao2(fator)
    for i in range(0,newImagemArray.shape[0]-1, 8):
        for j in range(0, newImagemArray.shape[1]-1,8):
            data = newImagemArray[i:i+8,j:j+8]
            out1 = np.matmul(DCTMatrix,data)
            out2 = np.matmul(out1, np.linalg.inv(DCTMatrix))
            dataOut = DivideByQuantizationMatrix(out2,quantization)
            newImagemArray[i:i+8,j:j+8] = dataOut
    return newImagemArray


def gerarMatrizR(Q,C):
    R = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            R[i][j] = Q[i][j] * C[i][j]
    return R

def decompressImage(ImagemArray,fator):
    newImageArray = ImagemArray.copy()
    newImageArray = reshapeImage(newImageArray)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = gerarMatrizQuantizacao2(fator)
    for i in range(0,newImageArray.shape[0]-1,8):
        for j in range(0,newImageArray.shape[1]-1,8):
            data = newImageArray[i:i+8,j:j+8]
            matrizR = gerarMatrizR(quantization,data)
            out1 = np.matmul(np.linalg.inv(DCTMatrix),matrizR)
            out2 = np.matmul(out1,DCTMatrix)
            out3 = out2.round()
            outFinal = out3 + 128
            newImageArray[i:i+8,j:j+8] = outFinal
    return newImageArray