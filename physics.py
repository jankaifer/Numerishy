#! /bin/env python3

from time import time
from math import floor

class Numb:
    default_max_enemy = +50
    default_min_enemy = -10
    
    def __init__(self, items=10, x=0, y=0, flag=0, speed=(0, 0)):
        self.items = items
        self.x, self.y = x, y
        self.real_x, self.real_y = x, y
        self.flag = flag
        self.speed_x = speed[0]
        self.speed_y = speed[1]
        self.last_moved = time()

    def __and__(self, other, second=False):
        if not isinstance(other, Numb):
            raise TypeError("Trying to test collision with wrong object.")
        else:
            spos1, spos2 = self.get_hitbox()
            opos1, opos2 = other.get_hitbox()

            smaxx = max(spos1[0], spos2[0]) 
            smaxy = max(spos1[1], spos2[1]) 
            sminx = min(spos1[0], spos2[0]) 
            sminy = min(spos1[1], spos2[1]) 

            omaxx = max(opos1[0], opos2[0]) 
            omaxy = max(opos1[1], opos2[1]) 
            ominx = min(opos1[0], opos2[0]) 
            ominy = min(opos1[1], opos2[1]) 

            return (ominx<=sminx<=omaxx and ominy<=sminy<=omaxy) or \
                   (ominx<=sminx<=omaxx and ominy<=smaxy<=omaxy) or \
                   (ominx<=smaxx<=omaxx and ominy<=sminy<=omaxy) or \
                   (ominx<=smaxx<=omaxx and ominy<=smaxy<=omaxy) or \
                                                                    \
                   (sminx<=ominx<=smaxx and sminy<=ominy<=smaxy) or \
                   (sminx<=ominx<=smaxx and sminy<=omaxy<=smaxy) or \
                   (sminx<=omaxx<=smaxx and sminy<=ominy<=smaxy) or \
                   (sminx<=omaxx<=smaxx and sminy<=omaxy<=smaxy)
                    
    
    def __lt__(self, other):
        return self.get_size() <  other.get_size()
        
    
    def __le__(self, other):
        return self.get_size() <= other.get_size()
    
    def __ne__(self, other):
        return self.get_size() != other.get_size()
    
    def __ge__(self, other):
        return self.get_size() >= other.get_size()
    
    def __gt__(self, other):
        return self.get_size() >  other.get_size()
    

    
    def die(self):
        return [self.items]
    
    def eat(self, items):
        self.items += len(items)
    
    def show(self, disp):
        disp.show(self.x, self.y, self.render(), self.flag)
    
    def render(self):
        return str(self.items)
    
    def get_hitbox(self):
        return ((self.x, self.y), (self.x+len(self.render())-1, self.y))

    def update_xy(self):
        self.x = floor(self.real_x)
        self.y = floor(self.real_y)
    
    def move(self):
        moved_time = time()
        time_diff = moved_time-self.last_moved
        self.last_moved = moved_time
        
        self.real_x += time_diff * self.speed_x
        self.real_y += time_diff * self.speed_y
        
        self.update_xy()
    
    def change_xy(self, x=None, y=None):
        if x is not None: self.real_x += x
        if y is not None: self.real_y += y
        
        self.update_xy();

    def set_xy(self, x=None, y=None):
        if x is not None: self.real_x = x
        if y is not None: self.real_y = y
        
        self.update_xy();
    
    def change_speed(self, x=None, y=None):
        if x is not None: self.speed_x += x
        if y is not None: self.speed_y += y
    
    def set_speed(self, x=None, y=None):
        if x is not None: self.speed_x = x
        if y is not None: self.speed_y = y
    
    def check_board(self, disp):
        hb = self.get_hitbox()
        right = max(hb[0][0], hb[1][0])
        if right >= disp.width:
            self.real_x = self.x + disp.width - 1 - right
        self.update_xy()

        left = min(hb[0][0], hb[1][0])
        if left < 0:
            self.real_x = self.x - left
        self.update_xy()

        up = min(hb[0][1], hb[1][1])
        if up < 0:
            self.real_y = self.y - up
        self.update_xy()

        down = max(hb[0][1], hb[1][1])
        if down >= disp.height:
            self.real_y = self.y + disp.height - 1 - down
        self.update_xy()
    
    def get_size(self):
        return self.items
        

        
