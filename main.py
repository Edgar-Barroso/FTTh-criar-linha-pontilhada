import os
import shutil
import sys
from caminho import Caminho
from geopy.distance import distance
import math
import simplekml


file = 'Cabos.kmz'
largura = 5



lista_coordenadas_dos_pontos = []
kml = simplekml.Kml()

caminhos = Caminho.extrair_caminhos(f'{file}')
for n1, caminho in enumerate(caminhos):

    for n2, coordenada in enumerate(caminho.coordenadas):
        if n2 != 0:
            coord1 = caminho.coordenadas[n2 - 1]
            coord2 = coordenada
            distancia = distance(coord1, coord2).meters
            if distancia % largura != 0:
                distancia += 1
            lat1 = float(coord1[0])
            lat2 = float(coord2[0])
            long1 = float(coord1[1])
            long2 = float(coord2[1])
            hipotenusa = distance((lat1, long1), (lat2, long2)).meters
            catetoad = distance((lat1, long2), (lat1, long1)).meters
            catetoop = math.sqrt((hipotenusa ** 2) - (catetoad ** 2))
            mov = 0
            div = int(distancia / largura)
            for c in range(0, div):
                mov = c * largura
                tang = catetoop / catetoad
                mov_lat = mov * catetoop / hipotenusa
                mov_long = mov * catetoad / hipotenusa
                y = mov_lat * 0.000008997
                x = mov_long * 0.000008997
                lat = 0
                long = 0
                if lat1 >= lat2 and long1 <= long2:
                    lat = lat1 - y
                    long = long1 + x
                elif lat1 >= lat2 and long1 >= long2:
                    lat = lat1 - y
                    long = long1 - x
                elif lat1 <= lat2 and long1 <= long2:
                    lat = lat1 + y
                    long = long1 + x
                elif lat1 <= lat2 and long1 >= long2:
                    lat = lat1 + y
                    long = long1 - x
                lista_coordenadas_dos_pontos.append([float(long), float(lat)])
for n, ponto in enumerate(lista_coordenadas_dos_pontos):
    if n % 3 == 0 and n >= 3:
        pontilhado = kml.newlinestring(coords=[ponto, lista_coordenadas_dos_pontos[n-2]])
        pontilhado.style.linestyle.color = 'ff0000ff'
        pontilhado.style.linestyle.width = 2
kml.save(f'pontilhado_{file}')
shutil.rmtree(f'{os.getcwd()}\TEMP')
