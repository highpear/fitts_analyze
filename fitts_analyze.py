import tkinter as tk
import pyautogui
import sys, time, datetime
import random

# クリックするボタンの色
ACTIVE_CL = "#0000ff"

# 規定値
BTN_PX = 10
BTN_NUM = 5
DATA_NUM = 10

# 1次元配列を2次元配列に変換
def convert_1d_to_2d(l, cols):
    return [l[i:i + cols] for i in range(0, len(l), cols)]

# 2次元配列の座標を1次元配列のインデックスに変換
def index_2d_to_1d(i, j, n):
    return i*n + j

# ランダムなボタンの座標を出力
def select_btn():
    i = random.randint(0, BTN_NUM-1)
    j = random.randint(0, BTN_NUM-1)
    return i, j

# i_btn:クリックされたボタン番号
def button_clicked(i_btn):
    def execute():
        # 実際に実行される処理
        global i_sel
        global j_sel
        global DATA_NUM
        # データ記録
        TIME.append(time.time())
        POSITION.append(pyautogui.position())
        hit = False
        if(i_btn == index_2d_to_1d(i_sel, j_sel, BTN_NUM)):
            hit = True
            # ヒットした時のみカウントを減らす(DATA_NUMはヒットしたデータのみ)
            DATA_NUM-=1
        HIT.append(hit)
        # クリック状態を表示
        # print("clicked at {} hit:{}".format(i_btn, hit))
        refresh_btns() # ボタン更新
    return execute

def refresh_btns():
    global buttons_2d
    global i_sel
    global j_sel
    if(DATA_NUM <= 0):
        finalize() # 終了処理をコール
    else: # 次の画面の描画
        for j in range(BTN_NUM):
            for i in range(BTN_NUM):
                buttons_2d[j][i].config(bg="#ffffff")
        # ボタンを再選択，色を変える
        i_sel, j_sel = select_btn()
        buttons_2d[i_sel][j_sel].config(bg=ACTIVE_CL)

# 終了処理
def finalize():
    # テキストファイルとして書き出す
    root.quit()
    # データ表示
    print("num_of_button: {}x{} button_px: {}".format(BTN_NUM, BTN_NUM, BTN_PX))
    for i, time in enumerate(TIME):
        print("{} {} {}".format(time, POSITION[i], HIT[i]))
    # 書き出し処理
    title = "DATA_{}".format(datetime.datetime.now())
    title = title.replace(":", "") # ファイル名にコロンは使えない
    title = title.split(".")[0]    # ピリオド以下の時間を除去
    with open(title + ".txt", mode="w", encoding="utf-8") as f:
        f.write("num_of_button: {}x{} button_px: {}\n".format(BTN_NUM, BTN_NUM, BTN_PX))
        for i, time in enumerate(TIME):
            f.write("{} {} {}\n".format(time, POSITION[i], HIT[i]))
    f.close()
    sys.exit()

# 条件変更(コマンドライン引数より)
args = sys.argv # -b(ピクセルの大きさpx) -n(一辺の個数) -c(回数)
# print(args) # 引数確認
for i, val in enumerate(args):
    if(val == "-b"):
        BTN_PX = int(args[i+1])
    elif(val == "-n"):
        BTN_NUM = int(args[i+1])
    elif(val == "-c"):
        DATA_NUM = int(args[i+1])
    else:
        continue

# 値が変更されているか確認
# print(BTN_PX, BTN_NUM, DATA_NUM, 10, 5, 3)

# GUI描画
root = tk.Tk()
root.title("フィッツの法則 計測プログラム")

# ボタン生成(1次元配列)
buttons = []
for i in range(BTN_NUM**2):
    buttons.append(tk.Button(height=int(BTN_PX/3), width=BTN_PX, command=button_clicked(i)))

# ボタンを2次元配列に変換
buttons_2d = convert_1d_to_2d(buttons, BTN_NUM)

# ボタンをグリッドに配置
for j in range(BTN_NUM):
    for i in range(BTN_NUM):
        buttons_2d[j][i].grid(column=i, row=j)

# データ記録用配列
TIME = []
POSITION = []
HIT = []

#初期値記録
TIME.append(time.time())
POSITION.append(pyautogui.position())
HIT.append(False) # 初期値はヒットなしとする

# ランダムにボタンを決定
i_sel, j_sel = select_btn()
buttons_2d[i_sel][j_sel].config(bg=ACTIVE_CL)

root.mainloop()