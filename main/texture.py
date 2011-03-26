# -*- coding: utf-8 -*-

from math import *
from numpy import *
from ia636 import *
import os
import FFT
import commands

# converter para tamanho apropriado (buscar tamanho real do quadro)

def test_haralick_paper():
	img = array([[0,0,1,1],[0,0,1,1],[0,2,2,2],[2,2,3,3]])
	m = matriz_coocorrencia(img,4,[1],[0])	
	print "matriz de coocorrencia:"
	print m[0]
	print "descritores:" 
 	print descritores(m[0],[contraste,segundomomentoangular,homogeneidade,entropia,correlacao])
 	
 	
def eq_hist(img):
	h = iahistogram(img)
	# histograma acumulado normalizado
	han = cumsum(h) / (1.*product(img.shape))
	# transformação de intensidade baseada no han
	gn = 255 * iaapplylut(img, han)
 	return gn
 	
 	
def matriz_coocorrencia(img,I,D,A):
	M = img.shape[0] # numero de linhas
	N = img.shape[1] # numero de colunas
	C = []	
	
	# normaliza a imagem para I niveis de intensidade
	imgn = ianormalize(img,(0,I-1))
	# arredonda o valor dos pixels
	imgn = (0.5 + imgn).astype(int)
	# equalização de histograma
	#imgn = img
	
	# d é a distancia entre pixels a ser analisada
	for d in D:	
	
		C0, C45, C90 = zeros([I,I]), zeros([I,I]), zeros([I,I])
		total0, total45, total90 = 0, 0, 0
		
		for i in xrange(0,M): # percorre toda a img
			for j in xrange(0,N):
				
				a = imgn[i][j] # elemento em analise
				
				# para 0 e 45 graus, j (coluna) tem prioridade
				# em verificar se não está fora dos limites da imagem
				
				if j-d >= 0:
					b0 = imgn[i][j-d] # 0 graus - esquerda
					C0[a][b0] += 1
					total0 += 1
					
					if i+d <= M-1:
						#print "\nM:"+str(M)+",N:"+str(N)+",i+d="+str(i+d)+",j+d="+str(j+d)
						b45 = imgn[i+d][j-d] # 45 graus - baixo
						C45[a][b45] += 1
						total45 += 1
						
						b90 = imgn[i+d][j] # 90 graus - baixo 
						C90[a][b90] +=1
						total90 += 1
						
				# para 90 graus, faz o calculo mesmo que o componente
				# horizontal esteja fora dos limites da imagem
				
				elif i+d <= M-1:
					b90 = imgn[i+d][j] # 90 graus - baixo 
					C90[a][b90] +=1
					total90 += 1
				
						
				if j+d <= N-1:
					c0 = imgn[i][j+d] # 0 graus - direita						
					C0[a][c0] += 1
					total0 += 1
					
					if i-d >= 0:
						c45 = imgn[i-d][j+d] # 45 graus - cima						
						C45[a][c45] += 1
						total45 += 1
						
						c90 = imgn[i-d][j] # 90 graus - cima 
						C90[a][c90] +=1
						total90 += 1
						
				elif i-d >= 0:
					c90 = imgn[i-d][j] # 90 graus - cima 
					C90[a][c90] +=1
					total90 += 1
							
		# aqui tem-se as matrizes de co-ocorrência
		if 0 in A: C.append(C0/total0)
		if 45 in A: C.append(C45/total45)
		if 90 in A: C.append(C90/total90)
		
	return C

# operações de haralick
def entropia(p,i=None,j=None):
	return p * (math.log(p+0.1))

def contraste(p,i,j):
	return p * ((i-j)**2)

def segundomomentoangular(p,i=None,j=None):
	return p**2

def dissimilaridade(p,i,j):
	return p * (i-j)
	
def homogeneidade(p,i,j):
	return p*(1/(1 + ((i-j)**2)))

def correlacao(matriz,M,N):
	x,y = indices((M,N))
	mx = sum(matriz*x)
	my = sum(matriz*y)	 
	varx = sum(((x - mx)**2) * matriz) # variancia x
	vary = sum(((y - my)**2) * matriz) # variancia y
	dx = sqrt(varx) # desvio padrão x
	dy = sqrt(vary) # desvio padrão y
	return sum((matriz*(x-mx)*(y-my))/((dx*dy)))/M*N
	
	
def descritores(matriz, hl):
	# matriz: matriz de co-ocorrencia
	# hlist: lista de funções descritoras de haralick
	
	M = matriz.shape[0] # numero de linhas
	N = matriz.shape[1] # numero de colunas
	desc = []
	hlist = []
	hlist.extend(hl)
	
	for f in hlist:
		desc.append(0.0) # inicializa todos os descritores como float
	
	# correlacao é uma excessao, pois precisa percorrer
	# a matriz mais de uma vez para ser calculada
	if correlacao in hlist: 
		hlist.remove(correlacao)
		desc[len(hlist)] = correlacao(matriz,M,N)
		
	# o restante das operações pode ser feito simultaneamente
	# percorrendo uma unica vez a matriz
	for i in xrange(0,M): 
		for j in xrange(0,N):
			e = matriz[i][j] # elemento em analise
			for id in range(0,len(hlist)):
				f = hlist[id]
				desc[id] += f(e,i,j) # somatoria para cada função
	
	return [x/(M*N) for x in desc] 		

# retorna só os elementos diferentes de zero em uma imagem
def nonzeroarea(img):
		list = []
		x,y = nonzero(img)
		for i in range(len(x)):
			list.append(img[x[i],y[i]])
		return array(list)
		
def divide4(img):
	M, N = img.shape[0], img.shape[1]
	p1 = iaroi(img,[0,0],[M/2,N/2])
	p2 = iaroi(img,[0,N/2],[M/2,N])
	p3 = iaroi(img,[M/2,0],[M,N/2])
	p4 = iaroi(img,[M/2,N/2],[M,N])
	return [p1,p2,p3,p4]

def espectrofourier(img, libdir, ts, frings, fsectors, raios, angulos):
	M,N = img.shape[0], img.shape[1]
	d = min(M,N) # dimensao menor das imagens
	ci, cj = M/2, N/2 # coordenadas do centro da img
	rmax = d/2 # raio maximo da circ. que cabe na img
	slices = []
	desc = []
	
	F = FFT.fft2d(img)
	Fview = iadftview(F) # passar threshold aqui!
	
	# threshold realizado com dinamica - valores de extinção:
	#iawrite(Fview,'../tmp/fv.pgm')
	#os.system('%s./extinction htop ../tmp/fv.pgm ../tmp/result.pgm' % (libdir)) 
	#Fvd = iaread('../tmp/result.pgm')
	#iashow(Fv)
	
	#Fvd = (Fvd>1)*Fview
	#iawrite(Fv,'../tmp/fv2.pgm')
	
	
	#iashow(dimask)
	#nz = nonzeroarea(dimask)
	#print nz
	#print "soma de tudo = "+str(nz.sum())
	#ts = nz.sum()/nz.shape[0]
	#print ts
	#iashow(Fview)
	# threshold simples:
	#Fv = Fview
	Fv = Fview * (Fview > ts)
	#iashow(Fv)
	#a = raw_input()
	
	# em seguida é cortado o lado direito da imagem do espectro
	if M>N: # se a imagem for mais alta que larga:
		rightside = iaroi(Fv,[abs(ci-rmax),cj],[(ci+rmax-1),N])
		#rightsided = iaroi(Fvd,[abs(ci-rmax),cj],[(ci+rmax-1),N])
	
	elif N>M: # se for mais larga que alta:
		rightside = iaroi(Fv,[0,cj],[M-1,(cj+rmax-1)])
		#rightsided = iaroi(Fvd,[0,cj],[M-1,(cj+rmax-1)])
	
	else: # se for quadrada:
		rightside = iaroi(Fv,[0,cj],[M,N])
		#rightsided = iaroi(Fvd,[0,cj],[M,N])
	
	# carrega uma lista com templates para setores
	for ang in angulos:
			file = "../imgs/templates/%d.pbm" % (ang)
			slices.append(iaread(file))
	
	
	for r in raios:		
		circ = iacircle([d,d],r,[rmax,rmax])
		circ = iaroi(circ,[0,rmax],[d,d]) # recorta lado direito do circulo
		circ2 = iacircle([d,d],50,[rmax,rmax])
		circ2 = iaroi(circ2,[0,rmax],[d,d]) 
		ring = circ-circ2 # diminui circulo maior pelo menor para formar anel
		
		if frings == "yes":
			# quantidade de pixels do anel
			qtd = ring.sum()
			
			# aplica a mascara para o anel inteiro
			rough = rightside*ring 
			#roughd = rightsided*ring
		
			# calcular só p/ valores não-zero
			#nz = nonzeroarea(roughd)
			
			mean = rough.sum()/float(qtd)
			std = sqrt(((rough - mean)**2).sum()/qtd)
			desc += [std,mean]
			#desc += [nz.sum()]
				
		# media e desvio padrão dos setores	
		if fsectors == "yes":
			for slice in slices:
				sector = slice*ring
				qtd = sector.sum()
				area = rightside*sector
				#aread = rightsided*sector
				#nz = nonzeroarea(aread)
				mean = area.sum()/float(qtd)
				std = sqrt(((area - mean)**2).sum()/qtd)
				#
				desc += [std,mean]
				#desc += [nz.sum()]
		
	return desc
		
	

def featureswrite(somart):
	""" 
	parametros da matriz de co-ocorrencia:
	 	D: lista de distancias
	 	A: lista de angulos
	 	H: lista de funções descritoras de haralick
	
	 parametros do espectro de fourier:
		t: threshold para valores de extinção
		R: lista de raios
		AF: lista de angulos (setores)
	"""
	saida = open(somart.infilename , 'w')
	#saida.write('\n') # pula uma linha (escrever dimensao no final)
	listar = "ls %s/*.pgm" % (somart.ppath)
	arquivos = commands.getoutput(listar)
	arquivos = arquivos.split("\n")

	for arq in arquivos:
		desc = []
		img = iaread(arq)
		# equalização de histograma
		#img = eq_hist(img)
		C = []
		feat_dim = 0
		
		if somart.mco == 'yes':
			#imgparts = divide4(img)
			#for part in imgparts:
			
			# dimensão dos vetores
			feat_dim += len(somart.dlist) * len(somart.alist) * len(somart.hlist)
			
			# lista de matrizes de co-ocorrencia
			C += matriz_coocorrencia(img,256, somart.dlist, somart.alist) 
			
			# lista de lista de descritores para cada matriz
			desc = [descritores(c, somart.hlist) for c in C]	
		
		if somart.fourierspectrum == 'yes':
			feat_dim += (len(somart.rlist)*2)
			desc += [espectrofourier(img, somart.spath, somart.tsimple, somart.frings, somart.fsectors, somart.rlist, somart.aflist)]
		
		print desc
		
		# escreve os descritores para cada arquivo
		
		# escreve a primeira linha (dimensao dos atributos)
		if saida.tell() == 0:
			saida.write(str(feat_dim)+"\n")
		
		for l in desc:
			for x in l:
				x=str(x)
				saida.write(x+" ")
	
		if "xilo" in arq: saida.write("X"+" ")
		if "lito" in arq: saida.write("L"+" ")
		if "vangogh" in arq: saida.write("V"+" ")
		if "seurat" in arq: saida.write("S"+" ")
		#saida.write("#"+arq)
		saida.write("\n")
		print "OK - %s" % (arq)		

	saida.close()


#espectrofourier(iaread("../imgs/gravuras/pgm/LW303.pgm"),"../lib/",[150,200],[30,60,90,120])
#test_haralick_paper()
#img = array([[0,0,1,1],[0,0,1,1],[0,2,2,2],[2,2,3,3]])
#descritores(img)

#featureswrite("../imgs/pgm/", "ttt.xtx", [1])	
 
