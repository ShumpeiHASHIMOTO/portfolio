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
    

def jam(phase,w_x_list,w_y_list,p_x,p_y,wall_np,value,direction):
    if check(w_x_list,w_y_list,p_x,p_y,wall_np,direction) == True:
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

def CanIPass(pas,phase,er):
    if pas == 1:
        phase -= 1
        er = 1
    return (phase,er)

def item_decider(ax,bx,ay,by,width,base):
    x = random.randint(ax,bx) * width + base
    y = random.randint(ay,by) * width + base
    return(x,y)
def item1(i1,phase):
    if i1 == 1:
        phase -=1
    if i1 == 2:
        phase -=1
    
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
    lol = 0 
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

    d = 999999

    #アイテムの設定
    i1_x,i1_y = item_decider(4,11,0,7,100,60)
    i2_x,i2_y = item_decider(4,11,0,7,100,60) 
    i1 = 0
    i1_m = 0
    item2 =  "wall breaker"
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

                
                elif event.key == K_UP or event.key == K_RIGHT or event.key == K_DOWN or event.key == K_LEFT:
                    phase += 1
                    er =0
                    er2 = 0
                    pas = 0
                    print(i1)

                if event.key == K_UP:
                    d = 0
                    if wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d)== True:
                        pas = 1
                    #壁があるか確認
                    if phase%2 == 0 :
                        P1_x,P1_y,phase = jam(phase,Lrect_x,Lrect_y,P1_x,P1_y,wall_np,speed,d)
                    else:
                        P2_x,P2_y,phase = jam(phase,Lrect_x,Lrect_y,P2_x,P2_y,wall_np,speed,d)
                    #駒の移動
                    P1_y,P2_y = move(P1_y,P2_y,speed,phase,d)
                    #ターンの処理
                    phase,er = CanIPass(pas,phase,er)
                    #プレイヤーの衝突判定
                    col = colision(P1_x,P1_y,P2_x,P2_y)
                    
                    
                if event.key == K_RIGHT:
                    d =1
                    if wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d)== True:
                        pas = 1
                    if phase%2 == 0 :
                        P1_x,P1_y,phase = jam(phase,Lrect_x,Lrect_y,P1_x,P1_y,wall_np,speed,d)
                    else:
                        P2_x,P2_y,phase = jam(phase,Lrect_x,Lrect_y,P2_x,P2_y,wall_np,speed,d)
                    
                    P1_x,P2_x = move(P1_x,P2_x,speed,phase,d)
                    
                    phase,er = CanIPass(pas,phase,er)

                    col = colision(P1_x,P1_y,P2_x,P2_y)
                    
                if event.key == K_DOWN:
                    d = 2
                    if wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d)== True:
                        pas = 1
                    if phase%2 == 0 :
                        P1_x,P1_y,phase = jam(phase,Lrect_x,Lrect_y,P1_x,P1_y,wall_np,speed,d)
                    else:
                        P2_x,P2_y,phase = jam(phase,Lrect_x,Lrect_y,P2_x,P2_y,wall_np,speed,d)
                    
                    P1_y,P2_y = move(P1_y,P2_y,speed,phase,d)

                    phase,er = CanIPass(pas,phase,er)

                    col = colision(P1_x,P1_y,P2_x,P2_y)
                    
                if event.key == K_LEFT:
                    d = 3
                    if wall_check(phase,Lrect_x,Lrect_y,P1_x,P1_y,P2_x,P2_y,wall_np,d)== True:
                        pas = 1
                    if phase%2 == 0 :
                        P1_x,P1_y,phase = jam(phase,Lrect_x,Lrect_y,P1_x,P1_y,wall_np,speed,d)
                    else:
                        P2_x,P2_y,phase = jam(phase,Lrect_x,Lrect_y,P2_x,P2_y,wall_np,speed,d)
                    
                    P1_x,P2_x = move(P1_x,P2_x,speed,phase,d)

                    phase,er = CanIPass(pas,phase,er)

                    col = colision(P1_x,P1_y,P2_x,P2_y)

        er2,phase,P1_x,P1_y,P2_x,P2_y = p_col(P1_x,P1_y,P2_x,P2_y,phase,d,speed,er2)

        if phase % 2 == 0:
            screen.blit(turn_text2,(0,0))
        else:
            screen.blit(turn_text1,(0,0))
        if er == 1:
            screen.blit(error_tx,(0,300))
        elif er2 == 1:
            screen.blit(error_tx2,(0,300))

        if colision(P1_x,P1_y,i1_x,i1_y) == True:
            i1 = 1
            i1_x,i1_y = 10000,10000
        elif colision(P2_x,P2_y,i1_x,i1_y) == True:
            i1 = 2
            i1_x,i1_y = 10000,10000

        if i1 != 0:
            i1_m = 1
        if i1_m == 1:
            phase -=1
            i1_m =0

        pygame.draw.circle(screen,BLACK,(P2_x,P2_y),rad)        
        pygame.draw.circle(screen,WHITE,(P1_x,P1_y),rad)
        
        pygame.draw.circle(screen,GREEN,(i1_x,i1_y),rad)
        pygame.draw.circle(screen,BLUE,(i2_x,i2_y),rad)

        pygame.draw.line(screen,BLACK,(b_x,b_y),(b_x,b_y+b_height),5)
        pygame.draw.line(screen,BLACK,(b_x,b_y),(b_x+b_width,b_y),5)
        pygame.draw.line(screen,BLACK,(b_x,b_y+b_height),(b_x+b_width,b_y+b_height),4)
        pygame.draw.line(screen,BLACK,(b_x+b_width,b_y),(b_x+b_width,b_y+b_height),4)

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
