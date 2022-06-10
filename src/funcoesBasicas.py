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
    novaImagem = Imagem.copy().astype(int)
    for i in range(novaImagem.shape[2]):
        novaImagem[:,:,i] = novaImagem[:,:,i] - 128
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

    Q = np.array(Q)

    if fator > 50 :
        Q = Q * ((100.0 - fator)/50.0)
    elif(fator < 50):
        Q = Q * 50.0/fator
    return Q.astype(np.uint8)

def reshapeImage(ImagemArray): 
    newImage = ImagemArray.copy()
    row,cols, depth = newImage.shape
    newRows = int(row/8) * 8
    newCols = int(cols/8) * 8
    return newImage.reshape((newRows,newCols,depth))

def verifyPixelValue(Block):
    newBlock = Block.copy()
    for i in range(len(newBlock)):
        for j in range(len(newBlock)):
            if newBlock[i,j] > 255:
                newBlock[i,j] = 255
            elif newBlock[i,j] < 0:
                newBlock[i,j] = 0
    return newBlock

def calculateOutMatrix(ImagemArray,fator):
    newImagemArray = ImagemArray.copy()
    newImagemArray = reshapeImage(newImagemArray).astype(float)
    newImagemArray = np.array(converterParaYCbCr(newImagemArray)).astype(float)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = gerarMatrizQuantizacao2(fator)
    for h in range(newImagemArray.shape[2]):
        for i in range(0,newImagemArray.shape[0], 8):
            for j in range(0, newImagemArray.shape[1],8):
                data = newImagemArray[i:i+8,j:j+8,h]
                out1 = np.matmul(DCTMatrix,data)
                out2 = np.matmul(out1, np.transpose(DCTMatrix))
                dataOut = np.divide(out2,quantization).round()
                #DivideByQuantizationMatrix(out2,quantization)
                newImagemArray[i:i+8,j:j+8,h] = dataOut
    return newImagemArray

def losslessQuantization():
    return [
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,0,0,0],
        [1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]

def decompressImage(ImagemArray,fator):
    newImageArray = ImagemArray.copy()
    newImageArray = reshapeImage(newImageArray)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = gerarMatrizQuantizacao2(fator)
    for h in range(newImageArray.shape[2]):
        for i in range(0,newImageArray.shape[0],8):
            for j in range(0,newImageArray.shape[1],8):
                data = newImageArray[i:i+8,j:j+8,h]
                matrizR = np.multiply(quantization,data)
                #gerarMatrizR(quantization,data)
                out1 = np.matmul(np.transpose(DCTMatrix),matrizR)
                out2 = np.matmul(out1,DCTMatrix)
                out3 = out2.round()
                outFinal = out3 + 128
                outFinal = verifyPixelValue(outFinal)
                newImageArray[i:i+8,j:j+8,h] = outFinal
    return newImageArray

def losslessDCT(ImagemArray):
    newImagemArray = ImagemArray.copy()
    newImagemArray = reshapeImage(newImagemArray).astype(float)
    #newImagemArray = converterParaYCbCr(newImagemArray)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = losslessQuantization()
    for h in range(newImagemArray.shape[2]):
        for i in range(0,newImagemArray.shape[0],8):
            for j in range(0,newImagemArray.shape[1],8):
                data = newImagemArray[i:i+8,j:j+8,h]
                out1 = np.matmul(DCTMatrix,data)
                out2 = np.matmul(out1,np.linalg.inv(DCTMatrix))
                out3 = out2*quantization
                newImagemArray[i:i+8,j:j+8,h] = out3
    return newImagemArray
            

def decompressLosslessDCT(ImagemArray):
    newImagemArray = ImagemArray.copy()
    newImagemArray = reshapeImage(newImagemArray).astype(float)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    for h in range(newImagemArray.shape[2]):
        for i in range(0,newImagemArray.shape[0],8):
            for j in range(0,newImagemArray.shape[1],8):
                data = newImagemArray[i:i+8,j:j+8,h]
                out1 = np.matmul(np.linalg.inv(DCTMatrix),data)
                out2 = np.matmul(out1,DCTMatrix)
                out2 = verifyPixelValue(out2)
                newImagemArray[i:i+8,j:j+8,h] = out2
    return newImagemArray
