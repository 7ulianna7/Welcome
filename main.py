import pygame as pg
import sys
from button import *
from graph import *

WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
PINK = (230, 50, 230)

class Edge(pg.sprite.Sprite):
    '''
        Класс ребер граба
    '''
    def __init__(self, name, screen, color=GRAY, size=3, pos1=None, pos2=None):
        self.name = name
        self.color = color
        self.screen = screen
        self.size = size
        self.image = pg.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (pos1, pos2)
    def update(self):
        pg.draw.line(self.screen, self.color, self.pos[0], self.pos[1], self.size)
        self.screen.blit(self.image, (self.pos[0][0], self.pos[0][1]))
class VertexClass(pg.sprite.Sprite):
    '''
        Класс вершин графа
    '''
    def __init__(self, name, screen, color=GRAY, size=50, pos=None):
        super().__init__()
        self.name = name
        self.color = color
        self.size = size
        self.screen = screen
        self.image = pg.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        if pos:
            self.rect.x, self.rect.y = pos
            self.center = (self.rect.x + 20, self.rect.y + 20)

    def update(self):
        pg.draw.circle(self.image, self.color, (self.size // 2,self.size // 2), self.size // 2)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))


i = 0
j = 0
b = []
graph = []
class VertexGroup(pg.sprite.Group):
    '''
        Группа вершин графов
        По клику на вершину цвет меняется
    '''

    def update(self, events, screen=None):
        global graph, St
        self.ch = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # проверяем каждую из вершин в группе, был ли по ней клик
                for v in self.spritedict:
                    if v.rect.collidepoint(event.pos):
                        self.ch = True
                        if v.color == GRAY:
                            v.color = PINK
                            self.addedge(v, pg.mouse.get_pos(), screen)
                if self.ch is False:
                    if not St.buttonRect.collidepoint(pg.mouse.get_pos()):
                        global i
                        self.add(VertexClass(i, screen, pos=pg.mouse.get_pos()))
                        i += 1
        super().update()
    def addedge(self, v, pos, screen):
        global b, j, graph
        b.append(v)
        if len(b) == 2:
            A = Edge(j, screen, pos1 = b[0].center, pos2 = b[1].center)
            A.update()
            j += 1
            b[0].color = GRAY
            b[1].color = GRAY
            graph.append((b[0].name, b[1].name))
            graph.append((b[1].name, b[0].name))
            b[0].update()
            b[1].update()
            b.clear()


def myFunction():
    G = Graph(graph, i)

screen = pg.display.set_mode((800,640))
screen.fill(WHITE)
# создаём вершины и помещаем их в группу
gr = VertexGroup()
St = Button(screen, 450, 540, 300, 50, 'Нажми, чтобы начать обход по графу', myFunction)
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    for object in objects:
        object.process(screen)
    # список полученных событий передаётся как параметр в функцию update группы вершин
    gr.update(events, screen)
    pg.display.update()
    pg.time.delay(100)

pg.quit()