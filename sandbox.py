import curses
import os
import json
import time


class Snapshot:
    "it does snapshot for selected directories"

    def __init__(self,scr, ls=[]):
        self.tree = {}
        [self.get_tree(d) for d in ls]

    # tree about selected path
    def get_tree(self, path): # {{{
        "It does tree of selected directories"

        # list of directories for path
        dirs = path.split('/')#[1:]
        dirs[0] = '/'

        # go to path in self.tree
        d = self.tree

        # make json' tree through dirs (17 line)
        for key in dirs: # {{{
            # if path doesn't exist
            if key not in list(d):
                # is it new?
                if type(d) == dict:
                    d[key] = []

                # is it exists?
                if type(d) == list: # {{{
                    l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                    if key not in l:
                        d.append( {key: []} )
                        d = d[-1]
                    else:
                        l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                        d = d[l.index(key)] # }}}

            # go to the next dir
            d = d[key] # }}}


        # creating list in dict (directory) or string (file)
        for f in os.listdir(path): # {{{
            try:
                if os.path.isdir(path+'/'+f):
                    #d.append( { f: [] } )
                    self.get_tree(path+'/'+f)
                else:
                    d.append( f )
                    #print(path+'/'+f)
            except PermissionError:
                continue # }}}
    # }}}

    def print_json(self):
        return json.dumps(self.tree, indent=5)

    def save_json(self):
        if 'files' not in os.listdir():
            os.mkdir('files') 
        name = time.strftime("%Y%m%d%H%M%S")
        f = open(f'files/{name}.json', 'w')
        json.dump(self.tree, f, indent=5)
        #f.save()

    def comparsion_old2new(self):
        if len(os.listdir('files')) >= 2:
            old, new = sorted(os.listdir('files'))[-2:]
            print(old,new)

if __name__ == '__main__':
    #curses.wrapper(Menu)
    s = Snapshot('a', ['/home','/etc'])
    s.save_json()
    s.comparsion_old2new()
    #print(m.tree)
    #print(json.dumps(s.tree, indent=5))
