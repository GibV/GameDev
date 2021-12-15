from random import randint as rnd
from Graph_path import GRAPH
import pygame
import math
from geometry import VECTOR

class CONTENT_VALUE:

    def __init__(self, value = 0):
        self.value = value

class TILE:

    def __init__(self, *args):
        self.opacity = 0
        self.depth = 0
        self.content = {'earth': CONTENT_VALUE(None)}
        for cont in args:
            self.content[cont[0]] = CONTENT_VALUE(cont[1])
        self.surf = pygame.Surface((10, 10))
        if 'wall' in self.content:
            self.surf.fill((127, 127, 127))

class MAP:

    def __init__(self, size, sboard = None):
        if sboard == None:
            self.board = [[(TILE(['wall', None]) if rnd(0, 2)==1 else TILE()) for _ in range(size[1])] for _ in range(size[0])]
        else:
            self.board = sboard
        self.mobs = []
        self.graph = GRAPH.map(self.board, lambda x: self.available(x, [1, 1]), lambda x, y: ((x[0]-y[0])**2+(x[1]-y[1])**2)**(1/2))
        self.graph.solve()

    def put_creature(self, target):
        self.mobs.append(target)

    def erase(self):
        # for i in self.mobs:
        #     del i
        self.mobs = []
        self.generate()

    def generate(self, seed = 0):
        pass

    def available(self, pos, size):
        print(len(self.board), len(self.board[0]), pos)
        cond_in = True
        cond_in *= math.floor(pos[0]+size[0])<len(self.board)
        print(pos[1]+size[1], math.floor(pos[1]+size[1]))
        cond_in *= math.floor(pos[1]+size[1])<len(self.board[0])
        cond_in *= 0<=pos[0] and 0<=pos[1]
        if not cond_in:
            print(False)
            return False
        x1, y1 = [math.floor(i) for i in pos]
        x2, y2 = [math.floor(pos[i]+size[i])  for i in range(len(pos))]
        ret = True
        for i in [x1, x2]:
            for j in [y1, y2]:
                if 0<=i<len(self.board) and 0<=j<len(self.board[0]):
                    ret *= not 'wall' in self.board[i][j].content
        print(ret)
        return ret

class MOB:

    def __init__(self, board, spos = None):
        self.board = board
        if spos == None:
            self.pos = [rnd(0, (len(board) if i==0 else len(board[0]))-1) for i in range(2)]
        else:
            self.pos = list(spos)
        board.put_creature(self)
        # self.body = []
        self.lvl = 0
        self.dmg = 1
        self.armor = 1
        self.exp = 1
        self.hp = 1
        self.speed = 0.1
        self.size = [0.8, 0.8]
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 0))

    @property
    def color(self):
        return None
    @color.setter
    def color(self, val):
        self.surf.fill(val)

    def defeat(self):
        pass

    def move(self, d, **kwargs):
        # print(pos)
        if type(d)!=VECTOR:
            d = VECTOR(d[0], d[1])
        d.normalise()
        new_pos = [max(0, min(self.pos[0]+self.speed*d.pos[0], len(self.board.board)-self.size[0])),
                   max(0, min(self.pos[1]+self.speed*d.pos[1], len(self.board.board[0])-self.size[1]))]
        if self.board.available(new_pos, self.size):
            self.pos = new_pos

    def move_to(self, end):
        start = [round(i) for i in self.pos]
        path = self.board.graph.paths[start[0]*len(self.board.board[0])+start[1]][end[0]*len(self.board.board[0])+end[1]].path
        if path==[]:
            return None
        path = path[-1]
        mid = [path//len(self.board.board[0]), path%len(self.board.board[0])]
        d = VECTOR(*mid)-VECTOR(*self.pos)
        self.move(d)

    def follow(self, target):
        pass

    def attack(self, target):
        pass

    def observe(self, **kwargs):
        pass

    def defense(self, target):
        pass

    def block(self):
        pass

    def damage(self, executor):
        pass

    def erase(self):
        pass

class PLAYER(MOB):
    pass
