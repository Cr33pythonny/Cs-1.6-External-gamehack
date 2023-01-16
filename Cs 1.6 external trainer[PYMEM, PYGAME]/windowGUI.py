from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import win32api,win32con,win32gui
from colors import*



def Get_cs_window_coords():
    window_handle = win32gui.FindWindow(None, "Counter-Strike")
    window_rect   = win32gui.GetWindowRect(window_handle)
    return window_rect

def DrawBox(display,color,x,y,width,height, thickness):
    lefttopX = x -width /2 
    lefttopY = y -height /2
    pygame.draw.rect(display, color, pygame.Rect(lefttopX, lefttopY, width, height),  thickness)


def set_window_gui(w,h):
        pygame.init()
        wincoord = Get_cs_window_coords()
        DISPLAY=pygame.display.set_mode((w, h), pygame.NOFRAME)
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)# winapi information to hwnd
        #Transparent
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
        
        
        pygame.mouse.set_visible(False)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, wincoord[2] -w -8, wincoord[3] -h -8, 0, 0, win32con.SWP_NOSIZE)
        DISPLAY.fill(fuchsia)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        return DISPLAY


