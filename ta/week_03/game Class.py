# coding=utf-8
"""
类的继承与重写类的方法

"""

class Game(object):
    '''
    这是一个关于游戏的类
    '''

    def __init__(self,title,year,month,platforms,type = 'sp'):
        self.title = title
        self.year = year
        self.month = month
        self.platforms = platforms
        self.type = type

    def changePlatforms(self,p = ['swtich','xbox','pc']):
        if not self.platforms:
            self.platforms = p

    def updatePlatforms(self,p = ['swtich','xbox','pc']):
        if p is not list:
            p = [p]

        for x in p:
            if x not in self.platforms:
                self.platforms.append(x)
            else:
                pass

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.title

class ConsonleGame(Game):
    def __init__(self,title,year,month,platforms,type = 'sp',price = 100):
        super(ConsonleGame, self).__init__(title,year,month,platforms,type)
        self.price = price

    
    
my_game = Game(title = 'zz',year = 2024,month = 'mouth',platforms = ['p43'],type = 'sp')
you_game = ConsonleGame(title = 'cc',year = 2014,month = 'mouth',platforms = ['ios'],type = 'mp')
