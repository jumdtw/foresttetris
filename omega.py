import tetris
import copy
import random
import os
import json

'''
学習順序

１，手とる

２，盤面を毎回評価する。その際の 特徴量は各ゲーム単位ですべて保存する。

３，ゲームが終了したら（ゲームオーバーか５０ライン消し終わったら）、その保存した特徴量群とスコアを紐づけて保存する

４，１０００ゲーム分くらいたまったら、スコアを比較して上位100位を学習させる（もしくは特徴量数で決める）

５，やったね。
'''

class Omegamap:
    # 目的座標までの軌跡
    # xspinが紛らわしい
    '''
    aa =  {
            "X":1,
            "Y":1,
            "ANG":1,
            スピンか横移動が必要な場合のmove. 直接 tetris.KEY_hogeをぶち込む
            "MOVE":[],
            基本これいらいないかも
            "NEXT":{
                "X":2,
                "Y":2,
                "ANG":2,
                "SPIN"
                "NEXT":{
                
                }
            }
        }
    '''
    def __init__(self, x, y, ang, move):
        self.map = {}
        self.map['desx'] = x
        self.map['desy'] = y
        self.map['desang'] = ang
        # 再度単純操作でゴールへと導くために、ここで軽く操作する
        self.map['desmove'] = move
        self.map['next'] = 0

    def add_next(self, x, y, ang, move):
        self.map['next'] = Omegamap(x, y, ang, move)

        
        
    
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
                            poslist.append(Omegamap(x, y, ang, []))
                y+=1

        rlist = self.placement_map(poslist)

        return rlist

    # Trueなら上からそのまま刺せる、Falseなら横移動が必要かそもそも設置が無理
    def drop_judge(self, field, minotype, minoang, mx, my):
        widthlist = [
            # x = 0
            99,
            # x = 1
            99,
            # x = 2
            99,
            # x = 3
            99
        ]
        for y in range(4):
            for x in range(4):
                if self.omegamino.minodate[minotype][minoang][y][x] >= 1:
                    # 横幅とそのピクセルの位置を把握
                    if widthlist[x] >= y:
                        widthlist[x] = y

        for i,q in enumerate(widthlist):
            if mx+i >= tetris.FIELD_WIDTH+1:
                continue
            if q>=99:
                continue
            bufy = my + q - 1 
            while bufy >=0:
                if not field[bufy][mx+i] == 0:
                    return False
                bufy-=1
        return True
        

    # spin 必要な場合はtrue, いらない場合はfalse
    def xspin_judge(self, field, minotype, minoang, mx, my):
        xspinX=0
        xspinY=1
        c=0
        # xspin[minotype][minoang][mx or my][index]
        xspin = [
            # tspin
            [
                # ang = 0
                [
                    [0,0,2,2],
                    [0,2,0,2]
                ],
                # ang = 1
                [
                    [0,0,2,2],
                    [0,2,0,2]
                ],
                # ang = 2
                [
                    [0,0,2,2],
                    [0,2,0,2]
                ],
                # ang = 3
                [
                    [0,0,2,2],
                    [0,2,0,2]
                ],               
            ],
            # ispin 存在しない
            [],
            # ospin 存在しない
            [],
            # Lspin 
            [
                [
                    # 必要個数が3つなので同じものをかぶせて4回に統一している
                    [0,0,0,2],
                    [0,0,2,2]
                ],
                [
                    [0,2,0,0],
                    [0,0,2,2]
                ],
                [
                    [0,2,2,2],
                    [0,0,2,2]
                ],
                [
                    [2,2,0,2],
                    [0,0,2,2]
                ],
            ],
            # Jspin 
            [
                [
                    # 必要個数が3つなので同じものをかぶせて4回に統一している
                    [2,2,0,2],
                    [0,0,2,2]
                ],
                [
                    [0,0,0,2],
                    [0,0,2,2]
                ],
                [
                    [0,2,0,0],
                    [0,0,2,2]
                ],
                [
                    [0,2,2,2],
                    [0,0,2,2]
                ],
            ],
            # Sspin 
            [
                [
                    # 必要個数が2つなので同じものをかぶせて4回に統一している
                    [0,0,2,2],
                    [0,0,1,1]
                ],
                [
                    [2,2,1,1],
                    [0,0,2,2]
                ],
                [
                    [0,0,2,2],
                    [1,1,2,2]
                ],
                [
                    [1,1,0,0],
                    [0,0,2,2]
                ],
            ],
            # Zspin 
            [
                [
                    # 必要個数が2つなので同じものをかぶせて4回に統一している
                    [2,2,0,0],
                    [0,0,1,1]
                ],
                [
                    [1,1,2,2],
                    [0,0,2,2]
                ],
                [
                    [2,2,0,0],
                    [1,1,2,2]
                ],
                [
                    [0,0,1,1],
                    [0,0,2,2]
                ],
            ],
        ]
        # T,I,O,L,J,S,Z
        judge_count = [3,99,99,3,3,2,2]
        
        for q in range(4):
            if minotype==tetris.MINO_O or minotype==tetris.MINO_I:
                continue
            bufx = mx + xspin[minotype][minoang][xspinX][q]
            bufy = my + xspin[minotype][minoang][xspinY][q]
            if (bufx >=tetris.FIELD_WIDTH+1 or bufx <= 0) or (bufy >= tetris.FIELD_HEIGHT or bufy <= 0):
                continue
            if field[bufy][bufx] >= 1:
                c+=1
                if c >= judge_count[minotype]:
                    return True
        return False
    
    # search_mapして得られた設置可能x,y,angを逆算して配置可能か調べる
    def placement_map(self, poslist):
        rlist = []
        pid = 0
        # [x, y, ang]
        for p in poslist:
            # 上から刺せるかをまず確認する。
            if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"], p.map['desy']):
                rlist.append(p)
                continue
            # 横移動させて上からさせないかを確認
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]+1, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]+1, p.map['desy']):
                    p.map["desx"] = p.map["desx"] + 1
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]+2, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]+2, p.map['desy']):
                    p.map["desx"] = p.map["desx"] + 2
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]+1, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]+1, p.map['desy']):
                    p.map["desx"] = p.map["desx"] + 3
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]+2, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]+2, p.map['desy']):
                    p.map["desx"] = p.map["desx"] + 4
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    p.map['desmove'].append(tetris.KEY_LEFT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]-1, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]-1, p.map['desy']):
                    p.map["desx"] = p.map["desx"] - 1
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]-2, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]-2, p.map['desy']):
                    p.map["desx"] = p.map["desx"] - 2
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]-1, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]-1, p.map['desy']):
                    p.map["desx"] = p.map["desx"] - 3
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    rlist.append(p)
                    continue
            elif self.omegamino.hitcheck(self.field, p.map['desy'], p.map["desx"]-2, self.omegamino.minotype[0], p.map["desang"]):
                if self.drop_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"]-2, p.map['desy']):
                    p.map["desx"] = p.map["desx"] - 4
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    p.map['desmove'].append(tetris.KEY_RIGHT)
                    rlist.append(p)
                    continue 
            else:
                continue

            # spin が必要ない場合で基本的には上から落とせる
            # ホールの場合この判定だとバグるがそもそもホールはいい盤面とは言えないのでこれでおけ
            #if not self.xspin_judge(self.field, self.omegamino.minotype[0], p.map["desang"], p.map["desx"], p.map['desy']):
            #    rlist.append(p)
            #    continue
            
        return rlist
    
    def pos_cmp(self, mvlist, mx, my):
        for p in mvlist:
            if mx==p[0] and my==p[1]:
                return False
        return True

    
    def debug_emap_print(self, maplist, index):
        os.system('cls')
        x = maplist[index].map['desx']
        y = maplist[index].map['desy']
        ang = maplist[index].map['desang']
        buffield = copy.deepcopy(self.field)
        for fy in range(4):
            for fx in range(4):
                if x+fx >= 0 and x+fx <= 11 and y+fy <= 20:
                    buffield[y+fy][x+fx] = buffield[y+fy][x+fx] or self.omegamino.minodate[self.omegamino.minotype[0]][ang][fy][fx]  
        for q in buffield:
            for p in q:
                if p==0:
                    print(f"{Color.WHITE}"+str(p)+' ', end='')
                elif p==1:
                    print(f"{Color.PURPLE}"+str(p)+' ', end='')
                elif p==2:
                    print(f"{Color.SKYBLUE}"+str(p)+' ', end='')
                elif p==3:
                    print(f"{Color.YELLOW}"+str(p)+' ', end='')
                elif p==4:
                    print(f"{Color.ORANGE}"+str(p)+' ', end='')
                elif p==5:
                    print(f"{Color.BLUE}"+str(p)+' ', end='')
                elif p==6:
                    print(f"{Color.YELLOWGREEN}"+str(p)+' ', end='')
                elif p==7:
                    print(f"{Color.RED}"+str(p)+' ', end='')
            print(f"{Color.RESET}")


    
    def evaulate_map(self):
        self.calcflag = True
        maplist = self.search_map()
        mr = random.randint(0,len(maplist)-1)
        # コンソールにデバッグ画面の表示
        self.debug_emap_print(maplist, mr)
        # 新しい評価盤面を追加するため先頭を削除
        self.posminolist.pop(0)
        self.posminolist.append(maplist[mr])
        self.calcflag = False


    # 手順としては、１，ミノのangを合わせるー＞２，ミノのxをそろえるー＞３，ミノのyをそろえる
    # tspin等は、回転するその一歩手前に目標座標を設置し、回転させる
    def return_ctllist(self, curx, cury, curang):
        self.calcflag = True
        key = tetris.KEY_UP
        # 目的座標
        # 0:x, 1:y, 2:ang
        fmino = self.posminolist[0]
        # 回転
        if curang==fmino.map['desang'] and curx==fmino.map['desx'] and cury==fmino.map['desy'] and not len(fmino.map['desmove'])==0:
            print("d;alfjksd;lkfajsd")
            key = fmino.map['desmove'].pop(0)
            if key=tetris.KEY_LEFT:
                self.posminolist[0].map['desx'] = self.posminolist[0].map['desx'] - 1
            elif key ==tetris.KEY_RIGHT:
                self.posminolist[0].map['desx'] = self.posminolist[0].map['desx'] + 1
        elif not curang==fmino.map['desang']:
            key = tetris.KEY_TURNRIGHT
        elif curx < fmino.map['desx']:
            print(f"RIGHT : {curx} : {fmino.map['desx']}")
            key = tetris.KEY_RIGHT
        elif curx > fmino.map['desx']:
            print(f"LEFT : {curx} : {fmino.map['desx']}")
            key = tetris.KEY_LEFT
        elif not cury==fmino.map['desy']:
            key = tetris.KEY_DOWN

        self.calcflag = False
        return key

class Color:
    BLACK          = '\033[30m'#(文字)黒
    RED            = '\033[31m'#(文字)赤
    GREEN          = '\033[32m'#(文字)緑
    YELLOW         = '\033[33m'#(文字)黄
    YELLOWGREEN    = '\033[38;2;171;207;0m'
    BLUE           = '\033[34m'#(文字)青
    SKYBLUE        = '\033[38;2;102;204;255m'#(文字)skyblue
    MAGENTA        = '\033[35m'#(文字)マゼンタ
    CYAN           = '\033[36m'#(文字)シアン
    WHITE          = '\033[37m'#(文字)白
    PURPLE         = '\033[38;2;255;0;255m' #(文字)紫
    ORANGE         = '\033[38;2;255;165;0m' #(文字)オレンジ
    COLOR_DEFAULT  = '\033[39m'#文字色をデフォルトに戻す
    BOLD           = '\033[1m'#太字
    UNDERLINE      = '\033[4m'#下線
    INVISIBLE      = '\033[08m'#不可視
    REVERCE        = '\033[07m'#文字色と背景色を反転
    BG_BLACK       = '\033[40m'#(背景)黒
    BG_RED         = '\033[41m'#(背景)赤
    BG_GREEN       = '\033[42m'#(背景)緑
    BG_YELLOW      = '\033[43m'#(背景)黄
    BG_BLUE        = '\033[44m'#(背景)青
    BG_MAGENTA     = '\033[45m'#(背景)マゼンタ
    BG_CYAN        = '\033[46m'#(背景)シアン
    BG_WHITE       = '\033[47m'#(背景)白
    BG_DEFAULT     = '\033[49m'#背景色をデフォルトに戻す
    RESET          = '\033[0m'#全てリセット