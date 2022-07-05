from PIL import Image
import numpy as np
import cv2
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from funcoesBasicas import FixImageRange, openImage, \
    gerarMatrizCoeficentesDCT, gerarMatrizQuantizacao2, reshapeImage, calculateOutMatrix,decompressImage, losslessDCT, decompressLosslessDCT

import os
 
 #Abro a imagem
img = openImage(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste9.png')

#Matriz de teste 1
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

#Matriz de teste 2
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

#Matriz de teste 3
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

#Reshape na imagem para multiplo de 8x8
newImage = reshapeImage(np.array(img))
newImage2 = Image.fromarray(newImage)
cv2.imwrite(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste9.jpg', newImage)
#Salvo imagem e a mostro na tela para comparação
newImage2.show()
#newImage2.save(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste9.jpg')
#newImage = np.array(exampleImage)

#Calculo compressão DCT
outMatrix = calculateOutMatrix(newImage,50)

print("Compressed using lossy")

#Descomprimo imagem DCT
decompressedImage = decompressImage(outMatrix,50)
print("===================================================")

#Exibo imagem descomprimida
print("Lossy image decompressed")
imdecompressed = Image.fromarray(decompressedImage.astype(np.uint8))
imdecompressed.show()

#Comprimo usando lossless DCT
print("===================================================")
print("Compressed using lossless")
compressedImage = losslessDCT(newImage)


#Descomrimo usando Lossless DCT
decompressedImageLossless = decompressLosslessDCT(compressedImage)
print("===================================================")
print("Decompressed lossless")
#Crio Imagem usando Pil e mostro na tela
imdecompressedLossless = Image.fromarray(decompressedImageLossless.astype(np.uint8))
imdecompressedLossless.show()

cv2.imwrite('imagemLossLessDaCertoPF.jpg',decompressedImageLossless)
cv2.imwrite('imagemDCT.jpg',decompressedImage)

file_size0 = os.path.getsize(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\data\images\imagemteste9.jpg')
file_size1 = os.path.getsize(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\src\imagemLossLessDaCertoPF.jpg')
file_size2 = os.path.getsize(r'C:\Users\Nathan\Documents\EA979 - 2022\EA979_ComputacaoGrafica_2022\src\imagemDCT.jpg')

print("File Size Not Compressed is :", file_size0, "bytes")
print("File Size Compressed is :", file_size2, "bytes")
print("File Size Lossless Compressed is :", file_size1, "bytes")

#Verifico tamanho em bytes das imagens(DCT, LDCT e Original)
img_file = BytesIO()
imdecompressed.save(img_file, 'jpeg')
img_file_size_jpeg = img_file.tell()
print(f'size = {img_file_size_jpeg}')

img_file = BytesIO()
imdecompressedLossless.save(img_file, 'jpeg')
img_file_size_jpeg = img_file.tell()
print(f'size = {img_file_size_jpeg}')

img_file = BytesIO()
newImage3 = Image.fromarray(newImage)
newImage3.save(img_file, 'jpeg')
img_file_size_jpeg = img_file.tell()
print(f'size = {img_file_size_jpeg}')

#Obtenho imagens da diferença e as exibo para ver quais pontos ficaram diferentes
difference1 = abs(newImage - decompressedImage)
difference2 = abs(newImage - decompressedImageLossless)
imDifference1 = Image.fromarray(difference1.astype(np.uint8))
imDifference1.show()

imDifference2 = Image.fromarray(difference2.astype(np.uint8))
imDifference2.show()

#Faço uma somatoria dos pontos onde a diferença foi maior que 10 nos valores de pixel para saber o quanto diferimos da imagem original
thresholdImage1 = difference1 > 10
thresholdImage2 = difference2 > 10

sumOfPixels1 = np.sum(thresholdImage1)
sumOfPixels2 = np.sum(thresholdImage2)

print(f'Diferença entre imagem original e DCT: {sumOfPixels1} \nDiferença entre imagem original e Lossless DCT: {sumOfPixels2}')
