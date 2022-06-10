from PIL import Image
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from funcoesBasicas import converterParaYCbCr, openImage, \
    gerarMatrizCoeficentesDCT, gerarMatrizQuantizacao2, reshapeImage, calculateOutMatrix,decompressImage, losslessDCT, decompressLosslessDCT

img = openImage(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste.jpg')

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
'''
DctMatrix = gerarMatrizCoeficentesDCT(8)
DctMatrixInverse = np.linalg.inv(DctMatrix)

outTemp = np.matmul(DctMatrix,M)

out = np.matmul(outTemp,DctMatrixInverse)

quantization = gerarMatrizQuantizacao2(50)

outFinal = DivideByQuantizationMatrix(out,quantization)


'''
outMatrix = calculateOutMatrix(np.array(img),50)

#print("Compressed using lossy")

#for linha in outMatrix:
#    print(linha)

decompressedImage = decompressImage(outMatrix,50)
#print("===================================================")

print("Lossy image decompressed")
imdecompressed = Image.fromarray(decompressedImage.astype(np.uint8))
imdecompressed.show()


#img_file = BytesIO()
#imdecompressed.save(img_file, 'jpeg')
#img_file_size_jpeg = img_file.tell()
#print(f'size = {img_file_size_jpeg}')

#print("===================================================")
#print("Compressed using lossless")
compressedImage = losslessDCT(np.asarray(img))
#for linha in compressedImage:
#	print(linha)

decompressedImageLossless = decompressLosslessDCT(compressedImage)
print("===================================================")
print("Decompressed lossless")
imdecompressedLossless = Image.fromarray(decompressedImageLossless.astype(np.uint8))
imdecompressedLossless.show()
#img_file2 = BytesIO()
#imdecompressedLossless.save(img_file2, 'jpeg')
#img_file_size_jpeg2 = img_file2.tell()
#print(f'size = {img_file_size_jpeg2}')
#for linha in decompressedImageLossless:
#	print(linha)

