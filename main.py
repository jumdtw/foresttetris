import tkinter
import tetris



def main():
    root = tkinter.Tk()
    root.title(u"test")
    root.geometry("800x800")
    canvas = tkinter.Canvas(root, width=800, height=800)
    field = tetris.Field(xo=100,  fmino=tetris.Mino())
    tetris.gameloop(field)
    root.mainloop()

if __name__=="__main__":
    main()