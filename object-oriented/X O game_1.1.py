from board_class import *
from player_class import *
import pygame
import sys
board = Board()
player =Player()
#勝利している側がどっちかをぶっこむ関数
def con():
    if matrix[a][b] == matrix[a][b] and matrix[a][b] == matrix[a][b]:
        if matrix[a][1] == 2:
            player.wtx("バツ")
        elif matrix[a][1] == 3:
            player.wtx("マル")
            
#勝利しているかどうかをチェックする関数
def check(matrix,screen,scx,scy,matrix_w,win):
    for a in range(7):
        for b in range(7):
            if a%2 != 0 and b%2 != 0:
                if matrix[a][1] != 0 and matrix[a][1] == matrix[a][3] and matrix[a][3] == matrix[a][5]:
                    matrix_w = OorX(screen,scx,scy,matrix,a,1,matrix_w)
                    win = 1
                elif matrix[1][a] != 0 and matrix[1][a] == matrix[3][a] and matrix[3][a] == matrix[5][a]:
                    matrix_w = OorX(screen,scx,scy,matrix,1,a,matrix_w)
                    win = 1
                elif matrix[1][1] != 0 and matrix[1][1] == matrix[3][3] and matrix[3][3] == matrix[5][5]:
                    matrix_w = OorX(screen,scx,scy,matrix,1,1,matrix_w)
                    win = 1
                elif matrix[1][5] != 0 and matrix[1][5] == matrix[3][3] and matrix[3][3] == matrix[5][1]:
                    matrix_w = OorX(screen,scx,scy,matrix,1,5,matrix_w)
                    win  =1
    return(matrix_w,win)
#勝利画面を表示する
def OorX(screen,scx,scy,matrix,a,b,matrix_w):
    if matrix[a][b] == 3 or matrix[a][b] == 2:
        matrix_w = []
        if matrix[a][b] == 3:
            board.wtx("バツ",screen,scx,scy)
        else:
            board.wtx("マル",screen,scx,scy)
        return(matrix_w)
def restart():
    matrix_w =[[0 for _ in range(7)] for _ in range(7)] #rectを格納する行列
    matrix_b =[[0 for _ in range(7)] for _ in range(7)] #0の時は空白、1のときは壁、2の時✕、3のとき〇
    matrix_b = board.edge(matrix_b,7,7) 
    phase = 0
    win =0 
    for i in range(7):
        if i%2 != 0:
            continue
        else:
            matrix_b[i][6] = 0
    return(matrix_w,matrix_b,phase,win)
def main():
    joke = 0
    pygame.init()
    win = 0#クリックされたときに勝利してるかチェックする
    scx,scy = board.basic_screen
    screen, caption = board.m_screen(scx,scy,"X and O")
    screen.fill(board.WHITE)
    bx, by= 400,150
    bwidth = 600
    gwidth = 200
    board.m_rect(screen,bx,by,bwidth,bwidth,board.PALE_YELLOW)
    matrix_w =[[0 for _ in range(7)] for _ in range(7)] #rectを格納する行列
    matrix_b =[[0 for _ in range(7)] for _ in range(7)] #0の時は空白、1のときは壁、2の時✕、3のとき〇
    matrix_b = board.edge(matrix_b,7,7) 
    phase = 0
    for i in range(7):
        if i%2 != 0:
            continue
        else:
            matrix_b[i][6] = 0
    while True:
        if win == 0:
            matrix_w = board.board_point(matrix_w,bx,by,gwidth,gwidth,screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rects in enumerate(matrix_w):
                    clicked = False
                    for j, rect in enumerate(rects):
                        if type(rect) != int:
                            if rect.collidepoint(event.pos) and i%2 != 0 and j%2 != 0 and win == 0:
                                clicked = True
                                if matrix_b[i][j] == 0:
                                    phase += 1
                                    if phase%2 == 0:
                                        matrix_b[i][j] = 3                                    
                                    else:
                                        matrix_b[i][j] = 2                                    
                                break
                    if clicked:
                        break                                
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and win == 1:
                    matrix_w,matrix_b,phase,win = restart()
        for i in range(7):
            for j in range(7):
                if matrix_b[i][j] == 2:
                    player.m_player_O(screen,bx+15,by+15,i,j,gwidth,180,20)
                elif matrix_b[i][j] == 3:
                    player.m_player_X(screen,bx+15,by+15,i,j,gwidth,180,20)
        if win == 0:
            board.wall(matrix_b,matrix_w,7,7,200,10,400,150,screen,600,600,10,0)
        matrix_w,win = check(matrix_b,screen,scx,scy,matrix_w,win)
        pygame.display.update()

if __name__ == "__main__":
    main()
