import time
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Poligonos import *
from Instancia import *
#from QuadTree import *

# Modelos de Objetos
Player = Polygon("Personagens\Player.txt")
TiroPlayer = Polygon("Personagens\TiroPlayer.txt")
TiroInimigo = Polygon("Personagens\TiroInimigo.txt")
ListaDeModelos = []

# Pontos de controle de uma curva Bezier
Curva1 = []

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
Personagens = []
TirosPlayer = []
TirosInimigos = []
TotalTiro = 0
PodeAtirar = True
TempoParaAtirar = 90
Municao = 10
TempoTiroInimigo = 0
Vidas = 3
NumeroInicialDeInimigos = 0
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

def DesenhaBoundingBox(points):
    glBegin(GL_LINE_LOOP)
    glColor3f(255,255,255)
    glVertex2f(*points[0])  # Top left
    glVertex2f(*points[1])  # Top right
    glVertex2f(*points[3])  # Bottom right
    glVertex2f(*points[2])  # Bottom left
    glEnd()

def DesenhaVetor(modelo):
    boundingBox = modelo.BoundingBox
    meioX = (boundingBox[3][0]) / 2
    meioY = (boundingBox[3][1]) / 2
    glBegin(GL_LINES) 
    glColor3f(50,255,50)
    glVertex2f(meioX,meioY)
    glVertex2f(meioX - 10, meioY)
    glEnd()

def DesenhaPixel(instancia,modelo):
    if(instancia.podeDesenhar == True):    
        glPushMatrix()
        glRotatef(-90 + instancia.rotacao,0,0,1)
        glTranslatef(instancia.pivot.x,instancia.pivot.y,0)
        #DesenhaBoundingBox(modelo.BoundingBox)
        #DesenhaVetor(modelo)
        for Vertice,indexCor in modelo.Vertices:
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

def DesenhaPersonagem(ordem,modelo):
    try:
        DesenhaPixel(Personagens[ordem],modelo)
    except IndexError:
        Personagens
        print(ordem)

def DesenhaTiroPlayer(ordem,modelo):
    DesenhaPixel(TirosPlayer[ordem],modelo)

def DesenhaTiroInimigo(ordem,modelo):
    DesenhaPixel(TirosInimigos[ordem],modelo)
        
def DesenhaNumero(x, y, number):
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glScale(5,4,0)

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
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, -0.5)
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
        glVertex2f(0.5, -0.5)
    elif number == 8:
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(-0.5, 0)
        glVertex2f(0.5, 0)
        glVertex2f(-0.5, 0)
        glVertex2f(0.5, 0)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, -0.5)
    if number == 9:
        glVertex2f(-0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(-0.5, -0.5)
        glVertex2f(-0.5, 0)
        glVertex2f(0.5, 0)
        glVertex2f(-0.5, 0)
        glVertex2f(0.5, 0)
        glVertex2f(-0.5, 0.5)
        glVertex2f(-0.5, 0)
    elif number == 10:
        glVertex2f(-1, -0.5)
        glVertex2f(-1, 0.5)
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

def CheckColisaoTela():
    global Min,Max,Vidas,Personagens

    for personagem in Personagens:
        if(personagem.posicao.x >= Max.x or personagem.posicao.x <= Min.x) or (personagem.posicao.y >= Max.y or personagem.posicao.y <= (Max.y * -0.85)):
                personagem.rotacao = 0
                personagem.vetor = Ponto(0,0.2)
                personagem.posicao = Ponto(0,0,0)
                if(personagem == Personagens[0]): 
                    Vidas -= 1

def CheckColisaoPlayerInimigos():
    global Min,Max,Vidas

    player = Personagens[0]

    playerMediaCordenadasX = player.modelo.BoundingBox[3][1] / 2
    playerMediaCordenadasY = player.modelo.BoundingBox[3][0] / 2

    playerMinX = player.posicao.x - playerMediaCordenadasX
    playerMaxX = player.posicao.x + playerMediaCordenadasX

    playerMinY = player.posicao.y - playerMediaCordenadasY
    playerMaxY = player.posicao.y + playerMediaCordenadasY

    for personagem in Personagens[1:]:

        personagemMediaCordenadasX = personagem.modelo.BoundingBox[3][1] / 2
        personagemMediaCordenadasY = personagem.modelo.BoundingBox[3][0] / 2

        minX = personagem.posicao.x - personagemMediaCordenadasX
        maxX = personagem.posicao.x + personagemMediaCordenadasX

        minY = personagem.posicao.y + personagemMediaCordenadasY
        maxY = personagem.posicao.y + personagemMediaCordenadasY

        if((playerMinX <= maxX and playerMaxX >= minX) and (playerMinY <= maxY and playerMaxY >= minY)):
            print(personagem)
            player.posicao = Ponto(0,0,0)
            player.rotacao = 0
            player.vetor = Ponto(0,0.1)
            Vidas -= 1

def CheckColisaoTirosPlayerComInimigos():
    global Min,Max,Vidas
    
    for tiroPlayer in TirosPlayer:

        playerTiroMediaCordenadasX = tiroPlayer.modelo.BoundingBox[3][1] / 2
        playerTiroMediaCordenadasY = tiroPlayer.modelo.BoundingBox[3][0] / 2

        playerTiroMinX = tiroPlayer.posicao.x + tiroPlayer.pivot.x - playerTiroMediaCordenadasX
        playerTiroMaxX = tiroPlayer.posicao.x + tiroPlayer.pivot.x + playerTiroMediaCordenadasX

        playerTiroMinY = tiroPlayer.posicao.y + tiroPlayer.pivot.y - playerTiroMediaCordenadasY
        playerTiroMaxY = tiroPlayer.posicao.y + tiroPlayer.pivot.y + playerTiroMediaCordenadasY

        for personagem in Personagens[1:]:

            personagemMediaCordenadasX = personagem.modelo.BoundingBox[3][1] / 2
            personagemMediaCordenadasY = personagem.modelo.BoundingBox[3][0] / 2

            minX = personagem.posicao.x + personagem.pivot.x - personagemMediaCordenadasX
            maxX = personagem.posicao.x + personagem.pivot.x + personagemMediaCordenadasX

            minY = personagem.posicao.y - personagemMediaCordenadasY
            maxY = personagem.posicao.y + personagemMediaCordenadasY

            if((maxX >= playerTiroMinX and minX <= playerTiroMaxX) and (maxY >= playerTiroMinY and minY <= playerTiroMaxY)):
                indexReferencia = personagem.ordem
                Personagens.remove(personagem)
                for inimigos in Personagens[1:]:
                    if(inimigos.ordem > indexReferencia):
                        inimigos.ordem -= 1
        
        if(playerTiroMinY <= -75):

            tiroPlayer.podeDesenhar = False

def DesenhaUI():
    global Min, Max, AlturaUi, Municao, TotalTiro

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
    
    DesenhaPlayerUI(Player)
    DesenhaNumero(UIReferenceX + (Max.x / 4) , UIReferenceY - 3.5, Vidas)

    glTranslatef(abs(UIReferenceX) - 3, UIReferenceY ,0)
    DesenhaPlayerUI(TiroPlayer)
    DesenhaNumero(abs(UIReferenceX) - (Max.x / 10) , UIReferenceY - 3.5, Municao - TotalTiro)
    
    glPopMatrix()

def DesenhaPersonagens():
    for personagens in Personagens:
        personagens.Desenha()
    for tiros in TirosPlayer:
        tiros.Desenha()
    for tiros in TirosInimigos:
        tiros.Desenha()  

def CriaTiroInimigo():
    global Personagens

    if(len(Personagens) > 1 and (len(TirosInimigos) <= 5)):
        inimigo = Personagens[random.randint(1,len(Personagens) - 1)]
        tiro = Instancia()
        
        TirosInimigos.append(tiro)
        indexTiro = TirosInimigos.index(tiro)

        player = Personagens[0]

        vetorX, vetorY = 0,0

        if(player.posicao.x - inimigo.posicao.x >= 0): vetorX = 0.5
        if(player.posicao.y - inimigo.posicao.y >= 0): vetorY = 0.5

        TirosInimigos[indexTiro].posicao = Ponto(inimigo.posicao.x,inimigo.posicao.y)
        TirosInimigos[indexTiro].vetor = Ponto(vetorX,vetorY, 0)
        TirosInimigos[indexTiro].rotacao = inimigo.rotacao
        TirosInimigos[indexTiro].escala = Ponto (1,1,1)
        TirosInimigos[indexTiro].pivot = Ponto(0,0,0)
        TirosInimigos[indexTiro].modelo = TiroInimigo
        TirosInimigos[indexTiro].ordem = indexTiro
        TirosInimigos[indexTiro].desenhaModelo = DesenhaTiroInimigo
        tiro.Desenha()
    else:
        TirosInimigos.clear()

def animate():
    global AccumDeltaT,oldTime,nFrames,TempoTotal,PodeAtirar,TempoParaAtirar,TotalTiro,TempoTiroInimigo

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1 

    TempoTiroInimigo = TempoTotal

    if(int(TempoTotal) % 3 == 0 and TempoTotal >= 1):
        TempoTotal = 0
        CriaTiroInimigo()

    if AccumDeltaT > 1.0/30:
        if(PodeAtirar == False):
            TempoParaAtirar -= 1
        if(TempoParaAtirar == 0):
            TirosPlayer.clear()
            TempoParaAtirar = 90
            PodeAtirar = True
            TotalTiro = 0  
        AccumDeltaT = 0
        display()
        glutPostRedisplay()

def ContaTiro():
    global Municao,TotalTiro, PodeAtirar
     
    if ((Municao - TotalTiro) == 0):
        PodeAtirar = False

def VerificaGameOver():
    global Vidas

    # if(Vidas == 0):
    #     null
# ***********************************************************************************
def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLineWidth(3)
    glColor3f(1,1,1) # R, G, B  [0..1]
    
    ContaTiro()

    VerificaGameOver()
    DesenhaUI()
    DesenhaPersonagens()
    
    CheckColisaoTela()
    CheckColisaoPlayerInimigos()
    CheckColisaoTirosPlayerComInimigos()
    
    glutSwapBuffers()

ESCAPE = b'\x1b'
def keyboard(*args):
    global TotalTiro,PodeAtirar

    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b' ' and PodeAtirar == True:
        TirosPlayer.append(Instancia())
        TirosPlayer[TotalTiro].posicao = Ponto(Personagens[0].posicao.x,Personagens[0].posicao.y)
        TirosPlayer[TotalTiro].vetor = Ponto(Personagens[0].vetor.x * 3, Personagens[0].vetor.y * 3, 0)
        TirosPlayer[TotalTiro].rotacao = Personagens[0].rotacao
        TirosPlayer[TotalTiro].escala = Ponto (0.3,0.3,1)
        TirosPlayer[TotalTiro].pivot = Ponto(0,0,0)
        TirosPlayer[TotalTiro].modelo = TiroPlayer
        TirosPlayer[TotalTiro].ordem = TotalTiro
        TirosPlayer[TotalTiro].desenhaModelo = DesenhaTiroPlayer

        TotalTiro += 1
    glutPostRedisplay()

def arrow_keys(a_keys: int, x: int, y: int):
    global TotalTiro
    
    if a_keys == GLUT_KEY_UP:
        Personagens[0].vetor.y = 0.5
        Personagens[0].vetor.x = 0
        Personagens[0].rotacao = 0
        Personagens[0].pivot = Ponto(-4,-8,0)
    if a_keys == GLUT_KEY_DOWN:       
        Personagens[0].vetor.y = -0.5
        Personagens[0].vetor.x = 0
        Personagens[0].rotacao = 180
    
    else:
        rotacao = Personagens[0].rotacao
            
        if(rotacao == 0):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = -0.5
                Personagens[0].vetor.y = 0.5
                Personagens[0].rotacao = 45
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0.5
                Personagens[0].vetor.y = 0.5
                Personagens[0].rotacao = -45
        elif(rotacao == 45):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = -0.5
                Personagens[0].vetor.y = 0
                Personagens[0].rotacao = 90
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0
                Personagens[0].vetor.y = 0.5
                Personagens[0].rotacao = 0
        elif(rotacao == 90):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = -0.5
                Personagens[0].vetor.y = -0.5
                Personagens[0].rotacao = 135
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = -0.5
                Personagens[0].vetor.y = 0.5
                Personagens[0].rotacao = 45
        elif(rotacao == 135):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = -0.5
                Personagens[0].vetor.y = 0
                Personagens[0].rotacao = 90
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0
                Personagens[0].vetor.y = -0.5
                Personagens[0].rotacao = 180
        elif(rotacao == 180):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = -0.5
                Personagens[0].vetor.y = -0.5
                Personagens[0].rotacao = 135
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0.5
                Personagens[0].vetor.y = -0.5
                Personagens[0].rotacao = -135
        elif(rotacao == -135):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = 0
                Personagens[0].vetor.y = -0.5
                Personagens[0].rotacao = 180
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0.5
                Personagens[0].vetor.y = 0
                Personagens[0].rotacao = -90
        elif(rotacao == -90):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = 0.5
                Personagens[0].vetor.y = 0.5
                Personagens[0].rotacao = -45
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0.5
                Personagens[0].vetor.y = -0.5
                Personagens[0].rotacao = -135
        elif(rotacao == -45):
            if (a_keys == GLUT_KEY_LEFT):
                Personagens[0].vetor.x = 0
                Personagens[0].vetor.y = 0.5
                Personagens[0].rotacao = 0
            if (a_keys == GLUT_KEY_RIGHT):
                Personagens[0].vetor.x = 0.5
                Personagens[0].vetor.y = 0
                Personagens[0].rotacao = -90

    glutPostRedisplay()

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

def CriaInstancias():
    global Personagens, NumeroInicialDeInimigos

    NumeroInicialDeInimigos = 10

    Personagens.append(Instancia())
    Personagens[0].posicao = Ponto(0,0)
    Personagens[0].escala = Ponto (0.2,0.2,1)
    Personagens[0].pivot = Ponto(-4,-8,0)
    Personagens[0].modelo = Player
    Personagens[0].desenhaModelo = DesenhaPersonagem

    for inimigo in range(NumeroInicialDeInimigos):
        inimigo1RandomX1 = random.uniform(-90,0)
        inimigo1RandomX2 = random.uniform(90,0)
        
        inimigo1RandomY1 = random.uniform(-75,0)
        inimigo1RandomY2 = random.uniform(10,0)
        
        modeloInimigo = random.randint(0,2)

        inimigo1X = inimigo1RandomX1 + inimigo1RandomX2
        inimigo1Y = inimigo1RandomY1 + inimigo1RandomY2

        ListaDeModelos.append(Polygon(("Personagens\inimigo"+str(modeloInimigo+1)+".txt")))
        novoInimigo = Instancia()
        novoInimigo.posicao = Ponto(inimigo1X,inimigo1Y)
        
        Personagens.append(novoInimigo)
        indexInimigo = len(Personagens) - 1

        Personagens[indexInimigo].escala = Ponto (0,0,0)
        Personagens[indexInimigo].vetor = Ponto (0,0,0)
        Personagens[indexInimigo].pivot = Ponto(-4,-8,0)
        Personagens[indexInimigo].modelo = ListaDeModelos[inimigo]
        Personagens[indexInimigo].ordem = indexInimigo
        Personagens[indexInimigo].desenhaModelo = DesenhaPersonagem

def init():
    global Min, Max,NumeroInicialDeInimigos
    
    d:float = 100
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)
    
    MaxX = (Max.x * 2) - 40
    MaxY = Max.y + 75 - 40
    #Quad = QuadTree(MaxX,MaxY)
    
    glClearColor(0, 0, 0, 1)
    CriaInstancias()



glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(900, 800)
glutInitWindowPosition(0, 0)
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
