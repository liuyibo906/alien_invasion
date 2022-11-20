# email liuyibo906@163.com
# 时间 2022/11/3 20:42
import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    def __init__(self,ai_geme):
        super().__init__()
        self.screen=ai_geme.screen
        self.settings=ai_geme.settings
        self.color=self.settings.bullet_color
    #在(0,0)处创建一个子弹的矩形,pygame.Ract类创建一个矩形
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_geme.ship.rect.midtop
        self.y=float(self.rect.y)
    def update(self):
        self.y-=self.settings.bullet_speed
        self.rect.y=self.y
    #屏幕绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)

