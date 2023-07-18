import pygame
from pygame.locals import*
import random
import sys
def who(p1,p2,phase):
    player=[]
    if phase%2==0:
        player = [p1,p2]
        mover = 0
    else:
        player = [p2,p1]
        mover = 1
    return(player,mover)

def phase_adjust(phase,p_m):
    if p_m == 0:
        phase += 1
    elif p_m == 1:
        phase -= 1
    return(phase)

def value_dicision(value,direction):
    if direction == 1 or direction ==  2:
        value = value
    if direction == 0 or direction ==  3:
        value = -1 * value
    return(value)

def move(p1,p2,value,phase,direction):
    player,mover = who(p1,p2,phase)
    val = value_dicision(value,direction)
    player[0] += val
    if mover == 0:
        player =player
    else:
        player = [player[1],player[0]]
    return(player[0],player[1])

def wall(x,wall_c,to_m_o_p):
    if x < wall_c and to_m_o_p == 0:
        return (True)
    elif x > wall_c and to_m_o_p ==1:
        return(True)
    
def colision(p1_x,p1_y,p2_x,p2_y):
    if p1_x == p2_x and p1_y == p2_y:
        return(True)
    else:
        return(False)
    
def against_move(direction,value,p_x,p_y):
    if direction == 0:
        p_y += value
    elif direction == 1:
        p_x -= value
    elif direction == 2:
        p_y -= value
    elif direction == 3:
        p_x += value
    return(p_x,p_y)
        
        
def p_col(p1x,p1y,p2x,p2y,phase,direction,value,er):
    if colision(p1x,p1y,p2x,p2y) == True:
        if phase%2 == 0:
            p1x,p1y = against_move(direction,value,p1x,p1y)
        else:
            p2x,p2y = against_move(direction,value,p2x,p2y)
        phase -=1
        er = 1
    return(er,phase,p1x,p1y,p2x,p2y)
    

def jam(phase,w_x_list,w_y_list,p_x,p_y,wall_np,value,direction,i1):
    if check(w_x_list,w_y_list,p_x,p_y,wall_np,direction) == True and item(i1,phase) == False:
        p_x,p_y=against_move(direction,value,p_x,p_y)
    return(p_x,p_y,phase)
            
def check(w_x_list,w_y_list,p_x,p_y,wall,direction):
    for i in range(len(w_x_list)):
        if direction == 0:
            w =i
        elif direction == 1:
            w = i+65
        elif direction == 2:
            w = i +8
        elif direction ==3:
            w = i+64

        if p_y < 100 and direction == 0:
            return(True)
        elif p_x > 1100 and direction ==1:
            return(True)
        elif p_y > 710 and direction == 2:
            return(True)
        elif p_x < 500 and direction ==3:
            return(True)
        elif p_x-50<=w_x_list[i]<p_x+50 and p_y-100<w_y_list[i]<p_y:
            if wall[w] == 1:
                return(True)
            else:
                return(False)
                
def wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,direction):
    if phase%2==0:
        wall = check(Lrect_x,Lrect_y,P1_x,P1_y,wall_np,direction)
    else:
        wall = check(Lrect_x,Lrect_y,P2_x,P2_y,wall_np,direction)
    return(wall)

def win(p1,p2,b_y,b_height):
    if p1 >  b_y + b_height-100:
        win = 1
    elif p2 < b_y+100:
        win =2
    else:
        win =0
    return(win)

def CanIPass(pas,phase,er,i1):
    if pas == 1 and item(i1,phase) == False:
        phase -= 1
        er = 1
    return (phase,er)

def item_decider(ax,bx,ay,by,width,base):
    x = random.randint(ax,bx) * width + base
    y = random.randint(ay,by) * width + base
    return(x,y)

def item(item,phase):
    if item == 1 and phase%2 == 0:
        return(True)
    elif item == 2 and phase%2 == 1:
        return(True)
    else:
        return(False)

def i2_use(i2,phase,i2_phase,pas,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d):
    if colision(P1_x,P1_y,P2_x,P2_y) == False and wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d) == False:
        if item(i2,phase) == True:
            i2_phase += 1
            if i2_phase % 2 ==0:
                phase -= 1
    return(phase,i2_phase)

def key_move(pas,phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d,speed,i1,er):
    if wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d)== True:
        pas = 1
    #壁があるか確認
    if phase%2 == 0 :
        P1_x,P1_y,phase = jam(phase,Lrect_x,Lrect_y,P1_x,P1_y,wall_np,speed,d,i1)
    else:
        P2_x,P2_y,phase = jam(phase,Lrect_x,Lrect_y,P2_x,P2_y,wall_np,speed,d,i1)
    #駒の移動
    if d % 2 == 0:
        P1_y,P2_y = move(P1_y,P2_y,speed,phase,d)
    elif d % 2 == 1:
        P1_x,P2_x = move(P1_x,P2_x,speed,phase,d)
    #ターンの処理
    phase,er = CanIPass(pas,phase,er,i1)
    #プレイヤーの衝突判定
    col = colision(P1_x,P1_y,P2_x,P2_y)
    return(pas,P1_x,P1_y,P2_x,P2_y,phase,er,col)

def item_getter(P1_x,P1_y,P2_x,P2_y,i_x,i_y,item):
    if colision(P1_x,P1_y,i_x,i_y) == True:
        item = 1
        i_x,i_y = 10000,10000
    elif colision(P2_x,P2_y,i_x,i_y) == True:
        item = 2
        i_x,i_y = 10000,10000
    return(i_x,i_y,item)


def item_text(item,w,b):
    if item == 1:
        tx = w
    elif item == 2:
        tx = b
    else:
        tx = None
    return(tx)

def main():
    pygame.init()
    screenX,screenY =1440,900
    screen = pygame.display.set_mode((screenX,screenY))
    pygame.display.set_caption("コリドール")

    #色指定
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    BROWN = (180,70,0)
    #ターンについて
    phase = -1
    i2_phase = 0
    #ボードの設定
    b_x,b_y = 410,10
    b_height,b_width = 800, 800
    #格子の設定
    m_width = 100
    m_height = 100
    Lrect_x =[]
    Lrect_y =[]
    wall_rect_l =[]
    wall_rect_r =[]

    wall_np =[]

    d = 99999999
    pas = 0

    #アイテムの設定
    i1_x,i1_y = item_decider(4,11,0,7,100,60)
    i2_x,i2_y = item_decider(4,11,0,7,100,60) 
    i1 = 0
    i2 = 0
    item3 = "colision"
    for j in range(8):
        for i in range(8):
            Lrect_x.append(b_x+m_width*i)
            Lrect_y.append(b_y+m_height*j)
            wall_rect_l.append(pygame.Rect(Lrect_x[i],Lrect_y[i+8*j],100,5))
            wall_rect_r.append(pygame.Rect(Lrect_x[i],Lrect_y[i+8*j],5,100))
            wall_np.append(0)
            wall_np.append(0)
    wall_rect = wall_rect_l + wall_rect_r
    wall_rect_amount = len(wall_rect)
    #プレイヤーの設定
    P1_x, P1_y = 760, 60
    P2_x, P2_y = 860, 760
    rad = 40
    speed =100
    #フォントと文字
    font = pygame.font.SysFont("hg正楷書体pro", 40)
    
    turn_text1 = font.render("白のターンです",True,BLACK,WHITE)
    turn_text2 = font.render("黒のターンです",True,BLACK,WHITE)
    
    error_tx = font.render("おっと、そこは壁です",True,RED,WHITE)
    error_tx2 = font.render("おっと、人がいますよ",True,RED,WHITE)
    
    i1_w = font.render("i1(壁超え):白",True,GREEN)
    i1_b = font.render("i1(壁超え):黒",True,GREEN)
    i2_w = font.render("i1(連撃):白",True,BLUE)
    i2_b = font.render("i1(連撃):黒",True,BLUE)
    
    P1Win = font.render("P1 Win!",True,BLACK)
    P2Win = font.render("P2 Win!",True,WHITE)
    tx_position1 = P1Win.get_rect(center=(screenX/2,screenY/2))
    tx_position2 = P2Win.get_rect(center=(screenX/2,screenY/2))
    
    er = 0
    er2 = 0
    while True:
        screen.fill(WHITE)
        board = pygame.Rect(b_x,b_y,b_width,b_height)
        pygame.draw.rect(screen,BROWN,board)
        col = 0
        
        for i in range(wall_rect_amount):
            if wall_np[i] == 0:
                pygame.draw.rect(screen,WHITE,wall_rect[i])
            elif wall_np[i] == 1:
                pygame.draw.rect(screen,BLACK,wall_rect[i])

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                for i in range(wall_rect_amount):
                    if wall_rect[i].collidepoint(event.pos):
                        wall_np[i]=1
                        phase +=1

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == K_UP:
                    d = 0
                                      
                if event.key == K_RIGHT:
                    d =1
                    
                if event.key == K_DOWN:
                    d = 2
                    
                if event.key == K_LEFT:
                    d = 3
                
                if event.key == K_UP or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_LEFT:
                    er =0
                    er2 = 0
                    pas = 0            
                    phase += 1
                    pas,P1_x,P1_y,P2_x,P2_y,phase,er,col = key_move(pas,phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d,speed,i1,er)
                    phase,i2_phase = i2_use(i2,phase,i2_phase,pas,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d)
                    
        er2,phase,P1_x,P1_y,P2_x,P2_y = p_col(P1_x,P1_y,P2_x,P2_y,phase,d,speed,er2)

        if phase % 2 == 0:
            screen.blit(turn_text2,(0,0))
        else:
            screen.blit(turn_text1,(0,0))
            
        if er == 1:
            screen.blit(error_tx,(0,300))
        elif er2 == 1:
            screen.blit(error_tx2,(0,300))

        i1_x,i1_y,i1 = item_getter(P1_x,P1_y,P2_x,P2_y,i1_x,i1_y,i1)
        i2_x,i2_y,i2 = item_getter(P1_x,P1_y,P2_x,P2_y,i2_x,i2_y,i2)

        pygame.draw.circle(screen,BLACK,(P2_x,P2_y),rad)        
        pygame.draw.circle(screen,WHITE,(P1_x,P1_y),rad)
        
        pygame.draw.circle(screen,GREEN,(i1_x,i1_y),rad)
        pygame.draw.circle(screen,BLUE,(i2_x,i2_y),rad)
        
        pygame.draw.line(screen,BLACK,(b_x,b_y),(b_x,b_y+b_height),5)
        pygame.draw.line(screen,BLACK,(b_x,b_y),(b_x+b_width,b_y),5)
        pygame.draw.line(screen,BLACK,(b_x,b_y+b_height),(b_x+b_width,b_y+b_height),4)
        pygame.draw.line(screen,BLACK,(b_x+b_width,b_y),(b_x+b_width,b_y+b_height),4)

        i1_tx = item_text(i1,i1_w,i1_b)
        i2_tx = item_text(i2,i2_w,i2_b)
        if i1_tx != None:
            screen.blit(i1_tx,(0,400))
        if i2_tx != None:
            screen.blit(i2_tx,(0,450))
        
        winner = win(P1_y,P2_y,b_y,b_height)
        #勝利条件
        if winner == 1:
            screen.fill(WHITE)
            screen.blit(P1Win,tx_position1)
        elif winner == 2:
            screen.fill(BLACK)
            screen.blit(P2Win,tx_position2)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
