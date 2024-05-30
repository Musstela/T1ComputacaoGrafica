from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
from Poligonos import *

class Instancia:   
    def __init__(self):
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (1,1,1)
        self.rotacao:float = 0.0
        self.vetor = Ponto(0,0.5)
        self.pivot:Ponto
        self.desenhaModelo:None
        self.modelo:Polygon
        self.t = 0.0
        self.ordem = 0
        self.podeDesenhar = True
    
    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            pass 
        else:
            print ("Rotacao:", self.rotacao)

    """ Define o modelo a ser usada para a desenhar """
    def setModelo(self, func):
        self.modelo = func

    def Desenha(self):
        glLoadIdentity()
        glPushMatrix()
        
        self.posicao.x += self.vetor.x
        self.posicao.y += self.vetor.y

        glTranslatef(self.posicao.x, self.posicao.y, 0)
        if(self.desenhaModelo != None):
            self.desenhaModelo(self.ordem,self.modelo)
        glPopMatrix()