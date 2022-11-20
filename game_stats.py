# email liuyibo906@163.com
# 时间 2022/11/8 20:41
class GameStats:
    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_stats()
        #self.ship_left=self.settings.ship_limit
        self.game_active=False
        self.high_score=0
        self.level=1
    def reset_stats(self):
        self.ship_left=self.settings.ship_limit
        self.score=0