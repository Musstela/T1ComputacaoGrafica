import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from Instancia import *

# Modelos de Objetos
MeiaSeta = Polygon()
Player = Polygon()
Tiro = Polygon()

# Pontos de controle de uma curva Bezier
Curva1 = []

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
Personagens = []
Vidas = 3
Municao = 10

nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ****************************************************************
def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0,0,1)
    glTranslatef(-P.x, -P.y, -P.z)


# ***********************************************************************************
def reshape(w,h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    #glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def DesenhaPixel(entidade):
    glPushMatrix()
    glRotatef(-90 + Personagens[0].rotacao,0,0,1)
    glTranslatef(Personagens[0].pivot.x,Personagens[0].pivot.y,0)
    for Vertice,indexCor in entidade.Vertices:
        glBegin(GL_QUADS)
        cor = ListaCor.pegaCor(indexCor)
        glColor3f(cor[0],cor[1],cor[2])
        glVertex2f(Vertice.x, Vertice.y)
        glVertex2f(Vertice.x + 1, Vertice.y)
        glVertex2f(Vertice.x + 1, Vertice. y+1)
        glVertex2f(Vertice.x, Vertice.y + 1)
        glEnd()
    glPopMatrix()

def DesenhaPlayerUI(entidade):
    glRotatef(-90,0,0,1)
    for Vertice,indexCor in entidade.Vertices:
        glBegin(GL_QUADS)
        cor = ListaCor.pegaCor(indexCor)
        glColor3f(cor[0],cor[1],cor[2])
        glVertex2f(Vertice.x, Vertice.y)
        glVertex2f(Vertice.x + 1, Vertice.y)
        glVertex2f(Vertice.x + 1, Vertice. y+1)
        glVertex2f(Vertice.x, Vertice.y + 1)
        glEnd()

def DesenhaPlayer():
    DesenhaPixel(Player)
    glPushMatrix()
    glScaled(0.2, 0.2, 1)
    glPopMatrix()

def DesenhaTiro():
    Tiro.DesenhaPixel()

# **************************************************************

def DesenhaNumero(x, y, number):
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(x, y, 0.0)

    glBegin(GL_LINES)
    if number == 0:
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, -0.5)
    elif number == 1:
        glVertex2f(0.0, -0.5)
        glVertex2f(0.0, 0.5)
    elif number == 2:
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, -0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
    elif number == 3:
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(-0.5, -0.5)
    elif number == 4:
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.0, 0.5)
        glVertex2f(0.0, -0.5)
    elif number == 5:
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(-0.5, -0.5)
    elif number == 6:
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(-0.5, 0.0)
    elif number == 7:
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, -0.5)
    elif number == 8:
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, -0.5)
    if number == 9:
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(-0.5, -0.5)
    elif number == 10:
        # Desenha o 1
        glVertex2f(0.0, -0.5)
        glVertex2f(0.0, 0.5)
        # Desenha o 0
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, -0.5)
    glEnd()

    glPopMatrix()


def DesenhaUI():
    global Min, Max

    Meio = Ponto()

    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    AlturaUi = ((Max.y + abs(Min.y)) / 8 ) + (Min.y)

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)

    #barra superior da UI
    glVertex2f(Min.x, AlturaUi)
    glVertex2f(Max.x, AlturaUi)
    glEnd()

    glColor3f(255, 255, 255)
    glBegin(GL_QUADS)
    glVertex2f(Max.x, Min.y)
    glVertex2f(Max.x, AlturaUi)
    glVertex2f(Min.x, AlturaUi)
    glVertex2f(Min.x, Min.y)
    glEnd()

    UIReferenceY = Min.y + abs(AlturaUi/5)
    UIReferenceX = (Max.x + UIReferenceY) + Min.x

    glLoadIdentity()
    glPushMatrix()
    glTranslatef(UIReferenceX,UIReferenceY,0)
    glScaled(0.2, 0.2, 1)
    DesenhaPlayerUI(Player)
    DesenhaNumero(UIReferenceX + (Max.x / 4) , UIReferenceY - 0.6 , Vidas)
    glPopMatrix()


# ***********************************************************************************
def DesenhaPersonagens():
    for I in Personagens:
        I.Desenha()

def animate():
    global AccumDeltaT
    global oldTime
    global nFrames 
    global TempoTotal

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        display()
        glutPostRedisplay()

# ***********************************************************************************
def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLineWidth(3)
    glColor3f(1,1,1) # R, G, B  [0..1]
    DesenhaUI()
    DesenhaPersonagens()
    
    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. 
# Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
# Forca o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        Personagens[0].vetor.y = 0.01
        Personagens[0].rotacao = 0
        Personagens[0].pivot = Ponto(-4,-8,0)
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        Personagens[0].vetor.y = -0.01
        Personagens[0].rotacao = 180
        #Personagens[0].pivot = Ponto(1.5,-0.5,0)
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        Personagens[0].vetor.x = -0.01
        Personagens[0].rotacao += 30
    if a_keys == GLUT_KEY_RIGHT:
        Personagens[0].vetor.x = 0.01
        Personagens[0].rotacao -= 30

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do 
    # Personagens definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return

def CarregaModelos():
    global Player, Tiro

    
    Player.LePontosDeArquivo("Personagens\Player.txt")
    Tiro.LePontosDeArquivo("Personagens\Tiro.txt")

def CriaInstancias():
    global Personagens

    Personagens.append(Instancia())
    Personagens[0].modelo = DesenhaPlayer
    Personagens[0].posicao = Ponto(0,0)
    Personagens[0].escala = Ponto (0.2,0.2,1)
    Personagens[0].pivot = Ponto(-4,-8,0)

def init():
    global Min, Max
    glClearColor(0, 0, 0, 1)

    CarregaModelos()
    CriaInstancias()

    d:float = 20
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1080, 920)
glutInitWindowPosition(850, 75)
wind = glutCreateWindow("Trabalho 1")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass
