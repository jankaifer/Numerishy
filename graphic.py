#! /bin/env python3

import curses, time, random
from curses import wrapper
from math import floor

class Display:
    
    width, height = None, None
    screen_map = None
    new_screen_map = None
    changed = False
    colors = {("green", "black"): 1}
    
    special_keys = {258: "down",
                    259: "up",
                    260: "left",
                    261: "right"}


    def __init__(self):
        pass
    
    def clear_new_map(self):
        self.new_screen_map = [[(" ", 0) for _ in range(self.width)] for _ in range(self.height)]
    
    def apply_new_map(self):
        if not self.changed:
            return
        for y in range(self.height):
            buffered_text = ""
            buffered_x = 0
            buffered_y = y
            buffered_flag = 0
            for x in range(self.width):
                
                if self.screen_map[y][x] != self.new_screen_map[y][x]:
                    if not buffered_text:
                        buffered_text = self.new_screen_map[y][x][0]
                        buffered_x = x
                        buffered_y = y
                        buffered_flag = self.new_screen_map[y][x][1]
                    else:
                        buffered_text += self.new_screen_map[y][x][0]
        
                if buffered_text and (x+1 == self.width or \
                                      self.screen_map[y][x+1][0] == self.new_screen_map[y][x+1][0] or \
                                      self.new_screen_map[y][x][1] != self.new_screen_map[y][x+1][1]):
                    self.stdsrc.addstr(buffered_y, buffered_x, buffered_text, buffered_flag)
                    for i, ch in enumerate(buffered_text):
                        self.screen_map[buffered_y][buffered_x+i] = (buffered_text[i], buffered_flag)
                    buffered_text = ""



        self.stdsrc.refresh()
        self.screen_map = self.new_screen_map
        self.clear_new_map()
        

    def init_screen(self):
        self.height, self.width = (item-1 for item in self.stdsrc.getmaxyx())
        self.clear_new_map()
        self.screen_map = self.new_screen_map
        self.clear_new_map()
    
    def show(self, x, y, text, flag=0):
        text = text
        i = 0
        if x<0 and -x<len(text):
            text = text[min(-x, len(text)-1):]
            x=0
        while 0 <= x+i < self.width and i < len(text) and 0 <= y < self.height:
            if not self.changed and self.new_screen_map[y][x+i] != text[i]:
                self.changed = True
            self.new_screen_map[y][x+i] = (text[i], flag)
            i += 1
    
    def user_main(self):
        raise NotImplementedError

    def main_loop(self, stdsrc):
        self.stdsrc = stdsrc

        curses.curs_set(0)
        for color in self.colors:
            curses.init_pair(self.colors[color], getattr(curses, "COLOR_%s" % color[0].upper()), getattr(curses, "COLOR_%s" % color[1].upper()))
        self.stdsrc.nodelay(True)

        self.init_screen()

        self.stdsrc.addstr(self.height, 0, "#"*self.width)
        for y in range(self.height):
            self.stdsrc.addstr(y, self.width, "#")

        while True:
            self.user_main(self)
        
    def run(self, main):
        self.user_main = main
        wrapper(self.main_loop)

    def refresh(self):
        self.apply_new_map() 

    def get_color(self, color):
        return curses.color_pair(self.colors[color])

    def get_key(self):
        key = self.stdsrc.getch()
        curses.flushinp()
        if key == -1:
            return None
        elif 0 <= key < 256:
            return chr(key)
        elif key in self.special_keys:
            return self.special_keys[key]
        else:
            return key


