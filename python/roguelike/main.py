import pygame
from pygame.locals import *
import Objs
import DATA

FPS = 60
TILE_SIZE = 30

WHITE = (255, 255, 255)
GREEN = (0  , 255,   0)
RED =   (255,   0,   0)
YELLOW= (255, 255,   0)
BLACK = (0, 0, 0)

data = DATA.DATA_MANAGER(r'.\data.bin')
data.load(lambda : {'levels': [], 'options': {'brightness': 0}})

def get_start_area(size):
    ret = [[(Objs.TILE(['wall', None]) if (i in [0, size[1]-1]) or (j in [0, size[0]-1]) or (i==5 and j==7)else Objs.TILE()) for i in range(size[1])] for j in range(size[0])]
    return ret

def END():
##    data.save()
    exit()

class GAME:

    def __init__(self):
        size = (20, 20)
        self.board = Objs.MAP(size, get_start_area(size), data = data)
        self.player = Objs.PLAYER(self.board, (1, 1))
        goblin = Objs.MOB(self.board, [18, 18])
        goblin.color = GREEN
        self.path = []
##        self.board.put_creature(goblin)#Не нужно, потому что он бахается на карту при инициализации

    def main_menu(self):
        items = {'play': self.run, 'Wow': lambda: print('Wow'), 'exit': lambda: END()}
        ITEM_H = screen.get_height()//(1+len(items))
        while True:
            clock.tick(FPS)
            # screen.fill(TILE_COLOR)
            for upbord in range(len(items)):
                surf = font.render(list(items.keys())[upbord], False, YELLOW)
                screen.blit(surf, ((screen.get_width()-surf.get_width())//2, ITEM_H*(upbord+1)))

            for event in pygame.event.get():
                if event.type==QUIT:
                    return 0
                if event.type==MOUSEBUTTONUP:
##                    print(event.pos[1]//ITEM_H)
                    list(items.values())[event.pos[1]*len(items)//screen.get_height()]()

            pygame.display.flip()

    def run(self):
        play = True
        while play:
            clock.tick(FPS)
            screen.fill(WHITE)
            screen.blit(self.get_surf(), (0, 0))

            if pygame.key.get_pressed()[K_UP]:
                self.player.move((0 ,-1))
            if pygame.key.get_pressed()[K_LEFT]:
                self.player.move((-1, 0))
            if pygame.key.get_pressed()[K_DOWN]:
                self.player.move(( 0, 1))
            if pygame.key.get_pressed()[K_RIGHT]:
                self.player.move(( 1, 0))
##            print(pygame.mouse.get_pressed())
            if pygame.mouse.get_pressed()[0]:
                self.path = self.player.move_to([i//TILE_SIZE for i in pygame.mouse.get_pos()])

            for event in pygame.event.get():
                if event.type==QUIT:
                    play = False
                if event.type==MOUSEBUTTONDOWN:
                    if event.button==1:
                        self.player.move_to([i//TILE_SIZE for i in event.pos])
                if event.type==KEYDOWN:
                    if event.key==K_SPACE:
##                        print(self.player.pos)
                        pause = True
                        surf = font.render('PAUSE', False, YELLOW)
                        screen.blit(surf, ((screen.get_width()-surf.get_width())//2, (screen.get_height()-surf.get_height())))
                        pygame.display.update()
                        while pause:
                            clock.tick(FPS)
                            for e in pygame.event.get():
                                if e.type==QUIT:
                                    pause = False
                                    play = False
                                elif e.type==KEYDOWN:
                                    if e.key==K_SPACE:
                                        pause = False
            pygame.display.flip()
        self.player.erase()
        self.board.erase()


    def get_surf(self):
        ret = pygame.Surface((TILE_SIZE*len(self.board.board), TILE_SIZE*len(self.board.board[0])))
        for i in range(len(self.board.board)):
            for j in range(len(self.board.board[i])):
##                print(self.board.board[i][j])
                if self.board.board[i][j]!=None:
                    ret.blit(pygame.transform.scale(self.board.board[i][j].surf, (TILE_SIZE, TILE_SIZE)), (i*TILE_SIZE, j*TILE_SIZE))
        for mob in self.board.mobs:
            ret.blit(pygame.transform.scale(mob.surf, [i*TILE_SIZE for i in mob.size]), [int(i*TILE_SIZE) for i in mob.pos])
        if len(self.path)>1:
##            print(self.path)
            pygame.draw.lines(ret, RED, False, [[j*TILE_SIZE for j in i] for i in self.path], 5)
        return ret

game = GAME()

pygame.init()
screen = pygame.display.set_mode((len(game.board.board)*TILE_SIZE, len(game.board.board[0])*TILE_SIZE))
clock = pygame.time.Clock()
font = pygame.font.SysFont('consolas', 40)
pygame.display.flip()

game.main_menu()
data.save()

pygame.quit()
##data.save()
