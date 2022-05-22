import math
import numpy as np



#Nao utilizar(Com erro)
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


#Nao utilizarrrrr
def gerarMatrizQuantizacao(fator):
    Q = []
    for i in range(8):
        Q.append(np.zeros(8))
    for i in range(8):
        for j in range(8):
            Q[i][j] = 1 + (1+i+j)*fator
    return Q

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
    else:
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


M = [
	[26,-5,-5,-5,-5,-5,-5,8],
	[64,52,8,26,26,26,8,-18],
	[126,70,26,26,52,26,-5,-5],
	[111,52,8,52,52,38,-5,-5],
	[52,26,8,38,38,21,8,8],
	[0,8,-5,8,26,52,70,26],
	[-5,-23,-18,21,8,8,52,38],
	[-18,8,-5,-5,-5,8,26,8]
]

DctMatrix = gerarMatrizCoeficentesDCT(8)
DctMatrixInverse = np.linalg.inv(DctMatrix)

outTemp = np.matmul(DctMatrix,M)

out = np.matmul(outTemp,DctMatrixInverse)

quantization = gerarMatrizQuantizacao2(50)


outFinal = DivideByQuantizationMatrix(out,quantization)

for linha in outFinal:
    print(linha)