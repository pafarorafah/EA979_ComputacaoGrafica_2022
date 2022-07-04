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
  
 Fórmula da DCT em 1D (Equação 1):
  $$F(i) = {1  \over \sqrt{2N}} C(i) \sum_{x=0}^{N-1} f(x)cos({(2x + 1)i \pi \over 2 N}) $$
 
 - Se u = 0, $\ C(u) = {1  \over \sqrt{2N}}  $
 - Se u > 0, $\ C(u) = 1  $
  
 Fórmula da DCT em 2D (Equação 2):
  $$F(i,j) = {1  \over \sqrt{2N}} C(i)C(j) \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} f(x,y)cos({(2x + 1)i \pi \over 2 N})cos({(2y + 1)j \pi \over 2 N}) $$
 
 - Se u = 0, $\ C(u) = {1  \over \sqrt{2N}}  $
 - Se u > 0, $\ C(u) = 1  $
  
  
  
### Plano de Trabalho
> * Etapa 1 (2 semanas): Estudo da técnica DCT com perda. 
> * Etapa 2 (3 semanas): Tentar Implementar um algoritmo inicial de compressão de imagem com perda utilizando DCT.
> * Etapa 3 (2 semanas): Estudo de técnicas de compressão de imagem sem perda de informação(LDCT).
> * Etapa 4 (3 semanas): Tentar implementar um algoritmo inicial de compressão de imagem sem perda(LDCT).
> * Etapa 5 (finalizar): Ter os algoritmos em mãos e compará-los. Analisar quando é vantajoso usar um ou outro. Escrever o relatório final.
  
### Referências Bibliográficas
> http://www.dpi.inpe.br/~carlos/Academicos/Cursos/Pdi/SemPerdas.htm
> http://computacaografica.ic.uff.br/transparenciasvol2cap8.pdf
> https://www.spiedigitallibrary.org/conference-proceedings-of-spie/2419/0000/DCT-based-scheme-for-lossless-image-compression/10.1117/12.206386.full?SSO=1
  
  
  
