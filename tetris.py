# 1マス 30x30
MINO_T = 0   #1 
MINO_I = 1   #2 
MINO_O = 2   #3 
MINO_L = 3   #4 
MINO_J = 4   #5 
MINO_S = 5   #6 
MINO_Z = 6   #7 
MINO_NUM = 7
MINO_0 = 0
MINO_90 = 1
MINO_180 = 2
MINO_270 = 3
MINO_ALL_ANGLE = 4
MINO_HEIGHT_WIDTH = 4
FIELD_HEIGHT = 20
FIELD_WIDTH = 10


class Field:

    def __init__(self, xo, fmino, tetcanvas):
        self.xoffset = xo
        self.mino = fmino
        self.score = 0
        self.dipfield = []
        self.ctlmlist = []
        self.canvas = tetcanvas

        for y in range(FIELD_HEIGHT+1):
            buf=[]
            for x in range(FIELD_WIDTH+2):
                if y==20:
                    buf.append(1)                
                elif x==0 or x==11:
                    buf.append(1)
                else:
                    buf.append(0)
            self.dipfield.append(buf)
    
    def refresh(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 800, 800, fill='black')
        fx = self.xoffset
        fy = 100
        ex = 411
        ey = 100
        for y in range(21):
            self.canvas.create_line(fx, fy, ex, ey, fill='white')
            fy+=31
            ey+=31

        fx = self.xoffset
        fy = 100
        ex = self.xoffset
        ey = 721
        for x in range(11):
            self.canvas.create_line(fx, fy, ex, ey, fill='white')
            fx+=31
            ex+=31
        self.canvas.place(x=0,y=0)
        
        

    def update(self, mlist, scoretxt):
        self.ctlmlist = mlist 
        self.mino.move(self.ctlmlist, self.dipfield)
        if self.mino.drop(self.dipfield):
            self.checkline()
            scoretxt.set("Score : " + str(self.score))
        self.mino.update(self.dipfield)
        
    
    def draw(self):
        fy = 101
        for y in range(20):
            fx = 101
            for x in range(10):
                if self.dipfield[y][x+1]==1:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='purple')
                elif self.dipfield[y][x+1]==2:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='deep sky blue')
                elif self.dipfield[y][x+1]==3:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='gold')
                elif self.dipfield[y][x+1]==4:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='orange2')
                elif self.dipfield[y][x+1]==5:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='blue')
                elif self.dipfield[y][x+1]==6:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='yellow green')
                elif self.dipfield[y][x+1]==7:
                    self.canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='red')
                fx+=31
            fy+=31
    
    def checkline(self):
        wcount = 0
        scorecount = 0
        y = 0
        while y < FIELD_HEIGHT:
            for x in range(1,FIELD_WIDTH+1):
                if self.dipfield[y][x]>=1:
                    wcount+=1
            if wcount==10:
                self.deleteline(y)
                scorecount += 1
            else:
                y+=1
                wcount = 0
        self.calcscore(scorecount)

    def deleteline(self, y):
        for x in range(1,FIELD_WIDTH+1):
            self.dipfield[y][x] = 0
        self.castline(y)

    def castline(self, uy):
        for y in range(uy,0,-1):
            for x in range(1,FIELD_WIDTH+1):
                if y==0:
                    self.dipfield[y][x] = 0
                else:
                    self.dipfield[y][x] = self.dipfield[y-1][x]
    
    def calcscore(self, y):
        self.score += y*y*100
                
class Mino:

    #[MINO_NUM][MINO_ALL_ANGLE][MINO_HEIGHT_WIDTH][MINO_HEIGHT_WIDTH]
    minodate = [
        [
            [
                #t mino 0
                [0,0,0,0],
                [0,1,0,0],
                [1,1,1,0],
                [0,0,0,0],    
            ],
            
            [
                #t mino 90
                [0,0,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,1,0,0],    
            ],
            
            [
                #t mino 180
                [0,0,0,0],
                [0,0,0,0],
                [1,1,1,0],
                [0,1,0,0],    
            ],
            
            [
                #t mino 270
                [0,0,0,0],
                [0,1,0,0],
                [1,1,0,0],
                [0,1,0,0],    
            ],
            
        ],

        [
            [
                #I mino 0
                [0,2,0,0],
                [0,2,0,0],
                [0,2,0,0],
                [0,2,0,0],
            ],
            
            [
                #I mino 90 
                [0,0,0,0],
                [0,0,0,0],
                [2,2,2,2],
                [0,0,0,0],
            ],
            
            [
                #I mino 180
                [0,2,0,0],
                [0,2,0,0],
                [0,2,0,0],
                [0,2,0,0],
            ],
            
            [
                #I mino 270
                [0,0,0,0],
                [0,0,0,0],
                [2,2,2,2],
                [0,0,0,0],
            ],
            
        ],

        [
            [
                #O mino 0
                [0,0,0,0],
                [0,3,3,0],
                [0,3,3,0],
                [0,0,0,0],
            ],
            
            [
                #O mino 90 
                [0,0,0,0],
                [0,3,3,0],
                [0,3,3,0],
                [0,0,0,0],
            ],
            
            [
                #O mino 180
                [0,0,0,0],
                [0,3,3,0],
                [0,3,3,0],
                [0,0,0,0],
            ],
            
            [
                #O mino 270
                [0,0,0,0],
                [0,3,3,0],
                [0,3,3,0],
                [0,0,0,0],
            ],
            
        ],
        
        [
            [
                #L mino 0
                [0,0,0,0],
                [0,4,0,0],
                [0,4,0,0],
                [0,4,4,0],
            ],
            
            [
                #L mino 90
                [0,0,0,0],
                [0,0,0,0],
                [4,4,4,0],
                [4,0,0,0],
            ],
            
            [
                #L mino 180 
                [0,0,0,0],
                [4,4,0,0],
                [0,4,0,0],
                [0,4,0,0],
            ],
            
            [
                #L mino 270 
                [0,0,0,0],
                [0,0,4,0],
                [4,4,4,0],
                [0,0,0,0],
            ],
            
        ],
    
        [
            [
                #J mino 0
                [0,0,0,0],
                [0,5,0,0],
                [0,5,0,0],
                [5,5,0,0],
            ],
            
            [
                #J mino 90
                [0,0,0,0],
                [5,0,0,0],
                [5,5,5,0],
                [0,0,0,0],
            ],
            
            [
                #J mino 180 
                [0,0,0,0],
                [0,5,5,0],
                [0,5,0,0],
                [0,5,0,0],
            ],
            
            [
                #J mino 270 
                [0,0,0,0],
                [0,0,0,0],
                [5,5,5,0],
                [0,0,5,0],
            ],
            
        ],
    
        [
            [
                #S mino 0
                [0,0,0,0],
                [0,6,6,0],
                [6,6,0,0],
                [0,0,0,0],
            ],
            
            [
                #S mino 90 
                [0,0,0,0],
                [0,6,0,0],
                [0,6,6,0],
                [0,0,6,0],
            ],
            
            [
                #S mino 180 
                [0,0,0,0],
                [0,6,6,0],
                [6,6,0,0],
                [0,0,0,0],
            ],
            
            [
                #S mino 270
                [0,0,0,0],
                [0,6,0,0],
                [0,6,6,0],
                [0,0,6,0],
            ],
            
        ],
    
        [
            [
                #Z mino 0
                [0,0,0,0],
                [7,7,0,0],
                [0,7,7,0],
                [0,0,0,0],
            ],
            
            [
                #Z mino 90
                [0,0,0,0],
                [0,0,7,0],
                [0,7,7,0],
                [0,7,0,0],
            ],
            
            [
                #Z mino 180
                [0,0,0,0],
                [7,7,0,0],
                [0,7,7,0],
                [0,0,0,0],
            ],
            
            [
                #Z mino 270
                [0,0,0,0],
                [0,0,7,0],
                [0,7,7,0],
                [0,7,0,0],
            ],
            
        ],
    
    ]

    def __init__(self):
        self.mx = 5
        self.my = 0
        self.dmx = 0
        self.dmy = 0
        self.minotype=0
        self.minoangle=0
        self.droptimer = 0
        self.positimer = 0

    def hitcheck(self, field, fmy,fmx,fminotype,fminoangle):
        for y in range(4):
            for x in range(4):
                if fmx+x >=0 and fmx+x <=11:
                    if field[fmy+y][fmx+x] > 0 and self.minodate[fminotype][fminoangle][y][x] > 0:
                        return False
        return True

    def update(self, field):
        self.dmx = self.mx
        self.dmy = self.my
        for y in range(4):
            for x in range(4):
                if self.mx+x <=11:
                    field[self.my+y][self.mx+x] = field[self.my+y][self.mx+x] or self.minodate[self.minotype][self.minoangle][y][x]

    def delete(self, field):
        for y in range(4):
            for x in range(4):
                if self.minodate[self.minotype][self.minoangle][y][x] > 0:
                    field[self.dmy+y][self.dmx+x] = 0

    def drop(self, field):
        flag = False
        self.droptimer += 20
        #self.delete(field)
        if self.droptimer >= 500:
            if self.hitcheck(field, self.my+1, self.mx, self.minotype, self.minoangle):
                self.my += 1
            else:
                self.positimer += 50
                if self.positimer >= 150:
                    flag = True
                    self.positimer = 0
                    self.update(field)
                    self.my = 0
                    self.mx = 5
                    self.minoangle += 1
                    if self.minoangle==4:
                        self.minoangle = 0
                    self.minotype += 1
                    if self.minotype==7:
                        self.minotype = 0
                    self.droptimer = 0
            self.droptimer = 0
        return flag

    def move(self,mlist,field):
        self.delete(field)
        if len(mlist)!=0:
            if mlist[0] == "l":
                if self.hitcheck(field, self.my, self.mx-1, self.minotype, self.minoangle):
                    self.mx -= 1
            elif mlist[0] == "r":
                if self.hitcheck(field, self.my, self.mx+1, self.minotype, self.minoangle):
                    self.mx += 1
            elif mlist[0] == "d":
                if self.hitcheck(field, self.my+1, self.mx, self.minotype, self.minoangle):
                    self.my += 1
            elif mlist[0] == "u":
                self.positimer += 100
                self.droptimer += 500
                while self.hitcheck(field, self.my+1, self.mx, self.minotype, self.minoangle):
                    self.my += 1
            elif mlist[0] == "s":
                buf = self.minoangle
                if self.minoangle == 3:
                    buf = 0
                else:
                    buf += 1
                if self.hitcheck(field, self.my, self.mx, self.minotype, buf):
                    self.minoangle = buf
                elif self.hitcheck(field, self.my, self.mx+1, self.minotype, buf):
                    self.minoangle = buf
                    self.mx +=1
                elif self.hitcheck(field, self.my, self.mx-1, self.minotype, buf):
                    self.minoangle = buf
                    self.mx -=1
            elif mlist[0] == "a":
                buf = self.minoangle
                if self.minoangle == 0:
                    buf = 3
                else:
                    buf -= 1
                if self.hitcheck(field, self.my, self.mx, self.minotype, buf):
                    self.minoangle = buf
                elif self.hitcheck(field, self.my, self.mx+1, self.minotype, buf):
                    self.minoangle = buf
                    self.mx +=1
                elif self.hitcheck(field, self.my, self.mx-1, self.minotype, buf):
                    self.minoangle = buf
                    self.mx -=1

            mlist.pop(0)
