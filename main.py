import tkinter

# 1マス 30x30
root = tkinter.Tk()
root.title(u"test")
root.geometry("800x800")
canvas = tkinter.Canvas(root, width=800, height=800)
dipfield = []
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



class Field:

    def __init__(self, xo):
        self.xoffset = xo
    
    def refresh(self):
                    
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 800, 800, fill='black')
        fx = self.xoffset
        fy = 100
        ex = 411
        ey = 100
        for y in range(21):
            canvas.create_line(fx, fy, ex, ey, fill='white')
            fy+=31
            ey+=31

        fx = self.xoffset
        fy = 100
        ex = self.xoffset
        ey = 721
        for x in range(11):
            canvas.create_line(fx, fy, ex, ey, fill='white')
            fx+=31
            ex+=31

                
        canvas.place(x=0,y=0)

    
    def draw(self):
        fy = 101
        for y in range(20):
            fx = 101
            for x in range(10):
                if dipfield[y][x+1]==1:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='purple')
                elif dipfield[y][x+1]==2:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='deep sky blue')
                elif dipfield[y][x+1]==3:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='gold')
                elif dipfield[y][x+1]==4:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='orange2')
                elif dipfield[y][x+1]==5:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='blue')
                elif dipfield[y][x+1]==6:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='yellow green')
                elif dipfield[y][x+1]==7:
                    canvas.create_rectangle(fx, fy, fx+29, fy+29, fill='red')
                fx+=31
            fy+=31


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

    def hitcheck(self,fmy,fmx,fminotype,fminoangle):
        for y in range(4):
            for x in range(4):
                if fmx+x <=11:
                    if dipfield[fmy+y][fmx+x] and self.minodate[fminotype][fminoangle][y][x]:
                        return False
        return True

    def draw(self):
        self.dmx = self.mx
        self.dmy = self.my
        for y in range(4):
            for x in range(4):
                if self.mx+x <=11:
                    dipfield[self.my+y][self.mx+x] = dipfield[self.my+y][self.mx+x] or self.minodate[self.minotype][self.minoangle][y][x]

    def fieldupdate(self):
        for y in range(4):
            for x in range(4):
                if self.mx+x <=11:
                    dipfield[self.my+y][self.mx+x] = dipfield[self.my+y][self.mx+x] or self.minodate[self.minotype][self.minoangle][y][x]

    def delete(self):
        for y in range(4):
            for x in range(4):
                if self.minodate[self.minotype][self.minoangle][y][x] > 0:
                    dipfield[self.dmy+y][self.dmx+x] = 0

    def drop(self):
        self.droptimer += 50
        if self.droptimer >= 800:
            if self.hitcheck(self.my+1, self.mx, self.minotype, self.minoangle):
                self.my += 1
            else:
                self.positimer += 50
                if self.positimer >= 150:
                    self.positimer = 0
                    self.fieldupdate()
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
            
    def move(self,mlist):
        while len(mlist)!=0:
            if mlist[0] == "l":
                if self.hitcheck(self.my, self.mx-1, self.minotype, self.minoangle):
                    self.mx -= 1
            elif mlist[0] == "r":
                if self.hitcheck(self.my, self.mx+1, self.minotype, self.minoangle):
                    self.mx += 1
            elif mlist[0] == "d":
                if self.hitcheck(self.my+1, self.mx, self.minotype, self.minoangle):
                    self.my += 1
            elif mlist[0] == "u":
                self.positimer += 100
                while self.hitcheck(self.my+1, self.mx, self.minotype, self.minoangle):
                    self.my += 1
            elif mlist[0] == "s":
                buf = self.minoangle
                if self.minoangle == 3:
                    buf = 0
                else:
                    buf += 1
                if self.hitcheck(self.my, self.mx, self.minotype, buf):
                    self.minoangle = buf
            elif mlist[0] == "a":
                buf = self.minoangle
                if self.minoangle == 0:
                    buf = 3
                else:
                    buf -= 1
                if self.hitcheck(self.my, self.mx, self.minotype, buf):
                    self.minoangle = buf

            mlist.pop(0)


def gameloop():
    field.refresh()
    mino.drop()
    mino.draw()
    field.draw()
    mino.delete()
    root.after(20, gameloop)

def dipfieldInit():
    for y in range(21):
        buf=[]
        for x in range(12):
            if y==20:
                buf.append(1)                
            elif x==0 or x==11:
                buf.append(1)
            else:
                buf.append(0)
        dipfield.append(buf)

def keyevent(event):
    # 入力されたキーを取得
    key = event.keysym

    # 入力されたキーに応じてラベルを変更
    if key == "Left":
        mino.move(['l'])
    elif key == "Right":
        mino.move(['r'])
    elif key == "Down":
        mino.move(['d'])
    elif key == "Up":
        mino.move(['u'])
    elif key == "s":
        mino.move(['s'])
    elif key == "a":
        mino.move(['a'])


field = Field(xo=100)
mino = Mino()
root.bind("<Key>", keyevent)

def main():
    dipfieldInit()
    gameloop()
    root.mainloop()

if __name__=="__main__":
    main()