import math
from PIL import Image
import numpy as np


mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

def convertNumpy(img):
    bpp = mode_to_bpp[img.mode]
    print(bpp)
    array = np.array(img)
    return array

def openImage(path):
    img = Image.open(path)
    #Image._show(img)
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

def FixImageRange(Imagem):
    novaImagem = Imagem.copy().astype(int)
    for i in range(1):
        novaImagem[:,:] = novaImagem[:,:] - 128
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
    try:
        newImage = newImage[:,:,0]
    except:
        newImage = newImage
    image = Image.fromarray(newImage.astype(np.uint8))
    image = image.resize((480,480),Image.ANTIALIAS)
    newArray = np.asarray(image)
    return newArray

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
    newImagemArray = np.array(FixImageRange(newImagemArray))
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = gerarMatrizQuantizacao2(fator)
    for h in range(1):
        for i in range(0,newImagemArray.shape[0], 8):
            for j in range(0, newImagemArray.shape[1],8):
                data = newImagemArray[i:i+8,j:j+8]
                out1 = np.matmul(DCTMatrix,data)
                out2 = np.matmul(out1, np.transpose(DCTMatrix))
                dataOut = np.divide(out2,quantization).round()
                newImagemArray[i:i+8,j:j+8] = dataOut
    return newImagemArray[:,:]

def losslessQuantization():
    '''
        [1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    '''
    return [
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,0,0,0],
        [1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0]
    ]

def decompressImage(ImagemArray,fator):
    newImageArray = ImagemArray.copy()
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = gerarMatrizQuantizacao2(fator)
    for h in range(1):
        for i in range(0,newImageArray.shape[0],8):
            for j in range(0,newImageArray.shape[1],8):
                data = newImageArray[i:i+8,j:j+8]
                matrizR = np.multiply(quantization,data)
                out1 = np.matmul(np.transpose(DCTMatrix),matrizR)
                out2 = np.matmul(out1,DCTMatrix)
                out3 = out2.round()
                outFinal = out3 + 128
                outFinal = verifyPixelValue(outFinal)
                newImageArray[i:i+8,j:j+8] = outFinal
    return newImageArray

def losslessDCT(ImagemArray):
    newImagemArray = ImagemArray.copy()
    newImagemArray = newImagemArray.astype(float)
    newImagemArray = FixImageRange(newImagemArray)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    quantization = losslessQuantization()
    for h in range(1):
        for i in range(0,newImagemArray.shape[0],8):
            for j in range(0,newImagemArray.shape[1],8):
                data = newImagemArray[i:i+8,j:j+8]
                out1 = np.matmul(DCTMatrix,data)
                out2 = np.matmul(out1,np.transpose(DCTMatrix))
                out3 = np.multiply(out2,quantization)
                newImagemArray[i:i+8,j:j+8] = out3
    return newImagemArray
            

def decompressLosslessDCT(ImagemArray):
    newImagemArray = ImagemArray.copy()
    newImagemArray = newImagemArray.astype(float)
    DCTMatrix = gerarMatrizCoeficentesDCT(8)
    for h in range(1):
        for i in range(0,newImagemArray.shape[0],8):
            for j in range(0,newImagemArray.shape[1],8):
                data = newImagemArray[i:i+8,j:j+8]
                out1 = np.matmul(np.transpose(DCTMatrix),data)
                out2 = np.matmul(out1,DCTMatrix)
                out2 = verifyPixelValue(out2 + 128) 
                newImagemArray[i:i+8,j:j+8] = out2
    return newImagemArray


