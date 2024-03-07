import pygame as pg
import sys
from button import *
from graph import *
from title import *
import random

WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
PINK = (230, 50, 230)
num = 20

class Edge(pg.sprite.Sprite):
    '''
        Класс ребер графа
    '''
    def __init__(self, v1, v2, screen, color=GRAY, size=3, pos1=None, pos2=None):
        super().__init__()
        self.v1 = v1
        self.v2 = v2
        self.w = random.randint(1, num)
        print("Первая вершина:", self.v1, "Вторая вершина:", self.v2, "Вес:", self.w)
        self.color = color
        self.screen = screen
        self.size = size
        self.image = pg.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (pos1, pos2)
    def update(self):
        # обновление картинки ребер
        global text, screen
        pg.draw.line(self.screen, self.color, self.pos[0], self.pos[1], self.size)
        self.screen.blit(self.image, (self.pos[0][0], self.pos[0][1]))

class EdgeGroup(pg.sprite.Group):
    '''
        Группа ребер графа
    '''
    def update(self, a):
        # добавляем ребро в группу и обновляем
        self.add(a)
        super().update()

class VertexClass(pg.sprite.Sprite):
    '''
        Класс вершин графа
    '''
    def __init__(self, name, screen, color=GRAY, size=35, pos=None):
        super().__init__()
        self.name = name
        print(self.name)
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
        # обновляем картинку вершин
        pg.draw.circle(self.image, self.color, (self.size // 2,self.size // 2), self.size // 2)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))


i = 0
j = 0
b = []
graph = []
class VertexGroup(pg.sprite.Group):
    '''
        Группа вершин графа
    '''

    def update(self, events, screen=None):
        global graph, St, i
        self.ch = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # проверяем каждую из вершин в группе, был ли по ней клик
                for v in self.spritedict:
                    if v.rect.collidepoint(event.pos):
                        # если был клик, то считаем одной из вершин будущего ребра, меняем цвет
                        self.ch = True
                        if v.color == GRAY:
                            v.color = PINK
                            self.addedge(v, pg.mouse.get_pos(), screen)
                if self.ch is False:
                    # если не было клика по вершине, значит создаем в этой точке новую вершину
                    if not St.buttonRect.collidepoint(pg.mouse.get_pos()):
                        self.add(VertexClass(i, screen, pos=pg.mouse.get_pos()))
                        i += 1
        super().update()
    def addedge(self, v, pos, screen):
        global b, graph, ed
        b.append(v)
        if len(b) == 2:
            #если было кликнуто по двум вершинам, создаем ребро
            A = Edge(b[0].name, b[1].name, screen, pos1 = b[0].center, pos2 = b[1].center)
            ed.update(A)
            b[0].color = GRAY
            b[1].color = GRAY
            graph.append((b[0].name, b[1].name, A.w))
            b[0].update()
            b[1].update()
            b.clear()


def myFunction():
    # создаем граф, вызываем функцию Форда-Беллмана
    global b, gr
    G = Graph(graph, i)
    if len(b) == 0:
        for g in gr.spritedict:
            if g.name == 0:
                b.append(g)
                break
    b[0].color = GRAY
    ans = bellman_ford(G.graph, G.n, b[0].name)
    print("Ответ:")
    for j in range(i):
        print("Расстояние от вершины", b[0].name, "до", j, "->", ans[j])

def upd(v):
    # меняем цвет вершины/ребра, если наша программа в неё заходит/из неё выходит
    if v.color == PINK:
        v.color = GRAY
        v.update()
        pygame.display.update()
        pygame.time.delay(500)
    v.color = PINK
    v.update()
    pygame.display.update()
    pygame.time.delay(500)

def bellman_ford(graph, n, s):
    # ункция обхода графа Беллмана-Форда
    global gr, screen, ed
    dist = [float('inf')] * n
    dist[s] = 0
    for _ in range(n - 1):
        for src, dest, weight in graph:
            for v in gr.spritedict:
                if v.name == src:
                    # меняем цвет вершины, в которой сейчас находимся
                    upd(v)
                    for k in ed.spritedict:
                        if k.v1 == src and k.v2 == dest:
                            # меняем цвет ребра, в котором сейчас находимся
                            upd(k)
                            break
                    break
            for l in gr.spritedict:
                if l.name == dest:
                    # меняем цвет вершины, в которую собираемся пойти
                    upd(l)
                    break

            if dist[src] + weight < dist[dest]:
                dist[dest] = dist[src] + weight

            print("Расстояние от начальной вершины до "+str(dest)+":", dist[dest])

        for e in gr.spritedict:
            # после одного цикла возвращаем всем вершинам серый цвет
            e.color = GRAY
            e.update()
        for l in ed.spritedict:
            # после одного цикла возвращаем всем ребрам серый цвет
            l.color = GRAY
            l.update()
        pygame.display.update()
        pygame.time.delay(500)


    return dist

screen = pg.display.set_mode((800,640))
screen.fill(WHITE)

# создаём вершины и помещаем их в группу
gr = VertexGroup()
# создаём ребра и помещаем их в группу
ed = EdgeGroup()
# создаём кнопу для старта обхода графа
St = Button(screen, 450, 540, 300, 50, 'Нажми, чтобы начать обход по графу', myFunction)

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    for object in objects:
        object.process(screen)
    # список полученных событий передаётся как параметр в функцию update группы вершин и ребер
    gr.update(events, screen)
    pg.display.update()
    pg.time.delay(100)

pg.quit()