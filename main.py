from pyray import *
from constgol import *
from raylib.colors import *



window = init_window(width, height, "GOL")

pause = True

def draw_board():
    color = BEIGE
    '''for i in range (0,nombre_cellules,2):
        for j in range (0,nombre_cellules,2):
            draw_rectangle(i*taille_case, j*taille_case, taille_case, taille_case, color)
            draw_rectangle((i+1)*taille_case, (j+1)*taille_case, taille_case, taille_case, color)
'''
    for i in range(nombre_cellules):
        draw_line(i*taille_case,0,i*taille_case, height, WHITE)
        draw_line(0,i*taille_case,width,i*taille_case, WHITE)
set_target_fps(fps)



game_state = [[0 for _ in range(nombre_cellules)]for _ in range(nombre_cellules)]
game_state[4][4] = 1
game_state[4][5] = 1
game_state[4][6] = 1
game_state[0][0] = 1

game_state[nombre_cellules-1][nombre_cellules-1] = 1
print(f"nombre de cellules {nombre_cellules}")
#print(game_state)

pause_timer = 20
click_timer = 20

def does_live(i, j):
    nombres_voisins = sum([game_state[i-1][j+h] for h in [-1, 0, 1]])
    nombres_voisins += sum([game_state[i+1][j+h] for h in [-1, 0, 1]])
    nombres_voisins += sum([game_state[i][j+h] for h in [-1, 1]])
    alive = (game_state[i][j] == 1)
    return (nombres_voisins == 3) or (alive and nombres_voisins == 2)

def update_grid():
    g_result = [[0 for _ in range(nombre_cellules)]for _ in range(nombre_cellules)]
    for i in range(1,nombre_cellules-1):
        for j in range(1,nombre_cellules-1):
            if does_live(i,j):
                g_result[i][j] = 1
    return g_result

def draw_grid():
    for i in range(nombre_cellules):
        for j in range(nombre_cellules):
            if game_state[i][j] == 1:
                draw_rectangle(i*taille_case, j*taille_case, taille_case, taille_case, WHITE)

def convert_coordinates(vector):
    return int(vector.x/taille_case),int(vector.y/taille_case)

space_was_hold = False
clicked_cells = []

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    draw_board()
    if not pause:
        game_state = update_grid()
    draw_grid()


    if is_mouse_button_down(MOUSE_BUTTON_LEFT) :
        if True: #click_timer == 0
            x, y = convert_coordinates(get_mouse_position())
            #click_timer = 20
            if not (x,y) in clicked_cells:
                clicked_cells.append((x,y))
                if game_state[x][y] == 0:
                    game_state[x][y] = 1
                else:
                    game_state[x][y] = 0

    else :
        if clicked_cells != []:
            clicked_cells = []

    if is_key_down(KEY_SPACE):
        if not space_was_hold:
            pause = not pause
            pause_timer = 20
            space_was_hold = True
    else:
        space_was_hold = False

    if is_key_down(KEY_C):
        game_state = [[0 for _ in range(nombre_cellules)] for _ in range(nombre_cellules)]

    if pause:
        draw_text("paused", 20, 20, 40, WHITE)

    end_drawing()

close_window()