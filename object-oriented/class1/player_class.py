import pygame
from PIL import Image
class Player:
    def m_player_X(self,screen,x,y,i,j,grid,size,mod):
        rx, ry = x + int(j/2) * (mod+size), y +int(i/2)*(mod+size)
        x_mark = Image.open("X_mark_revised.png")
        x_resize = x_mark.resize((size,size),Image.ANTIALIAS)
        image_data = x_resize.tobytes("raw", x_resize.mode)
        image_pg = pygame.image.fromstring(image_data, x_resize.size, x_resize.mode).convert_alpha()
        screen.blit(image_pg,(rx,ry))

    def m_player_O(self,screen,x,y,i,j,grid,size,mod):
        rx, ry = x + int(j/2) * (mod+size), y +int(i/2)*(mod+size)
        o_mark = Image.open("O_mark_revised.png")
        o_resize = o_mark.resize((size,size),Image.ANTIALIAS)
        image_data = o_resize.tobytes("raw", o_resize.mode)
        image_pg = pygame.image.fromstring(image_data, o_resize.size, o_resize.mode).convert_alpha()
        screen.blit(image_pg,(rx,ry))
        
    def m_player(self,rad,x,y,screen,color):
        player = pygame.draw.circle(screen,color,(x,y),rad)
        
    def which(self,phase):
        if phase % 2 == 0:
            return(True)
        else:
            return(False)
        
    def move(self,speed,p1x,p1y,p2x,p2y,d,phase):
        if d != 4:
            if self.which(phase) == True:
                if d == 0:
                    p1y -= speed
                if d == 1:
                    p1x += speed
                if d == 2:
                    p1y += speed
                if d == 3:
                    p1x -= speed
            else:
                if d == 0:
                    p2y -= speed
                if d == 1:
                    p2x += speed
                if d == 2:
                    p2y += speed
                if d == 3:
                    p2x -= speed
        return(p1x,p1y,p2x,p2y,phase)

    def deci_by_mat(self,pi,pj,matrix,size):
        true_size =size + 10
        px,py = matrix[pi][pj].x + true_size, matrix[pi][pj].y + true_size
        return(px,py)
    
    def move_mat(self,pi,pj,matrix,d,maxx,phase):
        matrix[pi][pj] = 0
        if d == 0:
            if pi >0 and self.check_mat(matrix,pi,pj,d)  != False:
                pi = pi-2
            else:
                phase -= 1
        elif d == 1:
            if pj < maxx-2 and self.check_mat(matrix,pi,pj,d)  != False:
                pj = pj+2
            else:            
                phase -= 1
        elif d == 2:
            if pi < maxx-2 and self.check_mat(matrix,pi,pj,d) != False:
                pi = pi+2
            else:            
                phase -= 1
        elif d == 3:
            if pj > 0 and self.check_mat(matrix,pi,pj,d) != False:
                pj = pj-2
            else:            
                phase -= 1
        matrix[pi][pj] = 5
        return(matrix,pi,pj,phase)

    def check_mat(self,mat,pi,pj,d):
        if d == 0:
            if mat[pi-1][pj] > 0 or mat[pi-2][pj] > 0:
                return(False)
        if d == 1:
            if mat[pi][pj+1] > 0 or mat[pi][pj+2] > 0:
                return(False)
        if d == 2:
            if mat[pi+1][pj] > 0 or mat[pi+2][pj] > 0:
                return(False)
        if d == 3:
            if mat[pi][pj-1] > 0 or mat[pi][pj-2] > 0:
                return(False)
