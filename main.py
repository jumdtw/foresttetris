import tkinter
import tetris
import copy



root = tkinter.Tk()
root.title(u"test")
root.geometry("800x800")
ctlmlist = []
canvas = tkinter.Canvas(root, width=800, height=800)
field = tetris.Field(fmino=tetris.Mino(), tetcanvas=canvas)
scoretxt = tkinter.StringVar()
scoretxt.set("Score : " + str(field.score))
Lscore = tkinter.Label(root, textvariable=scoretxt)
Lscore.place(x=5, y=5)

class FieldData():

    def __init__(self):
        self.fx = 0
        self.fy = 0
        self.ftype = 0
        self.sangle = 0
        self.fangle = 0
        self.frolflag = False
        self.ffield = []


def omega():
    array = [tetris.KEY_LEFT, tetris.KEY_RIGHT, tetris.KEY_LEFT, tetris.KEY_RIGHT, tetris.KEY_LEFT, tetris.KEY_DOWN]
    for x in array:
        ctlmlist.append(x)


def update(field, mlist):
    field.ctlmlist = mlist 
    field.mino.move(field.ctlmlist, field.dipfield)
    if field.mino.drop(field.dipfield):
        field.checkline()
        scoretxt.set("Score : " + str(field.score))
    field.mino.update(field.dipfield)

def gameloop():
    field.refresh()
    #all field create
    update(field, ctlmlist)
    field.draw()
    if len(ctlmlist) <= 0:
        root.after(20, omega)
    root.after(20, gameloop)
    

def keyevent(event):
    # 入力されたキーを取得
    key = event.keysym

    # 入力されたキーに応じてラベルを変更
    if key == "Left":
        ctlmlist.append(tetris.KEY_LEFT)
    elif key == "Right":
        ctlmlist.append(tetris.KEY_RIGHT)
    elif key == "Down":
        ctlmlist.append(tetris.KEY_DOWN)
    elif key == "Up":
        ctlmlist.append(tetris.KEY_UP)
    elif key == "s":
        ctlmlist.append(tetris.KEY_TURNRIGHT)
    elif key == "a":
        ctlmlist.append(tetris.KEY_TURNLEFT)

root.bind("<Key>", keyevent)

def main():
    gameloop()
    root.mainloop()

if __name__=="__main__":
    main()