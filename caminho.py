import xmltodict
from geopy.distance import distance
from simplekml import *
import zipfile
import math


class Caminho:
    def __init__(self, coordenadas=None):
        self._coordenadas = coordenadas

    @property
    def coordenadas(self):
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor):
        if type(valor) is not list:
            raise ValueError('coordenadas deve ser uma list')
        self._coordenadas = valor

    @classmethod
    def extrair_caminhos(cls, arq_name):
        """
        :param arq: kml a ser tratado
        :return: lista de objetos
        """
        if '.kmz' in arq_name:
            with zipfile.ZipFile(arq_name, 'r') as f:
                f.extract('doc.kml', 'TEMP')
                arq_name = 'TEMP\doc.kml'
        with open(f'{arq_name}', 'r+') as f:
            arq = f.read()
        arq = arq.replace('<Folder>', '').replace('</Folder>', '')
        arq = arq.replace('<Document>', '').replace('</Document>', '')
        lista = []
        arq = xmltodict.parse(arq)
        dicionario = arq['kml']['Placemark']
        for place in dicionario:
            try:
                coordenadas_texto = place['LineString']['coordinates']
                coordenadas_float = []
                for coordenada in coordenadas_texto.split():
                    coordenada = [float(coordenada.split(',')[1]), float(coordenada.split(',')[0])]
                    coordenadas_float.append(coordenada)
                try:
                    nome = place['name']
                except KeyError:
                    nome = ''
                try:
                    descricao = place['description']
                except KeyError:
                    descricao = ''
                try:
                    estilo = place['styleUrl']
                except KeyError:
                    estilo = ''
                pt = Caminho()
                pt.coordenadas = coordenadas_float
                pt.nome = nome
                pt.descricao = descricao
                pt.estilo = estilo
                lista.append(pt)
            except KeyError:
                continue
        return lista

