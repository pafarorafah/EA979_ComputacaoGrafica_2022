from PIL import Image
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from funcoesBasicas import FixImageRange, openImage, \
    gerarMatrizCoeficentesDCT, gerarMatrizQuantizacao2, reshapeImage, calculateOutMatrix,decompressImage, losslessDCT, decompressLosslessDCT

import os
 


img = openImage(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste11.jpg')

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

exampleImage = [
	[52,55,61,66,70,61,64,73],
	[63,59,66,90,109,85,69,72],
	[62,59,68,113,144,104,66,73],
	[63,58,71,122,154,106,70,69],
	[67,61,68,104,126,88,68,70],
	[79,65,60,70,77,68,58,75],
	[85,71,64,59,55,61,65,83],
	[87,79,69,68,65,76,78,94]
]



newImage = reshapeImage(np.array(img))
newImage2 = Image.fromarray(newImage)
newImage2.show()
newImage2.save(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste11.png')

outMatrix = calculateOutMatrix(newImage,50)

print("Compressed using lossy")

decompressedImage = decompressImage(outMatrix,50)
print("===================================================")

print("Lossy image decompressed")
imdecompressed = Image.fromarray(decompressedImage.astype(np.uint8))
imdecompressed.show()


#img_file = BytesIO()
#imdecompressed.save(img_file, 'jpeg')
#img_file_size_jpeg = img_file.tell()
#print(f'size = {img_file_size_jpeg}')

print("===================================================")
print("Compressed using lossless")
compressedImage = losslessDCT(newImage)

decompressedImageLossless = decompressLosslessDCT(compressedImage)
print("===================================================")
print("Decompressed lossless")
imdecompressedLossless = Image.fromarray(decompressedImageLossless.astype(np.uint8))
imdecompressedLossless.show()

shapeImage1 = decompressedImage.shape
print(decompressedImage[shapeImage1[0]-9:shapeImage1[0]-1,shapeImage1[1]-9:shapeImage1[1]-1])

shapeImage1 = decompressedImage.shape
print(newImage[shapeImage1[0]-9:shapeImage1[0]-1,shapeImage1[1]-9:shapeImage1[1]-1])

difference1 = abs(newImage - decompressedImage)
difference2 = abs(newImage - decompressedImageLossless)
imDifference1 = Image.fromarray(difference1.astype(np.uint8))
imDifference1.show()

imDifference2 = Image.fromarray(difference2.astype(np.uint8))
imDifference2.show()

thresholdImage1 = difference1 > 30
thresholdImage2 = difference2 > 30

sumOfPixels1 = np.sum(thresholdImage1)
sumOfPixels2 = np.sum(thresholdImage2)

print(f'Diferença entre imagem original e DCT: {sumOfPixels1} \nDiferença entre imagem original e Lossless DCT: {sumOfPixels2}')


imdecompressed.save(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\ImagensComprimidas\imagemteste11Fator50.png')
imdecompressedLossless.save(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\ImagensComprimidas\imagemteste11Lossless.png')

file_size0 = os.path.getsize(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste11.png')
file_size1 = os.path.getsize(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\ImagensComprimidas\imagemteste11Fator50.png')
file_size2 = os.path.getsize(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\ImagensComprimidas\imagemteste11Lossless.png')

print("File Size Not Compressed is :", file_size0, "bytes")
print("File Size Compressed is :", file_size1, "bytes")
print("File Size Lossless Compressed is :", file_size2, "bytes")
