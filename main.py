import tkinter
import tetris

root = tkinter.Tk()
root.title(u"test")
root.geometry("800x800")
ctlmlist = []
canvas = tkinter.Canvas(root, width=800, height=800)
field = tetris.Field(xo=100, fmino=tetris.Mino(), tetcanvas=canvas)
scoretxt = tkinter.StringVar()
scoretxt.set("Score : " + str(field.score))
Lscore = tkinter.Label(root, textvariable=scoretxt)
Lscore.place(x=5, y=5)

def gameloop():
    field.refresh()
    field.update(ctlmlist, scoretxt)
    field.draw()
    root.after(20, gameloop)

def keyevent(event):
    # 入力されたキーを取得
    key = event.keysym

    # 入力されたキーに応じてラベルを変更
    if key == "Left":
        ctlmlist.append('l')
    elif key == "Right":
        ctlmlist.append('r')
    elif key == "Down":
        ctlmlist.append('d')
    elif key == "Up":
        ctlmlist.append('u')
    elif key == "s":
        ctlmlist.append('s')
    elif key == "a":
        ctlmlist.append('a')

root.bind("<Key>", keyevent)

def main():

    gameloop()
    root.mainloop()

if __name__=="__main__":
    main()