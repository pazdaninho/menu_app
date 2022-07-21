import curses
import time
import sys
import json
import os

from modules.snake import Snake
from modules.snapshot_ls import Snapshot
from modules.move import Move



class Menu(Move):
    def __init__(self):
        Move.__init__(self)

        self.t1 = {'a':True, 'b':False, 'c':True}
        self.t2 = {'d':True, 'e':False, 'f':True}
        self.t3 = {'g':True, 'h':False, 'i':True}
        self.t4 = {'j':True, 'k':False, 'l':True}


    # menu what displayes menu
    def main(self, scr): 
        """
        first level in app
        """

        # content
        self.content = { 
                "start": [
                    {"start1"},
                    {'start2'},
                    {'start3'},
                    {'start4'}
                ],
                "todolist": [
                    {f"{list(self.t1)}": lambda: self.clicked_tile(scr, 0)},
                    {f"{list(self.t2)}": lambda: self.clicked_tile(scr, 1)},
                    {f"{list(self.t3)}": lambda: self.clicked_tile(scr, 2)},
                    {f"{list(self.t4)}": lambda: self.clicked_tile(scr, 3)},
                ],
                "snake": [
                    {"launch snake": lambda: [s:= Snake(Move()), s.main(scr)]},
                    {},
                    {},
                    {}
                ],
                "snapshot_ls": [
                    [s := Snapshot(self.c['snapshot_ls']), s.compare_jsons([-2, -1])][-1],
                    [s := Snapshot(self.c['snapshot_ls']), s.compare_jsons([-3, -2])][-1],
                    {},
                    {"edit config snapshot_ls"}
                ]
            }

        while True:
            try:
                curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
                curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLUE)
                curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
                curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
                curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
                self.display_menu(scr) 

                # conditions for move arrows
                l = [self.y>0,self.y<2, self.x>0,self.x<len(self.content)-1]
                self.key = self.press_key(scr, l)
                if self.key:
                    self.pressed_a_key(scr)
            except KeyboardInterrupt:
                break


    # enter tile
    def clicked_tile(self, scr, n):
        """
        third level in app
        main -> tiles_for_cat -> clicked_tile
        """
        win = self.wins[n]
        d = eval(f"self.t{n+1}")
        # execute app in tile
        d = self.tile_app(scr, win, d=d)

    # display menu
    def display_menu(self, scr):
        self.clear_board(scr)

        # display topbar
        menu_str = "/0) start      /1) todolist   /2) snake      /3) snapshot_ls"
        scr.addstr(0,0,menu_str, curses.color_pair(1))

        # mark selected option
        if self.y == 0:
            start_index = menu_str.find(str(self.x))-1
            end_index = menu_str.find(str(self.x+1))-2
            scr.addstr(0, start_index, menu_str[start_index:end_index], curses.color_pair(2))

            #key = list(self.content)[self.x]
            self.category = list(self.content)[self.x]

            self.display_tiles(scr, 
                    t1=self.content[self.category][0],
                    t2=self.content[self.category][1],
                    t3=self.content[self.category][2],
                    t4=self.content[self.category][3],
            )

        # mark hovering tile
        if self.y > 0:
            self.tiles_for_cat(scr)


    # action in tile
    def tiles_for_cat(self, scr):
        """
        second level in app
        main -> tiles_for_cat
        """
        beg = self.x
        self.x = 0 
        while True:

            self.display_tiles(scr, 
                    t1=self.content[self.category][0],
                    t2=self.content[self.category][1],
                    t3=self.content[self.category][2],
                    t4=self.content[self.category][3],
            )

            key = self.press_key(scr, cnds=[self.y>0,self.y<2, self.x>0,self.x<1])
            if self.y==0:
                break
            if type(key)!= bool and ord(key) == 10:

                if type(self.content[self.category][2*(self.y-1) + self.x]) == dict:
                    d = self.content[self.category][2*(self.y-1) + self.x]
                    for value in d.values():
                        value()

        self.x = beg


    # press a key
    def pressed_a_key(self,scr):

        # ESCAPE key
        if ord(self.key) == 27:
            sys.exit()
        
        # ENTER key
        #elif self.key == "KEY_ENTER":
        elif ord(self.key) == 10:

            # launching app in tile
            if type(self.content[self.category][self.y + self.x]) == dict:
                d = self.content[self.category][self.y + self.x]
                for value in d.values():
                    value()

    def get_config(self):
        if 'config.json' not in os.listdir():
            d = {'snapshot_ls':['/home'], 'snake':[], 'todolist':[],}
            json.dump(d, open('config.json', 'w', encoding='utf-8'))
        self.c = json.load(open('config.json', encoding='utf-8'))


if __name__ == '__main__':
    m = Menu()
    m.get_config()
    curses.wrapper(m.main)
    #m.main()
