from random import randint as rnd
from Graph_path import GRAPH, PATH
import pygame
import math
from geometry import VECTOR
import os

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

    def surf_save(self):
        path = '.\\picts\\tiles\\'
        listdir = os.listdir(path=path)
        name = str((max([int(file[:-4]) for file in listdir]) if listdir!=[] else 0)+1)+'.png'
        ret = path+name
        pygame.image.save(self.surf, ret)
        return ret

    def encode(self):
        ret = {}#self.content.copy()
        ret['opacity'] = self.opacity
        ret['depth'] = self.depth
        ret['surf'] = self.surf_save()
        ret['content'] = {}
        for i in self.content:
            ret['content'][i] = self.content[i].value
        return ret
    
##    @classmethod
    def decode(self, mas):
        self.opacity = mas['opacity']
        self.depth = mas['depth']
        self.surf = pygame.image.load(mas['surf'])
        self.content = {}
        for i in mas['content']:
            self.content[i] = mas['content'][i]

def board_decode(mas):
    ret = []
    for i in mas:
        ret.append([])
        for j in i:
            t = TILE().decode(j)
            ret[-1].append(t)
    return ret

def board_encode(board):
    ret = []
    for i in board:
        ret.append([])
        for j in i:
            ret[-1].append(j.encode())
    return ret

def graph_decode(mas):
    ret = GRAPH(mas['graph'])
    ret.paths = []
    for i in mas['paths']:
        ret.paths.append([])
        for j in i:
            p = PATH(j['price'])
            p.path = j['path']
            ret.paths[-1].append(p)
    return ret

def graph_encode(graph):
    ret = {'graph': graph.graph, 'paths':[]}
    for i in graph.paths:
        ret['paths'].append([])
        for j in i:
            ret['paths'][-1].append({'price': j.price, 'path': j.path})
    return ret

def mobs_decode(mas, board):
    mobs = []
    for mob in mas:
        m = MOB(board)
        mobs.append(m.decode(mob))
    return mobs

def mobs_encode(mobs):
    ret = []
    for mob in mobs:
        ret.append(mob.encode())
    return ret


class MAP:

    def __init__(self, size, sboard = None, **kwargs):
##        self.mobs = []
        if 'data' in kwargs:
            if (len(kwargs['data'].data['levels'])>0):
                self.board = board_decode(kwargs['data'].data['levels'][0]['board'])
                self.graph = graph_decode(kwargs['data'].data['levels'][0]['graph'])
                self.mobs  = mobs_decode(kwargs['data'].data['levels'][0]['mobs'], self)
            else:
                self.mobs = []
                if sboard == None:
                    self.board = [[(TILE(['wall', None]) if rnd(0, 2)==1 else TILE()) for _ in range(size[1])] for _ in range(size[0])]
                else:
                    self.board = sboard
                self.graph = GRAPH.map(self.board, lambda x, y: self.available((x+y)*(1/2), [0.49, 0.49]), lambda x, y: ((x[0]-y[0])**2+(x[1]-y[1])**2)**(1/2))
                self.graph.solve()
                kwargs['data'].data['levels'].append(self.encode())
        else:
            self.mobs = []
            if sboard == None:
                self.board = [[(TILE(['wall', None]) if rnd(0, 2)==1 else TILE()) for _ in range(size[1])] for _ in range(size[0])]
            else:
                self.board = sboard
            self.graph = GRAPH.map(self.board, lambda x, y: self.available((x+y)*(1/2), [0.49, 0.49]), lambda x, y: ((x[0]-y[0])**2+(x[1]-y[1])**2)**(1/2))
            self.graph.solve()

    def encode(self):
        ret = {'graph': graph_encode(self.graph),
               'board': board_encode(self.board),
               'mobs':  mobs_encode(self.mobs)}
        return ret

    def put_creature(self, target):
        self.mobs.append(target)
        return len(self.mobs)-1

    def erase(self):
        # for i in self.mobs:
        #     del i
        self.mobs = []
        self.generate()

    def generate(self, seed = 0):
        pass

    def available(self, pos, size):
        x1, y1 = [math.floor(i) for i in pos]
        x2, y2 = [math.floor(pos[i]+size[i])  for i in range(len(pos))]
        ret = True
        for i in [x1, x2]:
            for j in [y1, y2]:
                if 0<=i<len(self.board) and 0<=j<len(self.board[0]):
                    ret *= not 'wall' in self.board[i][j].content
                else:
                    return False
##        print(ret)
        return ret

class MOB:

    def __init__(self, board, spos = None):
        self.board = board
        if spos == None:
            self.pos = [rnd(0, (len(board) if i==0 else len(board[0]))-1) for i in range(2)]
        else:
            self.pos = list(spos)
        self.ind = board.put_creature(self)
        # self.body = []
        self.lvl = 0
        self.dmg = 1
        self.armor = 1
        self.exp = 1
        self.hp = 1
        self.hp_max = 10
        self.speed = 0.1
        self.size = [0.8, 0.8]
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 0))
        self.__prev_step_is_correct = False

    def encode(self):
        ret = {'pos': self.pos,
               'lvl': self.lvl,
               'dmg': self.dmg,
               'armor': self.armor,
               'exp': self.exp,
               'ind': self.ind,
               'hp': self.hp,
               'hp_max': self.hp_max,
               'speed': self.speed,
               'size': self.size,
               'surf': self.surf_save()}

    def surf_save(self):
        path = '.\\picts\\mobs\\'
        listdir = os.listdir(path=path)
        name = str((max([int(file[:-4]) for file in listdir]) if listdir!=[] else 0)+1)+'.png'
        ret = path+name
        pygame.image.save(self.surf, ret)
        return ret

    def decode(self, mas):
        self.pos = mas['pos']
        self.lvl = mas['lvl']
        self.dmg = mas['dmg']
        self.armor = mas['armor']
        self.exp = mas['exp']
        self.ind = mas['ind']
        self.hp = mas['hp']
        self.hp_max = mas['hp_max']
        self.speed = mas['speed']
        self.size = mas['size']
        self.surf = pygame.image.load(mas['surf'])

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
        if not ('is_correct' in kwargs and kwargs['is_correct']):
            self.__prev_step_is_correct = False
        if type(d)!=VECTOR:
            d = VECTOR(d[0], d[1])
        d.normalise()
        new_pos = [max(0, min(self.pos[0]+self.speed*d.pos[0], len(self.board.board)-self.size[0])),
                   max(0, min(self.pos[1]+self.speed*d.pos[1], len(self.board.board[0])-self.size[1]))]
        if self.board.available(new_pos, self.size):
            self.pos = new_pos

    def move_to(self, end):
##        print(self.pos)
        start = [round(i) for i in self.pos]
        path = self.board.graph.paths[start[0]*len(self.board.board[0])+start[1]][end[0]*len(self.board.board[0])+end[1]].path
        if len(path)<2:
            return []
        path = [[i//len(self.board.board[0]), i%len(self.board.board[0])] for i in path]
##        print(self.pos, path[0])
        if self.pos==path[0] or self.__prev_step_is_correct:
            mid = path[1]
##            print('!', mid, self.pos)
            self.__prev_step_is_correct = True
        else:
            mid = path[0]#[path[0]//len(self.board.board[0]), path[0]%len(self.board.board[0])]
        d = VECTOR(*mid)-VECTOR(*self.pos)
        self.move(d, is_correct = True)
        return path

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
