# -*- coding: utf-8 -*-
from ia636 import *
from texture import *
import commands
import HTML


class Visualize:
		
	def __init__(self,somart):
		mapa = open(somart.cofilename , 'r')
		mapa = mapa.readlines()

		#16 hexa 8 8 gaussian
		info = mapa[0]
		info = info.split(" ")
		self.Ux, self.Uy = int(info[2]) , int(info[3])  # dimensoes da camada de Kohonen
		coord = [] # lista de coordenadas do neuronio vencedor (BMU) para cada imagem
		del mapa[0]
		
		for linha in mapa:	
			linha = linha.split(" ")
			y = int(linha[0])
			x = int(linha[1])
			coord.append((x,y))
			
		self.coord = coord
		print coord
		
	def listfiles(self,testimages):
		#arquivos = commands.getoutput("ls ../imgs/%s/*.%s") % (type,type)
		arquivos = commands.getoutput("cd .. ; cd imgs ; cd %s ; cd jpg ; ls *.jpg" % (testimages))
		arquivos = arquivos.split("\n")
		return arquivos	
	
	def htmltable(self, somart):
		x,y = self.Ux , self.Uy
		
		# cria a estrutura da tabela
		table = []
		for i in range(x):
			table.append([])
			for j in range(y):
				table[i].append('<br><br><br><br>')

		# preenche a tabela com as imgs
		i = 0
		jpg = self.listfiles(somart.testimages)
		for (x,y) in self.coord:
			table[x][y] += "<img width='250' src='../../imgs/%s/jpg/%s'></img>" % (somart.testimages, jpg[i]) 
			i += 1
			
	    # formata a lista de funcoes/descritores
		desc = []
		for d in somart.hlist: 
			print d
			f = str(d).replace('function','')
			desc.append(f)
		
		# renderiza o HTML da tabela
		htmlcode = """
				<h1>Mapa Auto-Organizavel</h1>
				<ul>
					<li>Neuronios: %dx%d</li>
					<li>Coef. de aprendizado 1: %f</li>
					<li>Coef. de aprendizado 2: %f </li>
					<li>Raio vizinhanca 1: %d</li>
					<li>Raio vizinhanca 2: %d</li>
					<li>Epocas 1: %d</li>
					<li>Epocas 2: %d</li>
				</ul>
			
				<h1>Padroes de textura</h1>
				""" % (somart.kx,somart.ky,somart.c1,somart.c2,somart.r1,somart.r2,somart.e1,somart.e2) 
		if somart.mco == 'yes':
			htmlcode += """
				<h2>Matriz de Co-ocorrencia</h2>
				<ul>
					<li>Distancias: %s</li>
					<li>Angulos: %s</li>
					<li>Descritores: %s</li>
				</ul>
				""" % (str(somart.dlist),str(somart.alist),str(desc))
		
		if somart.fourierspectrum == 'yes':
			htmlcode += """
				<h2>Espectro de Fourier</h2>
				<ul>
					<li>Raios: %s</li>
					<li>Angulos: %s</li>
					<li>Threshold simples: %s</li>
				</ul>
			""" % (str(somart.rlist),str(somart.aflist),str(somart.tsimple))
		
		htmlcode += HTML.table(table)
		outfile = open(somart.htmfilename , "w")
		outfile.write(htmlcode)


	def pgmgrid():
		""" cria uma imagem pgm representando a camada de saída do mapa de Kohonen
			mas não trata o caso de um neurônio mapear mais de uma imagem
		"""
		imgs = [] # lista de todas as imagens
		saida = zeros([Ux*M,Uy*N])    
		arquivos = commands.getoutput("ls ../imgs/*.pgm")

		arquivos = arquivos.split("\n")
		for arq in arquivos:
			img = iaread(arq)
			img = iaresize(img, [M,N])
			imgs.append(img)

		print imgs[0].shape

		mapa = open('../data/mapa.txt' , 'r')
		mapa = mapa.readlines()
		del mapa[0] # primeira linha nao interessa

		#tratar o caso de duas imagens na mesma coordenada!


		id = 0
		
		for linha in mapa:	
			x = int(linha[0])
			y = int(linha[2])
			for i in range(0,M):
				for j in range(0,N):
					img = imgs[id] 
					saida[M*x+i,N*y+j] = img[i][j] 
			id += 1
			
		iawrite(saida,"grade.pgm")	
			

