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
# 设置洁尔佩塔及其初始方向
gilberta = pg.image.load("送货.png")
gilberta_right = pg.transform.flip(gilberta, True, False)
direction = "left"
# 设置洁尔佩塔斜向移动图(4个)
gilberta_up = pg.transform.rotate(gilberta, -30)
gilberta_right_up = pg.transform.rotate(gilberta_right, 30)
gilberta_down = pg.transform.rotate(gilberta, 30)
gilberta_right_down = pg.transform.rotate(gilberta_right, -30)
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
speed = 0
img = gilberta
sca = False
music = True
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


# 小人左进右出，上进下出
def limit():
    global x
    global y
    if x < 0:
        x = 800
    if x > 800:
        x = 0
    if y < 0:
        y = 600
    if y > 600:
        y = 0


# 加速时缩小，数字可修改，>1则放大
def ctrl_sca():
    global img
    img_sca = pg.transform.scale_by(img, 0.7)
    if sca:
        img = img_sca


def move():
    global x
    global y
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
    # 洁尔佩塔
    if dx == 0:
        if direction == "left":
            img = gilberta
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


while running:
    for ev in pg.event.get():
        # 当点击右上角的叉号(QUIT事件)关闭pg
        if ev.type == pg.QUIT:
            running = False
            break
        # music一曲结束
        elif ev.type == MUSIC_END:
            if music:
                if count < len(music_list) - 1:
                    count += 1
                    music_hear()
                elif count == len(music_list) - 1:
                    count = 0
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
                    if count > 0:
                        count -= 1
                        music_hear()
                    elif count == 0:
                        count = len(music_list) - 1
                        music_hear()
            # x键下一首
            elif ev.key == pg.K_x:
                if pg.mixer.music.get_busy():
                    if count < len(music_list) - 1:
                        count += 1
                        music_hear()
                    elif count == len(music_list) - 1:
                        count = 0
                        music_hear()
    # 要想冇残影得有底色
    screen.fill(0x66ccff)
    # 背景
    screen.blit(backcolor, (0, 0))
    # 酸橙
    screen.blit(decoration, decoration.get_rect(center=(400, 130)))
    # 洁尔佩塔
    move()
    limit()
    # 更新屏幕
    pg.display.update()
    # 设置帧率
    clo.tick(200)

pg.quit()
