import pygame
import sys
import ctypes
import random
from pygame import gfxdraw
import numpy as np
import pynput
import os
import time
from pynput.mouse import Controller, Button
from pynput import mouse as ms
pygame.init()
mouse=Controller()
listener=ms.Listener()
is_pressed=False
hang=False
roll_=False
roll_neg=False
sptext=False
spchoices=['sleep']
with open('resources/specialdays.txt','r') as f:
    daysandgreet=f.readlines()
daygreet={}
for day_ in daysandgreet:
    day,greet=day_.split(':',1)
    daygreet[f'{day}']=greet
t=time.gmtime()
date=time.strftime("%Y-%m-%d %H:%M:%S",t)
spgreets=[]
for key,value in daygreet.items():

    if key==''.join(date[5:10]):
        sptext=True
        spgreets.append(''.join(value[:-1]))

print(daygreet)
def on_scroll(x, y, dx, dy):
    global roll_
    global roll_neg
    if dy<0:
        roll_neg=False
        roll_=True
    else:
        roll_neg=True

        roll_=False



def on_click(x,y,button,pressed):
    global is_pressed
    global pet_loc
    is_pressed=pressed
    if pressed:
        print('down')
    else:
        print('released')
        global hang
        hang=False
        is_pressed=False
        button=False
    
    if is_pressed and abs(pet_loc[0]-mouse_x)<40 and abs(pet_loc[1]-mouse_y)<40:
        if button == ms.Button.left:
            print('dragging')
            hang=True
        elif button == ms.Button.right:
            pass
            

listener.on_click=on_click
listener.on_scroll=on_scroll

listener.start()
'''mouse = Controller()
# 模拟左键点击
mouse.click(Button.left)
# 模拟右键点击
mouse.click(Button.right)'''

# 初始化 Pygame

def get_screen_size():
    info = pygame.display.Info()  # 获取屏幕信息
    screen_width = info.current_w  # 获取屏幕宽度
    screen_height = info.current_h  # 获取屏幕高度
    return screen_width, screen_height  # 返回屏幕尺寸
# 设置窗口尺寸
WIDTH, HEIGHT = get_screen_size()
#pygame.NOFRAME
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.NOFRAME)
pygame.display.set_caption("小孤独")
icon_surface = pygame.image.load("littlepink.png")  # 准备PNG源文件
pygame.display.set_icon(icon_surface)
# 设置窗口透明
hwnd = pygame.display.get_wm_info()["window"]



# 设置窗口扩展样式
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20

# 获取当前扩展样式
extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

# 添加透明和层叠样式
extended_style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, extended_style)

# 设置窗口透明度 (0=完全透明, 255=完全不透明)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 0, 0x00000001)



'''class Particle:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.birth=time.time()
    def draw(self):
        pygame.draw.circle(screen,(190,255,190,255),(self.x,self.y),random.randint(20,30)*0.1,0)
        pygame.draw.circle(screen,(190,255,190,2),(self.x,self.y),random.randint(20,30)*0.3,0)

        pygame.draw.circle(screen,(190,255,190),(self.x+random.randint(-50,50)*0.1,self.y+random.randint(-50,50)*0.01),random.randint(40,50)*0.02,0)'''

# 主循环

path="images/"
paths=os.listdir(path)
allactions=[]
allactions_name=[]
for actions in paths:
    locals()[f'{actions}']=[]
    pathe=os.listdir(f"images/{actions}")
    for pics in pathe:
        thispic=pygame.image.load(f"images/{actions}/"+pics)
        locals()[f'{actions}'].append(thispic)

    allactions.append(locals()[f'{actions}'])
    allactions_name.append(f'{actions}')
print(allactions)
print(allactions_name)

class Actdoer():
    def __init__(self,actname,period):
        self.period=period
        self.indexing=allactions_name.index(f'{actname}')
        self.toact=allactions[self.indexing]
        self.len_of_act=len(self.toact)
        self.index_count=0
        global mouse_x,mouse_y
        self.present=time.time()
        self.past=self.present-self.period
        self.x=600
        self.y=600
    def doact(self):
        self.index=self.index_count%self.len_of_act
        self.motion()
        screen.blit(self.toact[self.index],(self.x-44,self.y-60))
        
        self.present=time.time()
        if self.present-self.past>self.period:
            self.past=self.present
            self.index_count+=1
            
        
        return [self.x,self.y]
    def motion():
        pass
class Speaking():
    def __init__(self):
        
        self.font = pygame.font.Font(None,25)

    def print_screen(self,tex,loc,color):
        self.tex=tex

        self.loc=loc
        self.color=color
        
        #pygame.draw.rect(screen,[250,200,200],[loc[0]+30,loc[1]-40-self.text_len,40,self.text_len*15],0)
        self.text=self.font.render(self.tex,True,self.color)
        screen.blit(self.text,(self.loc[0]+35,self.loc[1]-40))

just_fall=False
class DoLeft(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
    def motion(self):
        self.x-=2
class DoRright(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
    def motion(self):
        self.x+=2
class DoStill(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
    def motion(self):
        if self.index_count<12:
            self.index=0
        elif self.index==self.len_of_act-1:
            self.index_count=0


        
            
class DoFall(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
        
    def motion(self):
        self.y+=10
        
class DoFell(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)       
    def motion(self):
        if self.index_count<3:
            self.index=0
        
        elif self.index==self.len_of_act-1:
           
            global just_fall
            
            just_fall=False
            
class DoRoll(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)       
    def motion(self):
        if self.index==self.len_of_act-1:
            global roll_
            roll_=False
class DoRollNeg(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)       
    def motion(self):
        if self.index==self.len_of_act-1:
            global roll_neg
            roll_neg=False
class DoDrag(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
    def motion(self):
        self.y=mouse_y+20
        self.x=mouse_x-30
class DoProbe(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
    def motion(self):
        pass
class DoProbeNeg(Actdoer):
    def __init__(self,actname,period):
        super().__init__(actname,period)
    def motion(self):
        pass
clock = pygame.time.Clock()
running = True
pet_loc=[100,100]
DoActions=[]
##初始化字
speaking=Speaking()
##手动初始化动作
right_act=DoRright('right',0.06)
DoActions.append(right_act)
left_act=DoLeft('left',0.06)
DoActions.append(left_act)
still_act=DoStill('still',0.2)
DoActions.append(still_act)
fall_act=DoFall('fall',0.04)
DoActions.append(fall_act)
drag_act=DoDrag('drag',0.07)
DoActions.append(drag_act)
probe_act=DoProbe('probe',0.2)
DoActions.append(probe_act)
probe_neg_act=DoProbeNeg('probe_neg',0.2)
DoActions.append(probe_neg_act)
fell_act=DoFell('fell',0.2)
DoActions.append(fell_act)
roll_act=DoRoll('roll',0.1)
DoActions.append(roll_act)
roll_neg_act=DoRollNeg('roll_neg',0.1)
DoActions.append(roll_neg_act)
if sptext==True:

    speaktext=spgreets[0]
else:
    speaktext=''
while running:
    #ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)
    present=time.time()
    screen.fill((0, 0, 0, 0))
    mouse_x, mouse_y = mouse.position

    
    #part=Particle(mouse_x,mouse_y)
    #part.draw()

    if hang==True:
        pet_loc=drag_act.doact()
        done_act=drag_act
    
    elif pet_loc[1]<=HEIGHT-85:
        pet_loc=fall_act.doact()
        done_act=fall_act
        just_fall=True
    elif just_fall==True:
        pet_loc=fell_act.doact()
        done_act=fell_act
    elif roll_==True:
     
        pet_loc=roll_act.doact()
        done_act=roll_act
    elif roll_neg==True:
        pet_loc=roll_neg_act.doact()
        done_act=roll_neg_act
    elif abs(pet_loc[0]-mouse_x)<=30:
        if pet_loc[1]>=mouse_y+60:

            pet_loc=still_act.doact()
            done_act=still_act
        elif abs(pet_loc[1]-mouse_y)<60:
            pet_loc=still_act.doact()
            done_act=still_act
    elif pet_loc[0]<=20:
        pet_loc=probe_act.doact()
        done_act=probe_act
    elif pet_loc[0]>=WIDTH-30:
        pet_loc=probe_neg_act.doact()
        done_act=probe_neg_act
    elif mouse_x-pet_loc[0]>10:
        pet_loc=right_act.doact()
        done_act=right_act
    elif pet_loc[0]-mouse_x>10:
        pet_loc=left_act.doact()
        done_act=left_act
    
    speaking.print_screen(speaktext,pet_loc,[235,145,145])


    
    for acts in DoActions:
        if acts!=done_act:

            acts.x,acts.y=pet_loc
            acts.index=0
            acts.index_count=0

   

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            listener.stop()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()
listener.stop()
