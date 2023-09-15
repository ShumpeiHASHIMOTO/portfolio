import pygame
from class1.board_class import *
import sys
from class1.player_class import *
board = Board()
player = Player()
def win(phase,p1y,p2y,sc_x,sc_y,by,bh,screen):#勝利条件:
    if p1y >= by+bh-50 or p2y <= by+50:
        screen.fill(board.WHITE)
        if phase%2 == 0:
            board.wtx("黒",screen,sc_x,sc_y)
        else:
            board.wtx ("白",screen,sc_x,sc_y)
        game = 1
        return(game)
    else:
        return(0)
def start(bx,by,bw,bh,ww,wh):#初期値
    matrix_b = board.wall_make(17,17)#この行列でボードの壁か否かを判定する
    matrix_b = board.edge(matrix_b,17,17)#この行列でボードの端を壁にする
    p1x,p1y = bx+(bw/2)-(ww//2),by +(ww//2)
    i1, j1 = 1, 7
    p2x,p2y = bx+(bw/2)+(ww//2),by+bh-(ww//2)
    i2,j2 = 15,9
    matrix_b[i1][j1] = 5
    matrix_b[i2][j2] = 5
    phase = 0
    game = 0
    return(matrix_b,p1x,p1y,p2x,p2y,phase,game,i1,j1,i2,j2)
def wallORsq(matrix_b,i,j,phase):
    if matrix_b[i][j] != 1:
        matrix_b[i][j] = 1
        phase += 1
    return(matrix_b,phase)
def main():
    pygame.init()
    sc_x ,sc_y = board.basic_screen
    screen, caption = board.m_screen(sc_x,sc_y,"test")#スクリーン大きさ
    bx,by = board.basic_board_cor#ボードの座標
    bw,bh = board.basic_board_size#ボードの幅
    ww,wh = 100,5#格子の大きさ、幅
    size = 40#プレーヤーの駒の大きさ
    matrix_b,p1x,p1y,p2x,p2y,phase,game,i1,j1,i2,j2 = start(bx,by,bw,bh,ww,wh)#mat_b=壁があるかないか    
    matrix = board.wall_make(17,17)#壁を行列に配置
    while True:
        screen.fill(board.WHITE)
        board.m_rect(screen,bx,by,bw,bh,board.BROWN)
        matrix=board.wall(matrix_b,matrix,17,17,ww,wh,bx,by,screen,bw,bh,5,1)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game ==0:
                        for i,rects in enumerate(matrix):
                            for j,rect in enumerate(rects):
                                if isinstance(rect, int) == False:
                                    if rect.collidepoint(event.pos):
                                        if i%2 != 0 and j%2 == 0:
                                            wallORsq(matrix_b,i,j,phase)
                                        elif i%2 == 0 and j%2 != 0:
                                            wallORsq(matrix_b,i,j,phase)
                if event.type == pygame.KEYDOWN:
                    if game == 0:
                        phase += 1
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if game == 0:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            d=0
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            d=1
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            d=2
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            d=3  
                        else:
                            d=4#moveの中にdが必要なため捨て値として
                            phase -=1
                            
                        if phase%2 == 0:
                            matrix_b,i1,j1,phase = player.move_mat(i1,j1,matrix_b,d,17,phase)
                            p1x,p1y = player.deci_by_mat(i1,j1,matrix,size)#配列の一に合わせて駒の座標を変更する
                        else:
                            matrix_b,i2,j2,phase = player.move_mat(i2,j2,matrix_b,d,17,phase)
                            p2x,p2y = player.deci_by_mat(i2,j2,matrix,size)#配列の一に合わせて駒の座標を変更する
                    if game == 1 and event.key == pygame.K_r:
                        matrix_b,p1x,p1y,p2x,p2y,phase,game,i1,j1,i2,j2 = start(bx,by,bw,bh,ww,wh)
                                
        p1 = player.m_player(size,p1x,p1y,screen,board.BLACK)
        p2 = player.m_player(size,p2x,p2y,screen,board.WHITE)

        game = win(phase,p1y,p2y,sc_x,sc_y,by,bh,screen)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
