from PIL import Image
import numpy as np
from funcoesBasicas import gerarMatrizDCT, verCoef, converterParaYCbCr, openImage, \
    gerarMatrizCoeficentesDCT, gerarMatrizQuantizacao2, DivideByQuantizationMatrix

openImage('./data/images/bike.png')


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