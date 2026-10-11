import pygame as pg
import math
import os
import random


# 初始化
pg.mixer.init()
# 设置屏幕大小
screen = pg.display.set_mode((800, 600))
# 设置标题栏标题
pg.display.set_caption("洁尔佩塔")
# 设置标题旁图标
pg.display.set_icon(pg.image.load("海边.png"))
# 设置洁尔佩塔初始方向
direction = "left"
# 设置及缩放背景及透明度
backcolor = pg.transform.scale(pg.image.load("背景.jpg"), (800, 600))
backcolor.set_alpha(190)
# 设置装饰图
decoration = pg.transform.scale(pg.image.load("直到大地变成一颗酸橙.png"), (600, 200))
decoration.set_alpha(220)
# 创建对象以便之后设置帧率
clo = pg.time.Clock()
# 一些初始值
running = True
x = 600
y = 300
dx = 0
dy = 0
speed = 0
img = "送货ｓ/frame_0001.png"
sca = False
music = True
gilberta_right = None
gilberta_up = None
gilberta_right_up = None
gilberta_down = None
gilberta_right_down = None
gilberta = None
kind = None
last_update = pg.time.get_ticks()
# 设置music结束事件
MUSIC_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(MUSIC_END)
# 初始播放music
music_list = [
    "高梨康治 - Pendulum.mp3",
    "北出菜奈 - 月華 -tsukihana-.mp3",
    "洛天依 - 一秒的梦.mp3"
]
count = 0


def music_hear():
    if music:
        pg.mixer.music.load(music_list[count])
        pg.mixer.music.play()


music_hear()


# 语音导入及封装
voice = "予愿安洁莉娜语音"
voice_num = 0
voices = []
for i in os.listdir(voice):
    if i.lower().endswith(".wav"):
        voices.append(pg.mixer.Sound(os.path.join(voice, i)))


def voice_hear():
    global voice_num
    pg.mixer.stop()
    voice_num = random.randint(0, len(voices) - 1)
    voices[voice_num].play()


# gif转出的系列png导入及封装
def load_frames(folder):
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".png")])
    frames = []
    for f in files:
        image = pg.image.load(os.path.join(folder, f)).convert_alpha()
        frames.append(image)
    return frames


qi = load_frames("骑行ｓ")
song = load_frames("送货ｓ")
zhi = load_frames("纸飞机ｓ")
x_index = 0
y_index = 0


# 小人左进右出，上进下出d
def limit():
    global x
    global y
    if x < -150:
        x = 800
    if x > 800:
        x = -150
    if y < -150:
        y = 600
        y = 600
    if y > 600:
        y = -150


# 加速时缩小，数字可修改，>1则放大
def ctrl_sca():
    global img
    img_sca = pg.transform.scale_by(img, 0.7)
    if sca:
        img = img_sca


# 洁尔佩塔图像设置，以便L键切换
def gilberta_img():
    global img
    global gilberta_right
    global gilberta_up
    global gilberta_right_up
    global gilberta_down
    global gilberta_right_down
    global gilberta
    global kind
    if y_index == 0:
        kind = song
        img = pg.transform.scale(song[x_index], (150, 150))
    elif y_index == 1:
        kind = zhi
        img = pg.transform.scale(zhi[x_index], (150, 150))
    else:
        kind = qi
        img = pg.transform.scale(qi[x_index], (150, 150))
    gilberta = img
    gilberta_right = pg.transform.flip(img, True, False)
    gilberta_up = pg.transform.rotate(img, -30)
    gilberta_right_up = pg.transform.rotate(gilberta_right, 30)
    gilberta_down = pg.transform.rotate(img, 30)
    gilberta_right_down = pg.transform.rotate(gilberta_right, -30)


# 洁尔佩塔
def draw():
    global direction
    global img
    global sca
    if dx == 0:
        if direction == "left":
            gilberta_img()
            ctrl_sca()
            screen.blit(img, (x, y))
        elif direction == "right":
            img = gilberta_right
            ctrl_sca()
            screen.blit(img, (x, y))
    elif dy == 0:
        if dx < 0:
            img = gilberta
            ctrl_sca()
            screen.blit(img, (x, y))
            direction = "left"
        elif dx > 0:
            img = gilberta_right
            ctrl_sca()
            screen.blit(img, (x, y))
            direction = "right"
    elif dy > 0:
        if dx > 0:
            img = gilberta_right_down
            ctrl_sca()
            screen.blit(img, (x, y))
            direction = "right"
        elif dx < 0:
            img = gilberta_down
            ctrl_sca()
            screen.blit(img, (x, y))
            direction = "left"
    elif dy < 0:
        if dx > 0:
            img = gilberta_right_up
            ctrl_sca()
            screen.blit(img, (x, y))
            direction = "right"
        elif dx < 0:
            img = gilberta_up
            ctrl_sca()
            screen.blit(img, (x, y))
            direction = "left"


def move():
    global x
    global y
    global dx
    global dy
    global running
    global speed
    global direction
    global img
    global sca
    # 键盘事件(英文输入法)
    keys = pg.key.get_pressed()
    # Q键关闭游戏
    if keys[pg.K_q]:
        running = False
    # 键盘操控移动及斜走不变成根号二 倍速
    dx = 0
    dy = 0
    if keys[pg.K_w]:
        dy -= 1
    if keys[pg.K_s]:
        dy += 1
    if keys[pg.K_a]:
        dx -= 1
    if keys[pg.K_d]:
        dx += 1
    if dx != 0 or dy != 0:
        length = math.hypot(dx, dy)
        dx /= length
        dy /= length
    x += dx * speed
    y += dy * speed
    # ctrl加速
    if keys[pg.K_RCTRL] or keys[pg.K_LCTRL]:
        speed = 3.5
        sca = True
    else:
        speed = 1
        sca = False


while running:
    now = pg.time.get_ticks()
    for ev in pg.event.get():
        # 当点击右上角的叉号(QUIT事件)关闭pg
        if ev.type == pg.QUIT:
            running = False
            break
        # music一曲结束
        elif ev.type == MUSIC_END:
            if music:
                count = (count + 1) % len(music_list)
                music_hear()

        elif ev.type == pg.MOUSEBUTTONDOWN:
            # 左键单击让洁尔佩塔出现在指定位置
            if ev.button == pg.BUTTON_LEFT:
                xx, yy = pg.mouse.get_pos()
                x = xx - 30
                y = yy - 30
            # 右键播放语音
            elif ev.button == pg.BUTTON_RIGHT:
                voice_hear()
        # 鼠标滚轮调节music音量,初始即为最大音量
        elif ev.type == pg.MOUSEWHEEL:
            if ev.y == 1:
                volume = pg.mixer.music.get_volume()
                pg.mixer.music.set_volume(volume + 0.05)
            if ev.y == -1:
                volume = pg.mixer.music.get_volume()
                pg.mixer.music.set_volume(volume - 0.05)
        elif ev.type == pg.KEYDOWN:
            # 空格暂停music播放
            if ev.key == pg.K_SPACE:
                if music:
                    if pg.mixer.music.get_busy():
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
            # e键取消播放,暂停中亦可
            elif ev.key == pg.K_e:
                music = False
                if pg.mixer.music.get_busy():
                    pg.mixer.music.stop()
            # t键启动播放，与e相对
            elif ev.key == pg.K_t:
                music = True
                if not pg.mixer.music.get_busy():
                    music_hear()
            # r键重播，只有音乐在播时可
            elif ev.key == pg.K_r:
                pg.mixer.music.rewind()
            # z键上一首，只有音乐在播时可
            elif ev.key == pg.K_z:
                if pg.mixer.music.get_busy():
                    count = (count - 1) % len(music_list)
                    music_hear()
            # x键下一首
            elif ev.key == pg.K_x:
                if pg.mixer.music.get_busy():
                    count = (count + 1) % len(music_list)
                    music_hear()
            # l键切换人物
            elif ev.key == pg.K_l:
                y_index = (y_index + 1) % 3
                gilberta_img()
    # 要想冇残影得有底色
    screen.fill(0x66ccff)
    # 背景
    screen.blit(backcolor, (0, 0))
    # 酸橙
    screen.blit(decoration, decoration.get_rect(center=(400, 130)))
    # 洁尔佩塔
    draw()
    if now - last_update > 100:
        x_index = (x_index + 1) % len(kind)
        last_update = now
    gilberta_img()
    move()
    limit()
    # 更新屏幕
    pg.display.update()
    # 设置帧率
    clo.tick(200)

pg.quit()
