class NodoQuadTree:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.inimigo = None
        self.dividido = False
        self.folhas = []

    def subdividir(self):
        metade_largura = (self.largura / 2)
        metade_altura = (self.altura / 2)
        self.folhas = [
            NodoQuadTree(self.x - metade_largura, self.y, metade_largura, metade_altura), #Top Left
            NodoQuadTree(self.x, self.y, metade_largura, metade_altura), #Top Right
            NodoQuadTree(self.x - metade_largura, self.y - metade_altura,  metade_largura, metade_altura), #Bottom Left
            NodoQuadTree(self.x, self.y - metade_altura, metade_largura, metade_altura)                   #Bottom Right
        ]
        self.dividido = True

    def inserir(self, inimigo):
        if not self.contem(inimigo):
            return False
        
        if self.inimigo is None and not self.dividido:
            self.inimigo = inimigo
            return True
        else:
            if not self.dividido:
                self.subdividir()
            for folha in self.folhas:
                if folha.inserir(inimigo):
                    return True
        return False

    def contem(self, inimigo):
        return (self.x <= inimigo.posicao.x < self.x + self.largura and
                self.y <= inimigo.posicao.x < self.y + self.altura)

    def __str__(self, nivel=0):
        ret = "\t" * nivel + f"NodoQuadTree({self.x}, {self.y}, {self.largura}, {self.altura}, Inimigo: {self.inimigo})\n"
        if self.dividido:
            for folha in self.folhas:
                ret += folha.__str__(nivel + 1)
        return ret

class QuadTree:
    def __init__(self, largura, altura):
        self.raiz = NodoQuadTree(0, 0, largura, altura)

    def inserir(self, inimigo):
        return self.raiz.inserir(inimigo)

    def __str__(self):
        return str(self.raiz)