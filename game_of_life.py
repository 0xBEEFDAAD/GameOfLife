# -*- coding: utf-8 -*-
#
# Game of life
# see https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

from time import sleep

class GameOfLife():
    """Conway's Game Of Life as a Python class """
    MIN_SIZE    = 12
    DESCRIPTION = ""
    EMPTY       = 0
    RULES       = "23.3"
    
    def __init__(self,
                 width       =   64,
                 height      =   64,
                 generations = 2000,
                 delay       =    0.1,
                 rules       = RULES):
        self.width       = (GameOfLife.MIN_SIZE                   \
                            if   int(width )<GameOfLife.MIN_SIZE  \
                            else int(width))
        self.height      = (GameOfLife.MIN_SIZE                   \
                            if   int(height)<GameOfLife.MIN_SIZE  \
                            else int(height))
        self.generations = (2 if int(generations)<2 else int(generations))
        self.delay       = float(delay)
        self.rules_alive = ""
        self.rules_dead  = ""
        try:
            rules = str  (rules).split(".")
            self.rules_alive = rules[0]
            self.rules_dead  = rules[1]
        except:
            print("WARNING: invalid rules!")
        self.create()

    def create(self, description = ""):
        """ create a new, empty area """
        col              = [GameOfLife.EMPTY]*self.height
        self.area        = [col.copy() for x in range(self.width)]
        self.description = str(description)
        self.patternlist = [""]

    def pattern(self, x, y, pattern, modifier=""):
        """ add a pattern to the area """
        pat      = pattern.split("\n")
        modifier = modifier.upper()
        longest  = 0

        #remove empty lines at the top
        while len(pat[0].strip()) == 0:
            pat = pat[1:]

        #remove empty lines at the bottom
        while len(pat[-1].strip()) == 0:
            pat = pat[:-1]
            
        # equalize line length for correct modifications
        for line in pat:
            if len(line)>longest:
                longest = len(line)
        for l in range(len(pat)):
            if len(pat[l])<longest:
                pat[l] += " " * (longest-len(pat[l]))

        # rotate pattern
        if "R" in modifier:
            rot = []
            for p in range(longest):
                l = ""
                for q in range(len(pat)):
                    l += pat[q][p]
                rot = [l] + rot
            pat = rot

        # flip horizontally
        if "H" in modifier:
            pat.reverse()
        
        self.patternlist.append("")
        self.patternlist.append("Pattern at (%d, %d):" % (x, y))
    
        m = 0
    
        for line in pat:
            # flip vertically: invert every single line
            if "V" in modifier:
                line = line[::-1]

            # skip empty lines at the beginning
            # (possible after rotation)
            if (m==0) and (len(line.strip())==0):
                continue

            # printable presentation for patternlist
            pl = ""
            for ch in line:
                if ch == " ":
                    pl += " ."
                else:
                    pl += " " + ch
            self.patternlist.append(pl)

            # add pattern to area
            n = 0
            for c in line:
                if c in "#*+xX":
                    self.area[(x+n)%self.width][(y+m)%self.height] = 1
                n+=1
            m+=1

    def neighbour_column(self, column):
        """ create list of sums from a single column """
        prev = column[self.height-1]
        this = column[0]
        next = column[1]
        nr = []
        nr.append(prev+this+next)
        for y in range(1, self.height-1):
            prev = this
            this = next
            next = column[y+1]
            nr.append(prev+this+next)
        nr.append(this+next+column[0])
        return nr

    def neighbours(self):
        """ create a table with the number of neighbours """
        prev = self.neighbour_column(self.area[self.width-1])
        this = self.neighbour_column(self.area[0])
        next = self.neighbour_column(self.area[1])
        n = []
        for x in range(self.width):
            cprev = self.area[x][self.height-1]
            cthis = self.area[x][0]
            cnext = self.area[x][1]
            nl = []
            nl.append(prev[0]+cprev+cnext+next[0])
            for y in range(1, self.height-1):
                cprev = cthis
                cthis = cnext
                cnext = self.area[x][y+1]
                nl.append(prev[y]+cprev+cnext+next[y])
            nl.append(prev[self.height-1]   + \
                      cthis+self.area[x][0] + \
                      next[self.height-1]     )
            n.append(nl)
            prev = this
            this = next
            next = self.neighbour_column(self.area[(x+2)%self.width])
        return n

    def tick(self):
        """ proceed to the next generation """
        n = self.neighbours()
        generation = []
        for x in range(self.width):
            column = []
            for y in range(self.height):
                cell_alive = GameOfLife.EMPTY != self.area[x][y]
                cell_neigh = str(n[x][y])
                if cell_alive:
                    column.append((1 if cell_neigh in self.rules_alive else 0))
                else:
                    column.append((1 if cell_neigh in self.rules_dead  else 0))
            generation.append(column)
        return generation

    def print_area(self):
        """ print the current area to the console """
        for y in range(self.height):
            l = ""
            for x in range(self.width):
                e = self.area[x][y]
                l += (" ." if e==GameOfLife.EMPTY else " #")
            print (l)

    def play(self):
        """ execute the game of life """
        print ("\n"*100)
        print ("""

  #####  ####  ##   ## ######    #####  ######   #     #  ##### #####
 #      #    # # # # # #        #     # #        #     #  #     #
 #      #    # #  #  # #        #     # #        #     #  #     #
 # #### ###### #     # ####     #     # ####     #     #  ####  ####
 #    # #    # #     # #        #     # #        #     #  #     #
 #    # #    # #     # #        #     # #        #     #  #     #
  ####  #    # #     # ######    #####  #        ##### #  #     #####
     


""")
        print ("     " + self.description)
        for p in self.patternlist:
            if len(p)==0:
                sleep(3*self.delay)
            print (p)
        print("")
        
        sleep(30*self.delay)

        for gen in range(self.generations+1):
            print ("\n"*25+"======GENERATION %04d======" % gen)
            self.print_area()
            NEWGEN = self.tick()
            if NEWGEN == self.area:
                print (" " + "="*26+"\n"                            \
                       " reached tranquility after %d generation%s" \
                       % (gen, ("" if gen==1 else "s")))
                break
            self.area = NEWGEN
            sleep(self.delay)
        sleep(30*DELAY)

######## PATTERNS ############

#Still life
BLOCK = """
##
##
"""

BEEHIVE = """
 ##
#  #
 ##
"""

LOAF = """
 ##
#  #
 # #
  #
"""

BOAT = """
##
# #
 #
"""

TUB = """
 #
# #
 #
"""

#Oscillators
BLINKER = "###"

TOAD = """
 ###
###
"""

BEACON = """
##
##
  ##
  ##
"""

PULSAR = """
  ###   ###

#    # #    #
#    # #    #
#    # #    #
  ###   ###

  ###   ###
#    # #    #
#    # #    #
#    # #    #

  ###   ###
"""

PENTADECATHLON = """
 #
 #
# #
 #
 #
 #
 #
# #
 #
 #
"""

#Spaceships
GLIDER = """
# #
 ##
 #
"""

LWSS = """
  ##
## ##
####
 ##
"""

MWSS = """
   ##
### ##
#####
 ###
"""

HWSS = """
    ##
#### ##
######
 ####
"""

#Metusaleahs
R_PENTOMINO = """
 ##
##
 #
"""

DIEHARD = DIE_HARDT = """
      #
##
 #   ###
"""

ACORN = """
 #
   #
##  ###
"""

# Additional Patterns
BLOCKBUILDER = """
## ##
#   #

#   #
## ##
"""

#Other patterns

GOSPER_GLIDER_GUN = """
                        #
                      # #
            ##      ##            ##
           #   #    ##            ##
##        #     #   ##
##        #   # ##    # #
          #     #       #
           #   #
            ##
"""

SIMKIN_GLIDER_GUN = """
##     ##
##     ##

    ##
    ##




                      ## ##
                     #     #
                     #      #  ##
                     ###   #   ##
                          #



                    ##
                    #
                     ###
                       #
"""

GROWTH_PATTERN_A = """
      #
    # ##
    # #
    #
  #
# #
"""

GROWTH_PATTERN_B = """
### #
#
   ##
 ## #
# # #
"""

GROWTH_PATTERN_C = "######## #####   ###      ####### #####"

#DEMO: Still lifes and Oscillators
#pattern( 4,  4, BLOCK)
#pattern( 4, 10, BEEHIVE)
#pattern( 4, 16, LOAF)
#pattern( 4, 22, BOAT)
#pattern( 4, 28, TUB)

#pattern(14,  4, BLINKER)
#pattern(14, 10, TOAD)
#pattern(14, 16, BEACON)
#pattern(14, 28, PENTADECATHLON)
#pattern(34,  4, PULSAR)

#DEMO: Spaceship race (WARNING! Graphic scenes! Massive crash!)
#pattern( 4,  4, LWSS)
#pattern( 4, 14, MWSS)
#pattern( 4, 24, HWSS)
#pattern( 4, 34, GLIDER)
#pattern( 54, 34, GLIDER)

#DEMOS (one pattern at once!
#pattern( 30, 30, R_PENTOMINO)
#pattern( 30, 30, DIEHARD)
#pattern( 30, 30, ACORN)

#SCENARIO: Glider crashes into block
#pattern( 4,   4, GLIDER)
#pattern( 20, 24, BLOCK)

#SCENARIO: Lightweight Spaceship crashes into Pentadecathlon
#pattern(40, 20, PENTADECATHLON)
#pattern( 4, 26, LWSS)

#SCENARIO: Heavyweight Spaceship crashes into Pentadecathlon
#pattern(40, 20, PENTADECATHLON)
#pattern( 4, 26, HWSS)

#VARIATIONS: R=ROTATE, H=FLIP HORIZONTALLY, V=FLIP VERTICALLY
#pattern(20, 20, GLIDER, "RV")
#pattern(26, 20, GLIDER, "H")
#pattern(20, 26, GLIDER, "V")
#pattern(26, 26, GLIDER, "")

if __name__ == "__main__":
    HAZARD = """
  ####
 #
 # ##
 # ##
 #
"""
    gol = GameOfLife()
    gol.create("some test")
    gol.pattern(10, 10, HAZARD)
    gol.pattern(23, 10, HAZARD, "V")
    gol.pattern(18, 18, PENTADECATHLON)
    gol.pattern(10, 31, HAZARD, "H")
    gol.pattern(23, 31, HAZARD, "HV")
    gol.play()
    #game_of_life()
