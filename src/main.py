from PIL import Image
import numpy as np
from funcoesBasicas import converterParaYCbCr, openImage, \
    gerarMatrizCoeficentesDCT, gerarMatrizQuantizacao2, DivideByQuantizationMatrix, reshapeImage, calculateOutMatrix,decompressImage

#img = openImage('./data/images/bike.png')

#print(img.shape)


M2 = [
	[154,123,123,123,123,123,123,136],
	[192,180,136,154,154,154,135,110],
	[254,198,154,154,180,154,123,123],
	[239,180,136,180,180,166,123,123],
	[180,154,136,167,166,149,136,136],
	[128,136,123,136,154,180,198,154],
	[123,105,110,149,136,136,180,166],
	[110,136,123,123,123,136,154,136]
]

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


outMatrix = calculateOutMatrix(np.array(M2),50)

for linha in outMatrix:
    print(linha)

decompressedImage = decompressImage(outMatrix,50)
print("===================================================")

for linha in decompressedImage:
	print(linha)