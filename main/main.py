# -*- coding: utf-8 -*-

# supporting modules for feature extraction and output visualization
from texture import * 	# texture.py
from visualize import * # visualize.py

import os
import random
import time

class somart:
	
	def __init__(self):
		self.testimages = "gravuras" # image test set name
		self.escala = 400 # standard minimal width/height of jpeg images 	
	
		# paths to the images, data files and supporting libraries 
		self.ppath = "../imgs/%s/pgm/" % (self.testimages)
		self.jpath = "../imgs/%s/jpg/" % (self.testimages)
		self.dpath = "../data/%s/" % (self.testimages)
		self.spath = "../lib/"
		
                # (Co-occurence matrixes parameters)
		# distance, angle, and Haralick descriptors parameters
		self.mco = 'yes' # "yes" means that co-occurence matrixes are enabled in this extraction, set "no" to disable it 
		self.dlist = [3] # interpixels distance
		self.alist = [0,90] # angles - position operators 
		self.hlist = [correlacao,segundomomentoangular,contraste,homogeneidade]
		
                # (Fourier Spectrum Analysis parameters)
		# radius, angles and threshold parameters
		self.fourierspectrum = 'yes' # "yes" se espec. de fourier é usado "não" para não usar 
		self.frings = "yes" # "yes" para usar máscara em forma de anel 
		self.fsectors = "no" # "yes" para usar máscara em forma de setor (pouco eficiente)
		self.tsimple = 150 # valor do limiar/threshold sob o espectro de fourier
		self.textinction = 180
		self.rlist = [100,150,200] # lista com os raios dos anéis
		self.aflist = [30,60,90,120,150,180] # lista com os angulos dos setores
		
		# (Self Organizing Maps parameters)
		self.kx, self.ky = 8,8 # map dimension
		self.c1, self.c2 = 0.05, 0.02 # learning coefficients
		self.e1, self.e2 = 10000, 1000000 # number of epoch
		self.r1, self.r2 = (self.kx*self.ky)/4, 2 # neighborhood initial radius
		
		# file names are based on current time		
		t = time.localtime()
		hour = t[3]
		minute = t[4]
		day = t[2]
		month = t[1]
		filename = "%s%s-%s_%s-%s" % (self.dpath, day, month, hour, minute)
		filename = "%s28-6_1-10" % (self.dpath)
		
		# names of output files:
		self.infilename = filename+".in"
		self.outfilename = filename+".map"
		self.cofilename = filename+".co"
		self.ufilename = filename+".ps"
		self.htmfilename = filename+".htm"
		
		# convert all images to pgm and scales it to value of self.escala
		os.system("sh jpegtopgm.sh %s %s" % (self.testimages, self.escala))
		
		# extracts the texture features
		featureswrite(self)
		
		# SOM training
		self.training()
		
		# visualize the result in a HTML file
		V = Visualize(self)
		V.htmltable(self)
		
	def training(self):
		
		print "### SOM Initialization"
		init = "%s./randinit -xdim %s -ydim %s -din %s -cout %s -topol rect -neigh gaussian" % (self.spath, self.kx, self.ky, self.infilename, self.outfilename)
		os.system(init)
		
		print "### First phase - ordenation" 
		### coeficiente de aprendizado alto, vizinhança com raio grande
		first = "%s./vsom -din %s -cin %s -cout %s -rlen %d -alpha %f -radius %d" % (self.spath, self.infilename, self.outfilename, self.outfilename, self.e1, self.c1, self.r1)
		os.system(first)
		
		print "### Second phase - convergence"
		### coeficiente de aprendizado menor, maior número de épocas
		second = "%s./vsom -din %s -cin %s -cout %s	-rlen %d -alpha %f -radius %d" % (self.spath, self.infilename, self.outfilename, self.outfilename, self.e2, self.c2, self.r2)
		os.system(second)
		
		print "### Map Calibration"
		cal = "%s./vcal -din %s -cin %s -cout %s" % (self.spath, self.infilename, self.outfilename, self.outfilename)
		os.system(cal)
		
		print "### Map Avaliation"
		qerror = "%s./qerror -din %s -cin %s" % (self.spath, self.infilename, self.outfilename)
		os.system(qerror)
		
		print "### Coordinates for each winning neuron for each image:"
		coord = "%s./visual -din %s -cin %s -dout %s" % (self.spath, self.infilename, self.outfilename, self.cofilename)
		os.system(coord)
		
		# u-matrix:
		umat = "%s./umat -cin %s -median 1 > %s" % (self.spath, self.outfilename, self.ufilename)
		os.system(umat)


# somart class instance
somart()
