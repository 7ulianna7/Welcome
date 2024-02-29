import pygame as pg

WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
PINK = (230, 50, 230)

class Edge(pg.sprite.Sprite):
    '''
        Класс ребер граба
    '''
    def __init__(self, name, screen, color=GRAY, size = 3, pos = None):
        self.name = name
        self.color = color
        self.screen = screen
        self.size = size
        self.image = pg.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = pos
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
            #print(self.rect.x, self.rect.y)

    def update(self):
        pg.draw.circle(self.image, self.color, (self.size // 2,self.size // 2), self.size // 2)
        self.screen.blit(self.image, (self.rect.x-20, self.rect.y-20))

class VertexGroup(pg.sprite.Group):
    '''
        Группа вершин графов
        По клику на вершину цвет меняется
    '''

    def update(self, events, screen=None, i=None, j=None, a=None):
        self.ch = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                # проверяем каждую из вершин в группе, был ли по ней клик
                for v in self.spritedict:
                    if v.rect.collidepoint(event.pos):
                        self.ch = True
                        v.color = PINK if v.color == GRAY else GRAY
                        self.addedge(pg.mouse.get_pos(), j, screen)
                if self.ch is False:
                    self.add(VertexClass(i, screen, pos=pg.mouse.get_pos()))
                    i += 1
        super().update()
    def addedge(self, pos, j, screen):
        self.pos = pos
        a.append(self.pos)
        if len(a) == 2:
            A = Edge(j, screen, pos = a)
            A.update()
            j += 1
            a.clear()



screen = pg.display.set_mode((640,320))
screen.fill(WHITE)
# создаём вершины и помещаем их в группу
gr = VertexGroup()
"""
for i in range(5):
    gr.add(VertexClass(i, screen, pos=(100+100*i, 100)))
"""
i = 0
j = 0
a = []
running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    # список полученных событий передаётся как параметр в функцию update группы вершин
    gr.update(events, screen, i, j, a)
    pg.display.update()
    pg.time.delay(100)

pg.quit()