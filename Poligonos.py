# ************************************************
#   Poligonos.py
#   Define a classe Polygon
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
from ListaDeCoresRGB import *
import copy

class Polygon:

    def __init__(self):
        self.Vertices = [] # atributo do objeto

    def getNVertices(self):
        return len(self.Vertices)
    
    def insereVertice(self, x: float, y:float, z: float, cor: int):
        self.Vertices += [(Ponto(x,y,z),(cor))]

    #def insereVertice(self, P: Ponto):
    #    self.Vertices += [Ponto(P.x,P.y,P.z)]

    def getVertice(self, i):
        temp = copy.deepcopy(self.Vertices[i])
        return temp
        #return self.Vertices[i]
    
    def desenhaPoligono(self):
        #print ("Desenha Poligono - Tamanho:", len(self.Vertices))
        glBegin(GL_LINE_LOOP)
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd()

    def desenhaVertices(self):
        glBegin(GL_POINTS)
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd()

    def desenhaPixel(self):
        for Vertice,indexCor in self.Vertices:
            glBegin(GL_QUADS)
            cor = ListaCor.pegaCor(indexCor)
            glColor3f(cor[0],cor[1],cor[2])
            glVertex2f(Vertice.x, Vertice.y)
            glVertex2f(Vertice.x + 1, Vertice.y)
            glVertex2f(Vertice.x + 1, Vertice. y+1)
            glVertex2f(Vertice.x, Vertice.y + 1)
            glEnd()

    def imprimeVertices(self):
        for x in self.Vertices:
            x.imprime()

    def getLimits(self):
        Min = copy.deepcopy(self.Vertices[0][0])
        Max = copy.deepcopy(self.Vertices[0][0])
        
        for Vertice,Cor in self.Vertices:
            if Vertice.x > Max.x:
                Max.x = Vertice.x
            if Vertice.y > Max.y:
                Max.y = Vertice.y
            if Vertice.z > Max.z:
                Max.z = Vertice.z
            if Vertice.x < Min.x:
                Min.x = Vertice.x
            if Vertice.y < Min.y:
                Min.y = Vertice.y
            if Vertice.z < Min.z:
                Min.z = Vertice.z
        #print("getLimits")
        #Min.imprime()
        #Max.imprime()
        return Min, Max
#def setColor()
# ***********************************************************************************
# LePontosDeArquivo(Nome):
#  Realiza a leitura de uam arquivo com as coordenadas do polígono
# ***********************************************************************************
    def LePontosDeArquivo(self, Nome):
        
        Pt = Ponto()
        infile = open(Nome)
        lines = infile.readlines()
        config = lines[0].strip().split()
        configRow = int(config[0])
        configColumn = int(config[1])
        lines.pop(0)

        matriz = [[None for j in range(configRow)] for i in range(configColumn)]

        for index,item in enumerate(lines):
            matriz[index] = item.strip().split() # Separa as palavras na linha
        

        for indexLinha,linha in enumerate(matriz):
            for indexColuna,ponto in enumerate(linha):
                if(int(ponto) != -1): 
                    self.insereVertice(indexLinha,indexColuna,0,int(ponto))

        infile.close()
        
        print("Após leitura do arquivo:")

        return self.getLimits()

    def getAresta(self, n):
        P1 = self.Vertices[n]
        n1 = (n+1) % self.getNVertices()
        P2 = self.Vertices[n1]
        return P1, P2

    def desenhaAresta(self, n):
        glBegin(GL_LINES)
        glVertex3f(self.Vertices[n].x,self.Vertices[n].y,self.Vertices[n].z)
        n1 = (n+1) % self.getNVertices()
        glVertex3f(self.Vertices[n1].x,self.Vertices[n1].y,self.Vertices[n1].z)
        glEnd()

    def alteraVertice(self, i, P):
    #int i, Ponto P)
        self.Vertices[i] = P