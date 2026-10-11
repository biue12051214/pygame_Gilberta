import pygame as pg
import math
import os
import random
import sys

# ---------- 打包资源路径兼容 ----------
def resource_path(p):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, p)
    return os.path.join(os.path.abspath("."), p)

# 初始化
pg.mixer.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("洁尔佩塔")
pg.display.set_icon(pg.image.load(resource_path("海边.png")))

direction = "left"

backcolor = pg.transform.scale(pg.image.load(resource_path("背景.jpg")), (800, 600))
backcolor.set_alpha(190)

decoration = pg.transform.scale(pg.image.load(resource_path("直到大地变成一颗酸橙.png")), (600, 200))
decoration.set_alpha(220)

clo = pg.time.Clock()
running = True
x = 600
y = 300
dx = 0
dy = 0
speed = 0
img = None
sca = False
music = True

gilberta = None
gilberta_right = None
gilberta_up = None
gilberta_right_up = None
gilberta_down = None
gilberta_right_down = None
kind = None

last_update = pg.time.get_ticks()

MUSIC_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(MUSIC_END)

music_list = [
    resource_path("高梨康治 - Pendulum.mp3"),
    resource_path("北出菜奈 - 月華 -tsukihana-.mp3"),
    resource_path("洛天依 - 一秒的梦.mp3")
]
count = 0


def music_hear():
    if music:
        pg.mixer.music.load(music_list[count])
        pg.mixer.music.play()


music_hear()

# ---------- 语音 ----------
voice = resource_path("予愿安洁莉娜语音")
voice_num = 0
voices = []
for i in os.listdir(voice):
    if i.lower().endswith(".wav"):
        voices.append(pg.mixer.Sound(os.path.join(voice, i)))


def voice_hear():
    global voice_num
    pg.mixer.stop()
    if voices:
        voice_num = random.randint(0, len(voices) - 1)
        voices[voice_num].play()


# ---------- 帧加载 ----------
def load_frames(folder):
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".png")])
    frames = []
    for f in files:
        image = pg.image.load(os.path.join(folder, f)).convert_alpha()
        frames.append(image)
    return frames


qi = load_frames(resource_path("骑行ｓ"))
song = load_frames(resource_path("送货ｓ"))
zhi = load_frames(resource_path("纸飞机ｓ"))
x_index = 0
y_index = 0


# ---------- 边界 ----------
def limit():
    global x, y
    if x < -150:
        x = 800
    if x > 800:
        x = -150
    if y < -150:
        y = 600
    if y > 600:
        y = -150


# ---------- 缩放 ----------
def ctrl_sca():
    global img
    if sca:
        img = pg.transform.scale_by(img, 0.7)


# ---------- 按 y_index + x_index 生成各方向图 ----------
def gilberta_img():
    global img, gilberta, gilberta_right, gilberta_up
    global gilberta_right_up, gilberta_down, gilberta_right_down, kind

    if y_index == 0:
        kind = song
        base = song[x_index]
    elif y_index == 1:
        kind = zhi
        base = zhi[x_index]
    else:
        kind = qi
        base = qi[x_index]

    img = pg.transform.scale(base, (150, 150))
    gilberta = img
    gilberta_right = pg.transform.flip(img, True, False)
    gilberta_up = pg.transform.rotate(img, -30)
    gilberta_right_up = pg.transform.rotate(gilberta_right, 30)
    gilberta_down = pg.transform.rotate(img, 30)
    gilberta_right_down = pg.transform.rotate(gilberta_right, -30)


# ---------- 按方向选图 ----------
def draw():
    global direction, img
    if direction == "left":
        img = gilberta
    elif direction == "right":
        img = gilberta_right
    elif direction == "up":
        img = gilberta_up
    elif direction == "right_up":
        img = gilberta_right_up
    elif direction == "down":
        img = gilberta_down
    else:
        img = gilberta_right_down

    ctrl_sca()
    screen.blit(img, (x, y))


# ---------- 移动 ----------
def move():
    global x, y, dx, dy, running, speed, direction, sca
    keys = pg.key.get_pressed()

    if keys[pg.K_q]:
        running = False

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

        # 更新方向
        if dy == 0:
            direction = "left" if dx < 0 else "right"
        elif dy > 0:
            direction = "down" if dx < 0 else "right_down"
        else:
            direction = "up" if dx < 0 else "right_up"

    if keys[pg.K_RCTRL] or keys[pg.K_LCTRL]:
        speed = 3.5
        sca = True
    else:
        speed = 1
        sca = False

    x += dx * speed
    y += dy * speed


# ---------- 主循环 ----------
while running:
    now = pg.time.get_ticks()

    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
            break

        elif ev.type == MUSIC_END:
            if music:
                count = (count + 1) % len(music_list)
                music_hear()

        elif ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == pg.BUTTON_LEFT:
                xx, yy = pg.mouse.get_pos()
                x = xx - 30
                y = yy - 30
            elif ev.button == pg.BUTTON_RIGHT:
                voice_hear()

        elif ev.type == pg.MOUSEWHEEL:
            volume = pg.mixer.music.get_volume()
            if ev.y == 1:
                volume = min(1.0, volume + 0.05)
            if ev.y == -1:
                volume = max(0.0, volume - 0.05)
            pg.mixer.music.set_volume(volume)

        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_SPACE:
                if music:
                    if pg.mixer.music.get_busy():
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()

            elif ev.key == pg.K_e:
                music = False
                if pg.mixer.music.get_busy():
                    pg.mixer.music.stop()

            elif ev.key == pg.K_t:
                music = True
                if not pg.mixer.music.get_busy():
                    music_hear()

            elif ev.key == pg.K_r:
                pg.mixer.music.rewind()

            elif ev.key == pg.K_z:
                if pg.mixer.music.get_busy():
                    count = (count - 1) % len(music_list)
                    music_hear()

            elif ev.key == pg.K_x:
                if pg.mixer.music.get_busy():
                    count = (count + 1) % len(music_list)
                    music_hear()

            elif ev.key == pg.K_l:
                y_index = (y_index + 1) % 3
                x_index = 0
                gilberta_img()

    # 1. 切帧
    if now - last_update > 100:
        if kind:
            x_index = (x_index + 1) % len(kind)
        last_update = now

    # 2. 按当前帧生成各方向图
    gilberta_img()

    # 3. 移动
    move()

    # 4. 边界
    limit()

    # 5. 绘制
    screen.fill((102, 204, 255))
    screen.blit(backcolor, (0, 0))
    screen.blit(decoration, decoration.get_rect(center=(400, 130)))
    draw()

    pg.display.update()
    clo.tick(60)

pg.quit()
