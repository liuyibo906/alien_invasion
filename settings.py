# email liuyibo906@163.com
# 时间 2022/11/2 21:32
class Settings:
    def __init__(self):
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)
        #飞船信息
        self.ship_limit=3
        #添加子弹的设置,像素大小
        self.bullet_width=3000
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullets_allowed=3
        #外星人信息
        self.fleet_drop_speed=100
        self.speedup_scale=1.1
        self.score_scale=1.5
        self.initialiaze_dynamic_settings()

    def initialiaze_dynamic_settings(self):
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=1.0
        self.fleet_direction=1
        self.alien_points = 50
    def increase_speed(self):
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.alien_speed
        self.alien_points= int(self.score_scale*self.alien_points)
        print(self.alien_points)