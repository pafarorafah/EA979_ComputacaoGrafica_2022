# Análise e Implementação de Algoritmos de Compressão de Imagem <h1>
## Analysis and Implementation of Image Compression Algorithms <h1>
  
###  Apresentação 

O presente projeto foi originado no contexto das atividades da disciplina de pós-graduação *EA979A - Introdução a Computação Gráfica e Processamento de Imagens*, oferecida no primeiro semestre de 2022, na Unicamp, sob supervisão da Profa. Dra. Paula Dornhofer Paro Costa, do Departamento de Engenharia de Computação e Automação (DCA) da Faculdade de Engenharia Elétrica e de Computação (FEEC).

> |Nome  | RA | Curso|
> |--|--|--|
> | Rafaella Pafaro  | 205087  | Eng. de Computação|
> | Nathan Batista   | 222852  | Eng. de Computação|

### Descrição do Projeto 
> O objetivo do projeto será estudar e implementar Algoritmos de Compressão de Imagem **com** e **sem** perda de informação e compará-los.
>  - A primeira etapa será reproduzir um código baseado em DCT (Discrete Cosine Transform) lossy.
> - Na segunda etapa iremos implementar o LDCT(Lossless Discrete Cosine Transform) reaproveitando o código escrito para DCT. 
  
### DCT

 > Foi proposto por Nasir Ahmed em 1972. É uma transformação similar à DFT (Discrete Fourier Transform) usando apenas números reais.
 
 > Uma técnica amplamente usada em Processamento de Sinais e Compressão de Imagem, principalmente imagens digitais (implementada em JPEG e HEIF).
  
 > Pode ser usada tanto para compressão com perda quanto sem perda. Para compressão com perda utilizaremos o DCT e uma matriz de quantização para remover as altas frequências do sinal (pouco perceptíveis aos olhos humanos), depois usaremos a entropia para recuperar a imagem. Já no método sem perda utilizaremos também uma modularização delta para explorar correlações entre blocos vizinhos da imagem.
  
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
  
  
  
