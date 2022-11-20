# email liuyibo906@163.com
# 时间 2022/11/2 21:58
import pygame.image
from pygame.sprite import  Sprite


class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        #初始化飞船并设置其初始位置
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()
        #加载飞船图像，获取其外接矩形
        self.image=pygame.image.load('image/ship.bmp')
        self.rect=self.image.get_rect()
        #对于每艘飞船，将其放在屏幕底部中央
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        self.moving_right=False
        self.moving_left=False
    def blitme(self):
        #在指定位置绘制图像
        self.screen.blit(self.image,self.rect)
    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
        #根据self.x 更新rect对象。self.rect.x只存储整数部分
        self.rect.x=self.x
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)

