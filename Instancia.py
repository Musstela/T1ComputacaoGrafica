from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *

""" Classe Instancia """
class Instancia:   
    def __init__(self):
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (1,1,1)
        self.rotacao:float = 0.0
        self.vetor = Ponto(0,0.01)
        self.pivot:Ponto
        self.modelo = None
        self.t = 0.0
    
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

        print(self.rotacao)
        glTranslatef(self.posicao.x, self.posicao.y, 0)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        self.modelo()
        glPopMatrix()