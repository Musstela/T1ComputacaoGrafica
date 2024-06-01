import time
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from Poligonos import *
from Instancia import *
from QuadTree import *

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
Quad = None

# lista de instancias do Personagens
Personagens = []
TirosPlayer = []
TirosInimigos = []
TotalTiro = 0
PodeAtirar = True
FoiAtingido = False
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

def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0,0,1)
    glTranslatef(-P.x, -P.y, -P.z)

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
    global Min,Max,Vidas,Personagens,FoiAtingido

    for personagem in Personagens:
        if(personagem.posicao.x >= Max.x or personagem.posicao.x <= Min.x) or (personagem.posicao.y >= Max.y or personagem.posicao.y <= (Max.y * -0.70)):
                personagem.rotacao = 0
                personagem.vetor = geraVetorAleatorio()
                personagem.posicao = Ponto(0,0,0)
                if(personagem == Personagens[0]): 
                    FoiAtingido = True
                    personagem.vetor = Ponto(0,0.5,0)

def CheckColisaoPlayerInimigos():
    global Min,Max,Vidas,FoiAtingido

    player = Personagens[0]

    playerMediaCordenadasX = player.modelo.BoundingBox[3][1] / 2
    playerMediaCordenadasY = player.modelo.BoundingBox[3][0] / 2

    playerMinX = player.posicao.x + player.pivot.x - playerMediaCordenadasX
    playerMaxX = player.posicao.x + playerMediaCordenadasX

    playerMinY = player.posicao.y + player.pivot.y - playerMediaCordenadasY
    playerMaxY = player.posicao.y + player.pivot.y + playerMediaCordenadasY

    for personagem in Personagens[1:]:

        personagemMediaCordenadasX = personagem.modelo.BoundingBox[3][1] / 2
        personagemMediaCordenadasY = personagem.modelo.BoundingBox[3][0] / 2

        minX = personagem.posicao.x + personagem.pivot.x - personagemMediaCordenadasX
        maxX = personagem.posicao.x + personagem.pivot.x + personagemMediaCordenadasX

        minY = personagem.posicao.y + personagem.pivot.y - personagemMediaCordenadasY
        maxY = personagem.posicao.y + personagem.pivot.y + personagemMediaCordenadasY

        if((playerMinX <= maxX and playerMaxX >= minX) and (playerMinY <= maxY and playerMaxY >= minY)):
            player.posicao = Ponto(0,0,0)
            player.rotacao = 0
            player.vetor = Ponto(0,0.1)
            FoiAtingido = True

def CheckColisaoTirosComEntidades():
    global Min,Max,Vidas,FoiAtingido
    
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

    player = Personagens[0]

    playerMediaCordenadasX = player.modelo.BoundingBox[3][1] / 2
    playerMediaCordenadasY = player.modelo.BoundingBox[3][0] / 2

    minX = player.posicao.x - playerMediaCordenadasX
    maxX = player.posicao.x + playerMediaCordenadasX

    minY = player.posicao.y - playerMediaCordenadasY
    maxY = player.posicao.y + playerMediaCordenadasY
    
    for tiroInimigo in TirosInimigos:
        tiroInimigoMediaCordenadasX = tiroInimigo.modelo.BoundingBox[3][1] / 2
        tiroInimigoMediaCordenadasY = tiroInimigo.modelo.BoundingBox[3][0] / 2

        tiroInimigoMinX = tiroInimigo.posicao.x + tiroInimigo.pivot.x - tiroInimigoMediaCordenadasX
        tiroInimigoMaxX = tiroInimigo.posicao.x + tiroInimigo.pivot.x + tiroInimigoMediaCordenadasX

        tiroInimigoMinY = tiroInimigo.posicao.y + tiroInimigo.pivot.y - tiroInimigoMediaCordenadasY
        tiroInimigoMaxY = tiroInimigo.posicao.y + tiroInimigo.pivot.y + tiroInimigoMediaCordenadasY

        if((maxX >= tiroInimigoMinX and minX <= tiroInimigoMaxX) and (maxY >= tiroInimigoMinY and minY <= tiroInimigoMaxY)):
            tiroInimigo.podeDesenhar = False
            player.posicao = Ponto(0,0,0)
            player.rotacao = 0
            player.vetor = Ponto(0,0.1)
            TirosInimigos.remove(tiroInimigo)
            FoiAtingido = True

        if(tiroInimigoMinY <= -75):
            tiroInimigo.podeDesenhar = False

def DesenhaUI():
    global Min, Max, AlturaUi, Municao, TotalTiro,Vidas

    Meio = Ponto()

    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    AlturaUi = ((Max.y + abs(Min.y)) / 8 ) + (Min.y)
    
    glBegin(GL_LINES)
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

    if(len(Personagens) == 1 and Personagens[0].modelo == Player):
        glLineWidth(3)
        glColor3f(1,1,1)
        glScalef(0.2,0.2,0.2) 
        glPushMatrix()
        glTranslatef(-400, 0, 0)
        for character in "Voce Venceu":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(character))
        glPopMatrix()
    elif(Vidas == 0):
        glLineWidth(3)
        glColor3f(1,1,1)
        glScalef(0.2,0.2,0.2) 
        glPushMatrix()
        glTranslatef(-350, 0, 0)
        for character in "Game Over":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(character))
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

    if(len(Personagens) > 1 and (len(TirosInimigos) <= 15)):
        inimigo = Personagens[random.randint(1,len(Personagens) - 1)]
        tiro = Instancia()
        
        TirosInimigos.append(tiro)
        indexTiro = TirosInimigos.index(tiro)

        player = Personagens[0]
        vetorX, vetorY = 0,0
        rotacao = 0

        if(player.posicao.x > inimigo.posicao.x + 10):
            vetorX = 0.75
        elif(player.posicao.x < inimigo.posicao.x - 10):
            vetorX = -0.75

        if(player.posicao.y > inimigo.posicao.y + 10):
            vetorY = 0.75
        elif(player.posicao.y < inimigo.posicao.y - 10):
            vetorY = -0.75

        if(vetorX == 1 and vetorY == 0):rotacao = -90
        if(vetorX == 1 and vetorY == 1):rotacao = -45
        if(vetorX == 1 and vetorY == -1):rotacao = -135
        if(vetorX == 0 and vetorY == -1):rotacao = 180
        if(vetorX == -1 and vetorY == -1):rotacao = 135
        if(vetorX == -1 and vetorY == 0):rotacao = 90
        if(vetorX == -1 and vetorY == -1):rotacao = 45
            

        TirosInimigos[indexTiro].posicao = Ponto(inimigo.posicao.x,inimigo.posicao.y)
        TirosInimigos[indexTiro].vetor = Ponto(vetorX,vetorY, 0)
        TirosInimigos[indexTiro].rotacao = rotacao
        TirosInimigos[indexTiro].escala = Ponto (1,1,1)
        TirosInimigos[indexTiro].pivot = Ponto(0,0,0)
        TirosInimigos[indexTiro].modelo = TiroInimigo
        TirosInimigos[indexTiro].ordem = indexTiro
        TirosInimigos[indexTiro].desenhaModelo = DesenhaTiroInimigo
        tiro.Desenha()
    else:
        TirosInimigos.clear()

def MudaVetorInimigos():
    for inimigo in Personagens[1:]:
        inimigo.vetor = geraVetorAleatorio()

def animate():
    global AccumDeltaT,oldTime,nFrames,TempoTotal,PodeAtirar,TempoParaAtirar,TotalTiro,TempoTiroInimigo,Vidas,FoiAtingido

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1 

    TempoTiroInimigo = TempoTotal

    if AccumDeltaT > 1.0/30:
        if(FoiAtingido == True):
            FoiAtingido = False
            if(Vidas > 0): Vidas -= 1
        if(PodeAtirar == False):
            TempoParaAtirar -= 1
        if(TempoParaAtirar == 0):
            TirosPlayer.clear()
            TempoParaAtirar = 90
            PodeAtirar = True
            TotalTiro = 0  
        
        AccumDeltaT = 0
    
    if(int(TempoTotal) % 2 == 0 and TempoTotal >= 1):
        CriaTiroInimigo()
        MudaVetorInimigos()
        TempoTotal = 0

    if Vidas == 0:
        Personagens[0].podeDesenhar = False

    display()
    glutPostRedisplay()

def ContaTiro():
    global Municao,TotalTiro, PodeAtirar
     
    if ((Municao - TotalTiro) == 0):
        PodeAtirar = False

def display():

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLineWidth(3)
    glColor3f(1,1,1) # R, G, B  [0..1]
    
    ContaTiro()

    DesenhaUI()
    DesenhaPersonagens()
    
    CheckColisaoTela()
    CheckColisaoPlayerInimigos()
    CheckColisaoTirosComEntidades()
    
    glutSwapBuffers()

def keyboard(*args):
    ESCAPE = b'\x1b'
    global TotalTiro,PodeAtirar

    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b' ' and PodeAtirar == True and Vidas != 0:
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
                Personagens[0].vetor.y = 0.5
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

def geraVetorAleatorio():
    novoVetor = Ponto(0,0,0)
    movimento = [0,0.1,-0.1]

    while novoVetor.x == 0 and novoVetor.y == 0:
        novoVetor = Ponto(random.choice(movimento),random.choice(movimento),0)

    return novoVetor

def gerarInimigoAleatorio():
    while True:
        x = random.uniform(-90, 90)
        y = random.uniform(-100, 90)
        if not (-20 <= x <= 20 and -20 <= y <= 20) and (20 <= y <= 100 or -65 <= y <= -20):
            novoInimigo = Instancia()
            
            novoInimigo.posicao = Ponto(x,y)
            novoInimigo.escala = Ponto(0,0,0)
            novoInimigo.pivot = Ponto(-4,-8,0)
            novoInimigo.ordem = len(Personagens)
            novoInimigo.desenhaModelo = DesenhaPersonagem
            novoInimigo.vetor = geraVetorAleatorio()
            
            modeloInimigo = random.randint(1,3)
            ListaDeModelos.append(Polygon(("Personagens\inimigo"+str(modeloInimigo)+".txt")))
            novoInimigo.modelo = ListaDeModelos[len(Personagens) - 1]
            
            Quad.inserir(novoInimigo)
            return novoInimigo
    
def CriaInstancias():
    global Personagens, NumeroInicialDeInimigos

    NumeroInicialDeInimigos = 60

    Personagens.append(Instancia())
    Personagens[0].posicao = Ponto(0,0)
    Personagens[0].escala = Ponto (0.2,0.2,1)
    Personagens[0].pivot = Ponto(-4,-8,0)
    Personagens[0].modelo = Player
    Personagens[0].desenhaModelo = DesenhaPersonagem

    for _ in range(NumeroInicialDeInimigos):
        Personagens.append(gerarInimigoAleatorio())    

def init():
    global Min, Max, Quad
    
    d:float = 100
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)
    
    MaxX = (Max.x * 2) - 40
    MaxY = Max.y + 75 - 40
    Quad = QuadTree(MaxX,MaxY)
    
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
