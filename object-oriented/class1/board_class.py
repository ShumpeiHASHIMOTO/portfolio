import pygame
import copy
class Board:
    basic_screen = 1440,900
    basic_board_cor = 410,10
    basic_board_size = 800,800
    
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    BROWN = (180,70,0)
    PALE_YELLOW = (255,241,171)
    
    font_path ="C:/Users/chado/AppData/Local/Programs/Python/Python311/newgame/Noto_Sans_JP/static/NotoSansJP-Black.ttf"


    def __init__(self):
        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.Font(self.font_path, 30)
        
    def m_screen(self,x,y,tx):
        screen = pygame.display.set_mode((x,y))
        s_cap = pygame.display.set_caption(tx)
        return(screen,s_cap)

    def m_rect(self,screen,x,y,w,h,color):
        r= pygame.Rect(x,y,w,h)
        con = pygame.draw.rect(screen,color,r)
        return(con)

    def wall_make(self,i,j):
        matrix = [[0 for _ in range(j)] for _ in range(i)]
        return(matrix)
    
    def edge(self,matrix,i,j):
        for a in range(i):
            for b in range(j):
                if a == 0 or a == i-1:
                        matrix[a][b] = 1
                        matrix[0][j-1] = 0
                        matrix[i-1][j-1] = 0
                elif b == 0 or b ==j-1:
                    if a%2 == 1:
                        matrix[a][b] =1
        return(matrix)
    def mat_rect(self,matrix,i,j,rect):
        for a in range(i):
            for b in range(j):
                if a % 2 != 0 and b % 2 != 0:
                        matrix[a][b] = rect
        return(matrix)

    def wall(self,dicmat,matrix,i,j,length,width,bx,by,screen,bw,bh,lw,trigger):#ボードの格子の部分をrect的に解釈
        for a in range(i):
            for b in range(j):
                x,y = (bx+ int(b/2) * length),(by +int(a/2)*length)
                if a% 2 == 0:
                    if b % 2 != 0:
                        matrix[a][b] = pygame.Rect(x,y,length,width)
                        if dicmat[a][b] != 1:
                            self.m_rect(screen,x,y,length,width,self.WHITE)
                        else:
                            self.m_rect(screen,x,y,length,width,self.BLACK)
                    elif b%2 == 0 and trigger == 1:
                        self.wallall(matrix,length,x,y,a,b)
                else:
                    if b%2 == 0:
                        matrix[a][b] =pygame.Rect(x,y,width,length+10)
                        if dicmat[a][b] != 1:
                            self.m_rect(screen,x,y,width,length+10,self.WHITE)
                        else:
                            self.m_rect(screen,x,y,width,length+10,self.BLACK)
                    elif b%2 != 0 and trigger == 1:
                        self.wallall(matrix,length,x,y,a,b)
        return(matrix)
    
    def wallall(self,matrix,size,x,y,a,b):#ボードのすべてをrect的に解釈する
        matrix[a][b] =pygame.Rect(x,y,size,size)
        return(matrix)
    
    def draw_wall(self,i,j,length,width,bx,by,screen,bw,bh,lw):
        wmat = self.wall(self,i,j,length,width,bx,by,screen,bw,bh,lw)
        for i in range(len(wmat)):
            pygame.draw.Rect(screen,self.WHITE,wmat[i])    

    def board_point(self,matrix,x,y,width,height,screen):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i % 2 != 0 and j % 2 != 0:
                    matrix[i][j] = pygame.Rect(x,y,width*int((j+1)/2),height*int((i+1)/2))
                    pygame.draw.rect(screen,self.BROWN,matrix[i][j])
        return(matrix)
    
    def wtx(self,tx,screen,sx,sy):
        screen.fill(self.WHITE)
        tx = self.font.render("{}の勝利".format(tx),True,self.BLACK)
        tx1 = self.font.render("press Key_R to restart",True,self.BLACK)
        tx_position = tx.get_rect(center=(sx/2,sy/2))
        tx1_position = tx1.get_rect(center=(sx/2,(sy+300)/2))
        screen.blit(tx,tx_position)
        screen.blit(tx1,tx1_position)
