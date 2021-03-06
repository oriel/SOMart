#!/bin/bash
# exemplo: sh jpegtopgm.sh 400 gravuras

IFS_ATUAL=$IFS
IFS=$( echo -en "\n\b" )

dim=$1
conj=$2
dirjpg="../imgs/$conj/jpg/"
dirpgm="../pgm/"

cd $dirjpg
for jpg in *.jpg
    
    do
	
    # tratamento para o nome do arquivo .pgm:
    pgm=`echo $jpg | cut -d. -f1`
    pgm=$pgm".pgm"
    
    # identifica a proporção da imagem:
    width=`identify -format '%w' $jpg`
    height=`identify -format '%h' $jpg`
    
     # se a img é mais comprida que alta:
     if [ $width -gt $height ]
     	then # o redimensionamento usa a altura como base:
     		convert $jpg -colorspace Gray -resize x$dim temp.jpg
     	else # se não, usa a largura:
     		convert $jpg -colorspace Gray -scale $dim temp.jpg
     fi	
	
	jpegtopnm temp.jpg > $dirpgm$pgm
    rm temp.jpg    
	done

IFS=$IFS_ATUAL
