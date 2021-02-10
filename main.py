import tkinter
import tetris
import copy
import omega
import time
import threading





def player_evaluate_map():
    omegaplayer.evaulate_map()


def player_return_ctllist():
    if omegaplayer.calcflag:
        return
    q = omegaplayer.return_ctllist(field.mino.mx, field.mino.my, field.mino.minoangle)
    ctlmlist.append(q) 

def update(field, mlist):
    field.ctlmlist = mlist 
    field.mino.move(field.ctlmlist, field.dipfield)
    if field.mino.drop(field.dipfield):
        return True
    field.checkline()
    scoretxt.set("Score : " + str(field.score))
    field.mino.update(field.dipfield)
    return False

def gameloop():
    field.refresh()
    #all field create
    if update(field, ctlmlist):
        root.after(100, gamereset)
        return
    field.draw()
    if omegaplayer.cmp_map(field.dipfield, field.mino.dmx, field.mino.dmy, field.mino.minoangle):
        # deepcopyじゃないとインスタンスがもってる変数は共有のものを使用してしまう
        omegaplayer.omegamino = copy.deepcopy(field.mino)
        omegaplayer.field = copy.deepcopy(field.dipfield)
        omegaplayer.omegamino.delete(omegaplayer.field)
        player = threading.Thread(target=player_evaluate_map)
        player.start()
    else:
        player = threading.Thread(target=player_return_ctllist)
        player.start()
    root.after(15, gameloop)
    
def gamereset():
    canvas = tkinter.Canvas(root, width=800, height=800)
    global field
    global omegaplayer
    field = tetris.Field(fmino=tetris.Mino(), tetcanvas=canvas)
    omegaplayer = omega.Omegaplayer()
    root.after(100, gameloop)

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
    elif key == "t":
        time.sleep(5)



    
if __name__=="__main__":
    root = tkinter.Tk()
    root.title(u"test")
    root.geometry("800x800")
    ctlmlist = []
    root.bind("<Key>", keyevent)
    canvas = tkinter.Canvas(root, width=800, height=800)
    field = tetris.Field(fmino=tetris.Mino(), tetcanvas=canvas)
    scoretxt = tkinter.StringVar()
    scoretxt.set("Score : " + str(field.score))
    Lscore = tkinter.Label(root, textvariable=scoretxt)
    Lscore.place(x=5, y=5)
    omegaplayer = omega.Omegaplayer()
    gameloop()
    root.mainloop()
