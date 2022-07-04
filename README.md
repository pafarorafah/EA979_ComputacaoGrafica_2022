# Análise e Implementação de Algoritmos de Compressão de Imagem <h1>
## Analysis and Implementation of Image Compression Algorithms <h1>
  
###  Apresentação 

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação *EA979A - Introdução a Computação Gráfica e Processamento de Imagens*, oferecida no primeiro semestre de 2022, na Unicamp, sob supervisão da Profa. Dra. Paula Dornhofer Paro Costa, do Departamento de Engenharia de Computação e Automação (DCA) da Faculdade de Engenharia Elétrica e de Computação (FEEC).

> |Nome  | RA | Curso|
> |--|--|--|
> | Rafaella Pafaro  | 205087  | Eng. de Computação|
> | Nathan Batista   | 222852  | Eng. de Computação|

### Descrição do Projeto 
> O Objetivo do projeto será estudar e implementar um algoritmo de compressão de imagem baseado no método JPEG. 
A compressão JPEG é baseada no algoritmo DCT (Discrete Cosine Transform), que por sua vez é uma “simplificação” do DFT (Discrete Fourier Transform) e comumente apresenta uma certa perda de qualidade ao recuperar a imagem comprimida.
> Neste projeto, implementamos duas variações do JPEG:

  > Lossy: Método de compressão mais usado, apresenta uma redução na qualidade da imagem porém o tamanho do arquivo é significativamente reduzido.
  
  > Lossless: Método de compressão em que a imagem é reconstruída sem perdas (ou com perdas muito pequenas).

  
### JPEG

 > JPEG (ou JPG) é um acrónimo para Joint Photographic Experts Group, grupo esse que criou a marca em 1992. É um método de compressão que possibilita um "trade off"  ajustável entre qualidade de imagem e espaço de armazenamento. 
 
 > Essa “perda” de qualidade é calculada, e ocorre nas componentes em que a visão humana peca (luminância e crominância), por isso que caso a imagem seja RGB ela primeiramente é convertida para YCbCr ou YUV.
  
 > Pode ser usada tanto para compressão com perda quanto sem perda. Para compressão com perda utilizaremos o DCT e uma matriz de quantização para remover as altas frequências do sinal (pouco perceptíveis aos olhos humanos), depois usaremos a entropia para recuperar a imagem. Já no método sem perda utilizaremos também uma modularização delta para explorar correlações entre blocos vizinhos da imagem.
  
>  O algoritmo é baseado na técnica Discrete Cosine Transform, proposta por Nasir Ahmed em 1972. Até os dias de hoje, JPEG é o método de compressão mais utilizado para imagens digitais.
  
### DCT
  
> DCT é baseado em DFT (Discrete Fourier Transform) com a única diferença que a parte imaginária é excluída já que estamos trabalhando com sinais reais.
  
 Fórmula DCT 1D (Equação 1):
  $$F(i) = {1  \over \sqrt{2N}} C(i) \sum_{x=0}^{N-1} f(x)cos({(2x + 1)i \pi \over 2 N}) $$
 
 - Se u = 0, $\ C(u) = {1  \over \sqrt{2N}}  $
 - Se u > 0, $\ C(u) = 1  $
  
 Fórmula DCT 2D (Equação 2):
  $$F(i,j) = {1  \over \sqrt{2N}} C(i)C(j) \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} f(x,y)cos({(2x + 1)i \pi \over 2 N})cos({(2y + 1)j \pi \over 2 N}) $$
 
 - Se u = 0, $\ C(u) = {1  \over \sqrt{2N}}  $
 - Se u > 0, $\ C(u) = 1  $
  
  Fórmula DCT 2D inversa (Equação 3):
   $$f(x,y) = {1  \over 2}  \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} C(i)C(j) F(i,j) cos({(2x + 1)i \pi \over 2 N})cos({(2y + 1)j \pi \over 2 N}) $$
  
  Pode ser simplificada como (Equação 4):
   $$f(x,y) = \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} F(i,j) P(i,j) $$
  
> $P(i,j)$ são funções-base, ou primitivas, da DCT:
  
 ![](data/images/DCT-8x8.png)
  
 > $F(i,j)$ corresponde às quantidades de cada função primitiva que devem ser combinadas para obter o bloco original da imagem.
 
  > A DCT é uma função separável, independente na horizontal e na vertical e por isso pode ser feita sequencialmente através do produto matricial (Equação 5) :
  
  $$DCT = C \ x \ B \ x \ C^T $$    
  
  > Onde $B$ é um bloco de 8x8 pixels da imagem original e $C$ é uma matriz de transformação igual a:
  - Se i = 0, $\ C_{i,j} = {1  \over 2\sqrt{2N}}  $
  - Se 0 $\ \leq \$ i $\ \leq \$ 7, $\ C_{i,j} = {1  \over 2}cos({(2j+1)i\pi) \over 16})  $
  
  > $C_{i,j} = $
  
  
			      [ .354 	.354    .354    .354    .354     .354     .354     .354	]
			      [	.490 	.416    .278    .098   -.098    -.278   -.416    -.490	]
			      [	.462 	.191   -.191   -.462    -.462    -.191    .191    .462	]
                          [ .416   -.098   -.490   -.278     .278      .490    .098   -.416	]
		              [ .354   -.354   -.354    .354     .354     -.354   -.354    .354	]
			      [	.278   -.490    .098    .416    -.416     -.098    .490   -.278	]
			      [	.191   -.462    .462   -.191    -.191      .462   -.462    .191	]
			      [	.098   -.278    .416   -.490     .490     -.416    .278   -.098	]
  
  
### Projeto
### Compressão `Lossy`
> Seguimos o diagrama de blocos do processo JPEG básico:

![](data/images/JPEG-Fluxograma%20(2).png)
 
#### 1º Passo
	
>  Em primeiro lugar, toda imagem será dividida em blocos de 8x8 pixels. Esse dimensionamento é padrão e leva em conta a resposta em frequência espacial da visão humana. 

Exemplo usando uma imagem 8x8:

	exampleImage = [
	[52,55,61,66,70,61,64,73],
	[63,59,66,90,109,85,69,72],
	[62,59,68,113,144,104,66,73],
	[63,58,71,122,154,106,70,69],
	[67,61,68,104,126,88,68,70],
	[79,65,60,70,77,68,58,75],
	[85,71,64,59,55,61,65,83],
	[87,79,69,68,65,76,78,94]  ]

  > Vale ressaltar que como o projeto é feito usando somente imagens em preto e branco, não é necessária uma conversão dos formatos de cores. Ao usar imagens coloridas, teríamos um passo a mais para converter RGB em YCrCb ou em YUV, isso porque ambos os formatos descrevem cores usando luminância e crominância, essenciais para montar  matrizes de quantização eficientes.
	
#### 2º Passo	
> Aplicamos as funções DCT (equação 5) aos blocos dimensionados e obtemos os coeficientes da DCT.

Exemplo da imagem após o produto: 
	
	exampleImage_DCT = [
	[-4.14000000e+02 -2.91053867e+01 -6.19412066e+01  2.53321427e+01 
	   5.47500000e+01 -1.97158121e+01 -5.91123019e-01  2.07864440e+00]
	 [ 6.08235265e+00 -2.05871050e+01 -6.16330596e+01  8.01103064e+00 
	   1.15282812e+01 -6.64133590e+00 -6.42294788e+00  6.77807822e+00]
	 [-4.60903401e+01  7.95526804e+00  7.67266594e+01 -2.55941405e+01 
	  -2.96558331e+01  1.01388300e+01  6.38908730e+00 -4.77392934e+00]
	 [-4.89143283e+01  1.17702984e+01  3.43050762e+01 -1.42332214e+01 
	  -9.86124516e+00  6.19130180e+00  1.33550518e+00  1.49985441e+00]
	 [ 1.07500000e+01 -7.63378050e+00 -1.24519763e+01 -2.04424794e+00 
	  -5.00000000e-01  1.36592280e+00 -4.58375233e+00  1.51845335e+00]
	 [-9.64192346e+00  1.40699984e+00  3.41195403e+00 -3.29397958e+00 
	  -4.70616919e-01  4.15201877e-01  1.81186287e+00 -3.93915155e-01]
	 [-2.82719809e+00 -1.22845247e+00  1.38908730e+00  7.62891029e-02
	   9.18730157e-01 -3.51496643e+00  1.77334060e+00 -2.77443728e+00]
	 [-1.24570617e+00 -7.07203158e-01 -4.86865699e-01 -2.69445053e+00
	  -8.99835242e-02 -3.95823612e-01 -9.10250518e-01  4.05124460e-01] ]

> Uma característica desse processo é agrupar as baixas frequências no canto superior esquerdo da matriz, enquanto as altas frequências ocuparão as outras posições crescendo conforme deslocamos para baixo e para direita. Sendo a posição (i = 7,  j = 7) a maior frequência representada.

#### 3º Passo		
> A partir deste passo é que de fato ocorre o processo de compressão. O JPEG utiliza matrizes de compressão padrões que irão dividir cada elemento da matriz exampleImage_DCT. Estes coeficientes foram obtidos experimentalmente, e levam em conta a resposta visual em frequência espacial para detalhes de luminância e crominância. 
	
A quantizadora mais comum é de fator 50:
	
	quant = [
	[ 16  11  10  16  24  40  51  61]
	 [ 12  12  14  19  26  58  60  55]
	 [ 14  13  16  24  40  57  69  56]
	 [ 14  17  22  29  51  87  80  62]
	 [ 18  22  37  56  68 109 103  77]
	 [ 24  35  55  64  81 104 113  92]
	 [ 49  64  78  87 103 121 120 101]
	 [ 72  92  95  98 112 100 103  99]]

Observe que as posições onde se encontram as  frequências altas serão divididas por denominadores maiores do que a das frequências baixas, resultando em:

	exampleImage_DCT_quant = [
	[-26.  -3.  -6.   2.   2.  -0.  -0.   0.]
	 [  1.  -2.  -4.   0.   0.  -0.  -0.   0.]
	 [ -3.   1.   5.  -1.  -1.   0.   0.  -0.]
	 [ -3.   1.   2.  -0.  -0.   0.   0.   0.]
	 [  1.  -0.  -0.  -0.  -0.   0.  -0.   0.]
	 [ -0.   0.   0.  -0.  -0.   0.   0.  -0.]
	 [ -0.  -0.   0.   0.   0.  -0.   0.  -0.]
	 [ -0.  -0.  -0.  -0.  -0.  -0.  -0.   0.] ]
> Vemos que a maior parte dos coeficientes resultou em zero e restaram apenas alguns coeficientes de baixa frequência concentrados no canto superior esquerdo.

> A partir daqui, entraria o processo de codificação responsável por “abstrair” os zeros obtidos e de fato compactar a imagem. Porém, o projeto aborda somente até a etapa de quantização. 

#### 4º Passo
>Finalmente, supondo que a imagem tenha passado pelo processo de codificação e decodificação, para restaurar a matriz devemos fazer o passo a passo inverso.

Obteremos a seguinte matriz resultante:
	
	exampleImage_final= [
	[ 65  65  64  63  65  70  73  75]
	 [ 55  55  68  89  97  86  74  69]
	 [ 52  49  75 121 135 106  76  67]
	 [ 64  50  74 129 146 109  75  70]
	 [ 79  54  62 105 119  90  67  70]
	 [ 84  58  52  72  81  67  61  70]
	 [ 85  69  58  59  63  63  68  77]
	 [ 86  80  71  63  64  72  81  87] ]
	
> Observe que obtivemos resultados relativamente próximos se comparados com os da matriz original.

### Compressão `Lossless`
	
> A segunda parte do projeto, consiste em implementar um algoritmo “Lossless” mas que ainda utilize a DCT (como o JPEG). Veremos ao longo do projeto que o método `não é absolutamente sem perdas`, mas recupera a imagem com uma qualidade melhor.
	
O novo diagrama de blocos para o processo será:

![](data/images/JPEG-Fluxograma%20(3).png)

> Note que a única mudança é a troca da matriz de quantização por uma “máscara”. 

Essa nova matriz consistem em:
	
	mask = [
	 [ 1   1   1   1    0    0    0    0 ]
	 [ 1   1   1   0    0    0    0    0 ]
	 [ 1   1   0   0    0    0    0    0 ]
	 [ 1   0   0   0    0    0    0    0 ]
	 [ 0   0   0   0    0    0    0    0 ]
	 [ 0   0   0   0    0    0    0    0 ]
	 [ 0   0   0   0    0    0    0    0 ]
	 [ 0   0   0   0    0    0    0    0 ] ]

>Vemos aqui que as altas frequências continuam sendo zeradas, porém, as baixas frequências não foram divididas por nenhum parâmetro e apresentaram seu valor “verdadeiro”.

Por comparação, usamos o mesmo exemplo feito no método lossy e obtemos a matriz final igual a:
	
	exampleImage_final_lossless = [
	[ 51  57  58  66  71  61  63  72]
	 [ 61  60  65  91 107  84  68  73]
	 [ 63  56  67 115 142 104  68  70]
	 [ 63  56  71 122 151 109  67  70]
	 [ 67  60  68 103 124  92  63  72]
	 [ 77  65  60  69  78  65  59  74] 
	 [ 85  72  62  56  58  59  66  82]
	 [ 87  76  72  66  66  72  81  92]]

> É notável que a perda de informações foi menor, porém ao comparar o tamanho do armazenamento, o método Lossy é mais vantajoso.

### Referências Bibliográficas
> http://www.dpi.inpe.br/~carlos/Academicos/Cursos/Pdi/SemPerdas.htm

> http://computacaografica.ic.uff.br/transparenciasvol2cap8.pdf

> https://www.spiedigitallibrary.org/conference-proceedings-of-spie/2419/0000/DCT-based-scheme-for-lossless-image-compression/10.1117/12.206386.full?SSO=1

> http://pi.math.cornell.edu/~web6140/TopTenAlgorithms/JPEG.html

> https://www.lcs.poli.usp.br/~gstolfi/PPT/APTV0616.pdf

> https://www.researchgate.net/publication/323771460_Lossless_Image_Compression_using_Discrete_Cosine_Transform_DCT

> https://www.ripublication.com/ijaer17/ijaerv12n23_121.pdf

