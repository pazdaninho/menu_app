import curses
import time

class Todolist:
    "docstring of class"


    def __init__(self, scr):
        # declaring program variables
        # --------------------------------------------------------------------------------------{{{
        self.d, self.y={}, 0
        self.a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~\t "
        self.colors = lambda x: curses.color_pair(x)
        self.main(scr)
        # }}}--------------------------------------------------------------------------------------

    def main(self, scr):
        "docstring of method"

        self.program_colors(scr)
        line = ""
        while True:

            # display list of items
            # ----------------------------------------------------------------------------------{{{
            w = (scr.getmaxyx()[1]//9)*2
            for i in range(len(self.d)):
                item = list(self.d)[i]
                # True         or           False
                n = 2 if self.d[item] else 1
                line = f'{i+1}) {item} | {str(self.d[item]):5}'
                scr.addstr(i, w, f"{line:{w}}", self.colors(n))
            # }}}----------------------------------------------------------------------------------

            # display selected item
            # {{{----------------------------------------------------------------------------------
            if len(self.d) > self.y:
                line = f"{str(self.y+1)+ ')' + repr(list(self.d)[self.y])}"
            else:
                line = f"{self.y+1})"
            #scr.addstr(self.y, w, f"{line:{w}}")
            self.clrdis_line(scr, f"{line:{w}}", h=self.y)
            self.clrdis_line(scr, "[d]elete [number]", h=len(self.d)+1)
            # }}}----------------------------------------------------------------------------------



            # press arrow 
            # {{{----------------------------------------------------------------------------------
            pressed_key = scr.getkey()
            if pressed_key in ('KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT'):
                # line 88
                self.press_arrow(pressed_key)
            # }}}
            # press enter
            # {{{----------------------------------------------------------------------------------
            elif pressed_key == '\n':
                if len(self.d) == 0:
                    self.insert_mode(scr)
                elif len(self.d) != self.y:
                    # self.y = 1 gdy list(self.d) = [' '] index 0
                    k = list(self.d)[self.y]
                    self.d[k] = not self.d[k]
            # }}}----------------------------------------------------------------------------------
            # press a letter
            # {{{-------------------------------------------------------------------------------
            elif pressed_key in self.a_z:
                if len(self.d) == self.y:
                    # pressed_key is first letter
                    self.insert_mode(scr, pressed_key)
                else:
                    self.insert_mode(scr, list(self.d)[self.y]+pressed_key)

            # }}}----------------------------------------------------------------------------------
            
            # display options

            scr.addstr(scr.getmaxyx()[0]-1, 16, f"{self.y+1}")


    def clrdis_line(self, scr, line, n=1, h=0):
        w = (scr.getmaxyx()[1]//9)*2
        scr.addstr(h, w, f"{'':{w}}", self.colors(4))
        scr.addstr(h, w, line, self.colors(n))

    def insert_mode(self, scr, item=''):
        "docstring of method enter_item"
        
        scr.addstr(scr.getmaxyx()[0]-1, 0, "INSERT")
        while True:
            w = (scr.getmaxyx()[1]//9)*2
            line = f'{self.y+1}) {repr(item)}'
            self.clrdis_line(scr, f'{line}', h=self.y)


            key = scr.getkey()
            # press backspace
            # {{{----------------------------------------------------------------------------------
            if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                item = item[:-1]
            # }}}----------------------------------------------------------------------------------
            # press enter
            #{{{-----------------------------------------------------------------------------------
            elif key in '\n':
                if item in list(self.d):
                    scr.addstr(len(self.d)+1, 0, f'{repr(item)} juz istnieje')
                else:
                    scr.addstr(scr.getmaxyx()[0]-1, 0, "SELECT")
                    self.y += 1
                break
            #}}}-----------------------------------------------------------------------------------
            # press letter
            # {{{----------------------------------------------------------------------------------
            elif key in self.a_z:
                item += key
            # }}}----------------------------------------------------------------------------------

        # exit insert mode
        # {{{--------------------------------------------------------------------------------------
        # add item to self.d
        if len(self.d) == self.y-1:
            self.d[item] = False
        # replace item
        else:
            oldkey = list(self.d)[self.y-1]
            self.d[item] = self.d.pop(oldkey)
        # }}}--------------------------------------------------------------------------------------


    def press_arrow(self, key):
        "docstring press arrow"
        if key == 'KEY_UP':
            if self.y > 0:
                self.y -= 1
        if key == 'KEY_DOWN':
            if self.y < len(self.d):
                self.y += 1

    def program_colors(self, scr):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

curses.wrapper(Todolist)
print(Todolist.main.__doc__)
