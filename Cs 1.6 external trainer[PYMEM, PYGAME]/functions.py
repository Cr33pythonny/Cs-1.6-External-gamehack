from offsets import *
from windowGUI import *
from time import sleep
from math import sqrt
from config_parser import get_current_weapon,get_value_from_cfg
import keyboard

def read_resolution():
    w = pm.read_int(hw+HWResolution)
    h = pm.read_int(hw+HWResolution + 4)
    return w,h

def updateent():
    while True:
        sleep(0.5)
        for i in range(32):
            pm.write_int(hw + HWEntity + 376 + 592 * i,0)

def bhop():
    while True:
        onair = pm.read_int(hw + 0x13CE44)
        if keyboard.is_pressed('space'):
            if onair != -1:
                pm.write_int(client + 0x131434,5)
                sleep(0.008)
                pm.write_int(client + 0x131434,4)

def ddrun():
    while True:
        onair = pm.read_int(hw + 0x13CE44)
        fps = pm.read_float(hw + 0x149CF4)
        if keyboard.is_pressed('ctrl'):
            if onair !=-1:
                pm.write_float(hw + 0x149D5C,float(1)) # override
                pm.write_float(hw + 0x149CF4,float(999)) # fps
                for i in range(999):
                    pm.write_int(client + 0x1313B0,5)
                    pm.write_int(client + 0x1313B0,4)
        else:
            if fps> 100:
                pm.write_float(hw + 0x149CF4,float(100))

def parse_matrix(matrix_resolution):
    matrix = []
    for i in range(matrix_resolution):
        mat0 = pm.read_float(hw + HWview_matrix + 4 * i)
        matrix.append(mat0)
    return matrix



def w2s(x,y,z,w,h):
    matrix = parse_matrix(4*4)
    fovx = matrix[0] * x + matrix[4] * y + matrix[8] * z + matrix[12]
    fovy = matrix[1] * x + matrix[5] * y + matrix[9] * z + matrix[13]
    fovz = matrix[3] * x + matrix[7] * y + matrix[11] * z+ matrix[15]
    if fovz < 0.01:
        return False
    nx = fovx / fovz
    ny = fovy / fovz
    screenx = (w/2 * nx) + (w/2 + nx)
    screeny = -((h/2 * ny) - (h/2 + ny)) 
    return screenx,screeny
  
        
def read_players():
    players = []
    for i in range(32):
        vec3 = []
        x=pm.read_float(hw + HWEntity + 388+ 592 * i) 
        y=pm.read_float(hw + HWEntity + 392+ 592 * i)
        z=pm.read_float(hw + HWEntity + 396+ 592 * i)
        vec3.append(x)
        vec3.append(y)
        vec3.append(z)
        players.append(vec3)
    return players


def players_team():
    teams = []
    for i in range(32):
        m =pm.read_string(hw+HWEntity + 300 + 592 * i)
        if m == 'leet' or m == 'terror' or m == 'guerilla' or m == 'arctic':
            teams.append(1) 
        elif m == 'gign' or m == 'sas' or m == 'urban' or m == 'gsg9'or m == 'vip':
            teams.append(2)
        else:
            teams.append(3)
    return teams
        
def read_val():
    values = []
    for i in range(32):
        val = pm.read_float(hw + HWEntity + 376 + 592 * i)
        values.append(val)
    return values



def calc_dist(enemy_x,enemy_y,enemy_z):
    my_x = pm.read_float(hw + HWVec3)
    my_y = pm.read_float(hw + HWVec3 + 4)
    my_z = pm.read_float(hw + HWVec3 + 8)
    delta_x = enemy_x - my_x
    delta_y = enemy_y - my_y
    delta_z = enemy_z - my_z
    return sqrt(delta_x*delta_x + delta_y * delta_y + delta_z * delta_z)

def calc_scalling(w,h,distance,factor):
    aspect =pm.read_float(hw + hwZOOMING)
    if aspect > 1:
        w *=aspect
        h *= aspect
    try:
        return w / distance * factor,h / distance * factor
    except(ZeroDivisionError,TypeError): return False


def get_distance(screen,w,h):
    crosshairX,crosshairY =w/2,h/2
    distx = screen[0] - crosshairX 
    disty = screen[1] - crosshairY
    return distx,disty
    

def get_targets():
        targets = []              
        players = read_players()
        teams = players_team()
        val = read_val()
        my_team = pm.read_int(client + CLMyTeamNumber)
        for i in range(len(players)):
            if teams[i] != my_team and val[i] !=0:
                targets.append(players[i])
        return targets


def find_best_target(targets:list,w,h):
    nearest_index = -1
    min_dist = 99999
    for i in range(len(targets)):
        screen = w2s(targets[i][0],targets[i][1],targets[i][2] + 18,w,h)
        if screen:
            distx,disty = get_distance(screen,w,h)
            dist = sqrt(distx * distx + disty * disty)
            if dist < min_dist:
                min_dist = dist
                nearest_index = i
    return nearest_index

    
def AIMBOT():
    while True:
        sleep(0.01)
        w,h = read_resolution()              
        targets = get_targets()
        nearest_index = find_best_target(targets,w,h)

        WEAPON_ID = pm.read_int(client + 0x125F10)
        current_weapon = get_current_weapon(WEAPON_ID)
        fov = get_value_from_cfg('FOV',current_weapon)
        smooth = get_value_from_cfg('SMOOTH',current_weapon)
        rcs = get_value_from_cfg('RCS',current_weapon)
        SCALEFACTOR = get_value_from_cfg('SCALEFACTOR',current_weapon)
        recoil_y = pm.read_float(hw + 0x108AED0)
        recoil_x = pm.read_float(hw + 0x108AED0 + 4)

        if nearest_index != -1:
            dist = calc_dist(targets[nearest_index][0],targets[nearest_index][1],targets[nearest_index][2] + 18)
            screen = w2s(targets[nearest_index][0],targets[nearest_index][1],targets[nearest_index][2] + 18,w,h)

            scalling = calc_scalling(fov,fov,dist,SCALEFACTOR)
            if screen and scalling:
                REC = (screen[0] + recoil_x * rcs,screen[1] +abs(recoil_y) * rcs)
                distx,disty =get_distance(REC,w,h)
                distx /= smooth
                disty /=smooth
                if abs(distx) <= scalling[0] and abs(disty) <= scalling[1] and win32api.GetAsyncKeyState(0x01) & 0x8000:
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(distx), int(disty), 0, 0)  
    
    


def ESP():
    while True:
        sleep(0.01)
        resolution = read_resolution()    
        display =set_window_gui(resolution[0],resolution[1])           
        players = read_players()
        teams = players_team()
        val = read_val()
        my_team = pm.read_int(client + CLMyTeamNumber)
        for i in range(len(players)):
            
            if teams[i] != my_team and val[i] !=0:
                dist = calc_dist(players[i][0],players[i][1],players[i][2])
                screen = w2s(players[i][0],players[i][1],players[i][2],resolution[0],resolution[1])
                scalling = calc_scalling(15,25,dist,resolution[0])
                if screen and scalling:
                    try:
                        DrawBox(display,GREEN,screen[0],screen[1],scalling[0],scalling[1],1)
                    except(TypeError): continue  
            

        pygame.display.update()     
        




  
    

    
      

    
   
