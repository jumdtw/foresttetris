import tetris
import copy
import random

class Omegaplayer:

    def __init__(self):
        # 予測盤面生成のためにomega用のミノとfieldを生成
        self.omegamino = tetris.Mino()
        self.field = []
        # minotypeが変わったか否かで盤面の生成を開始するので、初期値は適当に大きい値を入れる。
        self.omegamino.minotype = [255]
        # このリストに最適解のミノの配置を記録する。
        # x, y, angの情報が入っいる
        self.posminolist = [[1,1,1]]
        # 計算中にスレッドに入られると困るので
        self.calcflag = False

    # ミノの切り替わりを検知
    def cmp_map(self, cmpfield, dx, dy, angle):
        if len(self.field) <= 0:
            return True
        self.omegamino.dmx = dx
        self.omegamino.dmy = dy
        self.omegamino.minoangle = angle
        self.omegamino.delete(cmpfield)
        for x, cf in enumerate(cmpfield):
            if not cf == self.field[x]:
                return True
        return False



    # 設置可能なミノのx, y, angをサーチ.設置可能な場所探してるだけなので配置不可な可能性はある。
    def search_map(self):
        poslist = []
        # アングル4種類
        for ang in range(4):
            y = 0
            while y < tetris.FIELD_HEIGHT:
                for x in range(tetris.FIELD_WIDTH):
                    if self.omegamino.hitcheck(self.field, y, x, self.omegamino.minotype[0], ang):
                        if not self.omegamino.hitcheck(self.field, y+1, x, self.omegamino.minotype[0], ang):
                            poslist.append([x, y, ang])
                y+=1

        rlist = self.placement_map(poslist)

        return rlist
    
    # search_mapして得られた設置可能x,y,angを逆算して配置可能か調べる
    def placement_map(self, poslist):
        rlist = []
        pid = 0
        for p in poslist:
            
            c=0
            flag = True
            mx = p[0]
            my = p[1]
            mang = p[2]
            # 袋小路に入って右左を繰り返さないようにするためのフラッグ
            rflag = False
            lflag = False
            # 上とほぼ同じ理由。右回転左回転を繰り返さないようにするための処理
            rrolflag = False
            lrolflag = False
            # 動きの軌跡。理論的には同じ場所に行かないはずなので
            mvlist = []

            while flag:
                
                c +=1
                angplus = mang + 1
                angminus = mang - 1
                if mang ==3:
                    angplus = 0
                elif mang ==0:
                    angminus = 3

                # 逆算して戻ってこれたので配置可能
                if mx==5 and my==0 and mang==0:
                    flag = False
                    rflag = False
                    lflag = False
                    rrolflag = False
                    lrolflag = False
                    rlist.append(p)
                    #print(1)
                elif self.omegamino.hitcheck(self.field, my-1, mx, self.omegamino.minotype[0], mang) and (not my==0) and self.pos_cmp(mvlist, mx, my-1):
                    my -= 1
                    mvlist.append([mx, my])
                    rflag = False
                    lflag = False
                    rrolflag = False
                    lrolflag = False
                    #print(2, end="")
                    #print("[" + str(pid) + "]" + ", mx : " + str(mx) + ", my : " + str(my) + ", ang : " + str(mang))
                elif self.omegamino.hitcheck(self.field, my, mx+1, self.omegamino.minotype[0], mang) and ((not my==0) or mx<5) and not lflag and self.pos_cmp(mvlist, mx+1, my):
                    mx += 1
                    mvlist.append([mx, my])
                    rflag=True
                    rrolflag = False
                    lrolflag = False
                    #print(3, end="")
                    #print("[" + str(pid) + "]" + ", mx : " + str(mx) + ", my : " + str(my) + ", ang : " + str(mang))
                elif self.omegamino.hitcheck(self.field, my, mx-1, self.omegamino.minotype[0], mang) and ((not my==0) or mx>5) and not rflag and self.pos_cmp(mvlist, mx-1, my):
                    mx -= 1
                    mvlist.append([mx, my])
                    lflag=True
                    rrolflag = False
                    lrolflag = False
                    #print(4, end="")
                    #print("[" + str(pid) + "]" + ", mx : " + str(mx) + ", my : " + str(my) + ", ang : " + str(mang))
                elif self.omegamino.hitcheck(self.field, my, mx, self.omegamino.minotype[0], angplus) and (not my==0 or not mang==0) and not lrolflag and (not self.omegamino.minotype[0]==tetris.MINO_O) and (not self.omegamino.minotype[0]==tetris.MINO_T):
                    mang = angplus
                    rrolflag = True
                    rflag = False
                    lflag = False
                    #print(5, end="")
                    #print("[" + str(pid) + "]" + ", mx : " + str(mx) + ", my : " + str(my) + ", ang : " + str(mang))
                elif self.omegamino.hitcheck(self.field, my, mx, self.omegamino.minotype[0], angminus) and (not my==0 or not mang==0) and not rrolflag and (not self.omegamino.minotype[0]==tetris.MINO_O) and (not self.omegamino.minotype[0]==tetris.MINO_T):
                    mang = angminus
                    lrolflag = True
                    rflag = False
                    lflag = False
                    #print(6, end="")
                    #print("[" + str(pid) + "]" + ", mx : " + str(mx) + ", my : " + str(my) + ", ang : " + str(mang))
                #逆算してるからlrolは右回ししたとき、 rrolは左回ししたとき
                elif len(vec:=self.superrrolcheck(mx, my, angminus, self.omegamino.minotype[0]))<0 and (not my==0 or not mang==0) and not lrolflag:
                    mang = angminus
                    my = vec[0]
                    mx = vec[1]
                    rrolflag = True
                    rflag = False
                    lflag = False
                elif len(vec:=self.superlrolcheck(mx, my, angminus, self.omegamino.minotype[0]))<0 and (not my==0 or not mang==0) and not rrolflag:
                    mang = angminus
                    my = vec[0]
                    mx = vec[1]
                    lrolflag = True
                    rflag = False
                    lflag = False
                else:
                    flag = False
                    rflag = False
                    lflag = False
                    rrolflag = False
                    lrolflag = False
                    #print(7, end="")
                    #print("[" + str(pid) + "]" + "mx : " + str(mx) + ", my : " + str(my) + ", ang : " + str(mang))
                
                if c > 150:
                    self.debug_emap_print(poslist, pid)
                    print("error")
                    exit(1)
            pid += 1

        #print("a;fak;djf : " + str(len(rlist)))
        return rlist
    
    # 移動前の場所がヒットしていないかのチェックをする
    def superrrolcheck(self, mx, my, mang, mtype):
        # 逆算なので左回転してもとに戻す
        angminus = mang-1
        # i minoの動きスーパーローテイションにおけるムーブリスト
        # y, x の順番だから注意
        iposlist=[
            # i mino ang = 0
            [[0, -2], [0, 1], [1, -2], [-2, 1]],
            # i mino ang = 1
            [[0, -1], [0, 2], [-2, -1], [1, 2]],
            # i mino ang = 2
            [[0, 2], [0, -1], [-1, 2], [2, -1]],
            # i mino ang = 3
            [[0, -2], [0, 1], [2, 1], [-1, -2]],
        ]
        # i mino以外のやつ 
        anoposlist = [
            # another mino ang = 0
            [[0, -1], [-1, -1], [2, -1], []],
            # another mino ang = 1
            [[0, 1], [1, 1], [-2, 0], [-2, 1]],
            # another mino ang = 2
            [[0, 1], [2, 0], [2, 1], []],
            # another mino ang = 3
            [[0, -2], [1, -2], [-2, 0], [-2, -1]],
        ]
        if mang ==0:
            angminus = 3
        
        if mtype==1:
            for q in range(4):
                if self.omegamino.hitcheck(self.field, my-iposlist[angminus][q][0], mx-iposlist[angminus][q][1], mtype, angminus):
                    return iposlist[angminus][q]
        else:
            for q in range(4):
                if len(anoposlist[angminus][q]) <=0:
                    continue
                if self.omegamino.hitcheck(self.field, my-anoposlist[angminus][q][1], mx-anoposlist[angminus][q][0], mtype, angminus):
                    return anoposlist[angminus][q]

        return []
    
    # 移動前の場所がヒットしていないかのチェックをする
    def superlrolcheck(self, mx, my, mang, mtype):
        # 逆算なので左回転してもとに戻す
        angplus = mang+1
        # i minoの動きスーパーローテイションにおけるムーブリスト
        # y, x の順番だから注意
        iposlist=[
            # i mino ang = 0
            [[0, -1], [0, 2], [-2, -1], [1, 2]],
            # i mino ang = 1
            [[0, 2], [0, -1], [-1, 2], [2, -1]],
            # i mino ang = 2
            [[0, 1], [0, -2], [2, 1], [-1, -2]],
            # i mino ang = 3
            [[0, 1], [0, -2], [1, -2], [-2, 1]],
        ]
        # i mino以外のやつ 
        anoposlist = [
            # another mino ang = 0
            [[0, 1], [-1, 1], [2, 1], []],
            # another mino ang = 1
            [[0, 1], [1, 1], [-2, 0], [-2, 1]],
            # another mino ang = 2
            [[0, -1], [2, 0], [2, -1], []],
            # another mino ang = 3
            [[0, -1], [1, -1], [-2, 0], [-2, -1]],
        ]
        if mang==3:
            angplus = 0
        
        if mtype==1:
            for q in range(4):
                if self.omegamino.hitcheck(self.field, my-iposlist[angplus][q][0], mx-iposlist[angplus][q][1], mtype, angplus):
                    return iposlist[angplus][q]
        else:
            for q in range(4):
                if len(anoposlist[angplus][q]) <=0:
                    continue
                if self.omegamino.hitcheck(self.field, my-anoposlist[angplus][q][1], mx-anoposlist[angplus][q][0], mtype, angplus):
                    return anoposlist[angplus][q]

        return []


    def pos_cmp(self, mvlist, mx, my):
        for p in mvlist:
            if mx==p[0] and my==p[1]:
                return False
        return True

    
    def debug_emap_print(self, maplist, index):
        x = maplist[index][0]
        y = maplist[index][1]
        ang = maplist[index][2]
        buffield = copy.deepcopy(self.field)
        for fy in range(4):
            for fx in range(4):
                if x+fx >= 0 and x+fx <= 11 and y+fy <= 20:
                    buffield[y+fy][x+fx] = buffield[y+fy][x+fx] or self.omegamino.minodate[self.omegamino.minotype[0]][ang][fy][fx]  
        for q in buffield:
            print(q)

    
    def evaulate_map(self):
        self.calcflag = True
        maplist = self.search_map()
        #self.debug_emap_print(maplist, 0)
        self.posminolist.pop(0)
        self.posminolist.append(maplist[random.randint(0,len(maplist)-1)])
        self.calcflag = False

    # 
    def return_ctllist(self, curx, cury, curang):
        self.calcflag = True
        key = tetris.KEY_LEFT
        fmino = self.posminolist[0]
        if not curang == fmino[2]:
            # 3 0 -> TURNRIGHT
            # 0 3 -> TURNLEFT
            if curang==3 and fmino[2]==0:
                key = tetris.KEY_TURNRIGHT
            elif curang==0 and fmino[2]==3:
                key = tetris.KEY_TURNLEFT
            elif curang < fmino[2]:
                key = tetris.KEY_TURNRIGHT
            else:
                key = tetris.KEY_TURNLEFT
        elif not curx == fmino[0]:
            if curx < fmino[0]:
                key = tetris.KEY_RIGHT
            else:
                key = tetris.KEY_LEFT
        
        elif not cury == fmino[1]:
            key = tetris.KEY_UP

        self.calcflag = False
        return key

