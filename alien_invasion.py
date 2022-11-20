# email liuyibo906@163.com
# 时间 2022/11/2 21:08
#图灵书籍文件地址https://www.ituring.com.cn/book/2784
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import  Scoreboard
class AlienInvasion:
    def __init__(self):
        #初始化pygame操作
        pygame.init()
        self.settings=Settings()
        #创建显示窗口，让所有的内容在窗口显示，元组设置宽和高,赋给属性self.screen的对象是一个surface，在pygame中，所有surface是屏幕的一部分，
        #用于显示游戏元素，每个原色都是一个surface,display.set_mode() 返回的surface表示整个游戏窗口
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        #self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width=self.screen.get_rect().width
        #self.settings.screen_height=self.screen.get_rect().height
        #设置窗口名字
        pygame.display.set_caption("Alien Invasion")
        self.stats=GameStats(self)
        #设置背景颜色颜色,使用settings后注
        #self.bg_color=(230,230,230)
        self.ship=Ship(self)
        #创建一个编组，存储有效的子弹，是pygame.sprite.Group类的一个实例
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._creat_fleet()
        #创建按钮对象
        self.button=Button(self,'play')
        #创建积分
        self.sb=Scoreboard(self)
    def run_gage(self):
        #开始游戏主循环
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                #方法fill()用于处理surface,背景色填充屏幕，每次循环都会重新绘制
            self._update_screen()
    #新增方法检查用户是否退出
    def _check_events(self):
        # 监视键盘和鼠标操作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    def _check_keydown_event(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_event(self,event):
        if event.key==pygame.K_LEFT:
            self.ship.moving_left=False
        elif event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_ESCAPE:
            sys.exit()
    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:
            #创建新子弹，添加到group中
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_alien_collisinos()

    def _check_bullet_alien_collisinos(self):
        #检查是否有子弹击中了外行人,检测每个子弹和每个外星人的rect,如果一致，True,表示消失
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if collisions:
            for alien in collisions.values():
                self.stats.score+=self.settings.alien_points*len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._creat_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

    def _creat_fleet(self):
        alien=Alien(self)
        alien_width=alien.rect.width
        alien_height=alien.rect.height
        available_space_x=self.settings.screen_width-2*alien_width
        number_aliens_x=available_space_x//(2*alien_width)
        #计算屏幕可以容纳多少行外星人
        ship_height=self.ship.rect.height
        available_space_y=self.settings.screen_height-3*alien_height-ship_height
        number_aliens_y=available_space_y//(2*alien_height)
        for row_number in range(number_aliens_y):
            for alien_number in range(number_aliens_x):
                self._creat_aliens(alien_number,row_number)

    def _creat_aliens(self,alien_number,row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height=alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y=alien_height+2*alien_height*row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #返回第一个碰撞的对象
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            #print('ship hit!!!')
            self._ship_hit()
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._check_fleet_direction()
                break
    def _check_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
    def _ship_hit(self):
        if self.stats.ship_left>0:
            self.stats.ship_left-=1
            self.sb.prep_ship()
            self.aliens.empty()
            self.bullets.empty()
            self._creat_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active=False
            #当游戏结束，鼠标可见
            pygame.mouse.set_visible(True)
    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for aline in self.aliens.sprites():
            if aline.rect.bottom>screen_rect.bottom:
                self._ship_hit()
                break
    #检查鼠标的位置是否再button的rect范围内
    def _check_play_button(self,mouse_pos):
        button_check=self.button.rect.collidepoint(mouse_pos)
        if button_check and not self.stats.game_active:
            #重置游戏统计信息,和分数
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()
            self.stats.game_active= True
            #当游戏开始鼠标不可见
            pygame.mouse.set_visible(False)
            #清空外乡人和idan
            self.aliens.empty()
            self.bullets.empty()
            #创建外乡人，归位
            self._creat_fleet()
            self.ship.center_ship()
            self.settings.initialiaze_dynamic_settings()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        #如果游戏处于非活动状态，绘制play按钮
        if not self.stats.game_active:
            self.button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()
if __name__=='__main__':
    ai=AlienInvasion()
    ai.run_gage()
