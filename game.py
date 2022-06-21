import json
import random
import time
import numpy as np

def get_info():
    with open('conf.json') as f:
       data = json.load(f)
    return data


class FlightChess:
    def __init__(self):
        self.data = [(f'第{i}个动作', -1, -1) for i in range(51)]
        self.chess_pos = [(-1, -1) for i in range(51)]

    def get_issue(self, number):
        return self.data[number]

    def reset(self):
        self.side = 'red'
        self.poses = {'red': 1, 'blue': 1}

    def step(self):
        self.throw()
        self.issue_action()
        self.side = 'red' if self.side=='blue' else 'blue'

    def issue_action(self):
        issue, fix_pos, abs_pos = self.get_issue(self.poses[self.side])
        print(self.side, issue)
        self.show()
        if fix_pos != -1:
            self.poses[self.side] += fix_pos
            issue_action()
        elif abs_pos != -1:
            self.poses[self.side] = abs_pos
            issue_action()

    def game_over(self):
        pass

    def throw(self):
        point = self.shower.throw_show()
        self.poses[self.side] += point
        if self.poses[self.side] > 50:
             self.poses[self.side] =  100 - self.poses[self.side]


class Shower:
    def __init__(self):
        from pyshow import RenderApi
        config = {
            "range_x": [-700, 700],
            "range_y": [-500, 500],
            "display_size": [1400, 1000],
            "tcolor": (0,0,0),
            'bg_img': 'bgp.png',
            'fontsize': 28
        }
        self.render = RenderApi(config)
        self.render.init()
        with open('position.json') as f :
            self.poses = json.load(f)
        self.data = [
            { 'icon': 'obj',   'position': [450, 250],      'side': 'white',    'iconsize': 90  },
            { 'icon': 'chess', 'position': self.poses[0],   'side': 'blue',     'iconsize': 120 },
            { 'icon': 'chess', 'position': self.poses[10],  'side': 'red',      'iconsize': 120 }
        ]


    def throw_show(self):
        for t in range(30):
            p = random.randint(1, 6)
            self.data[0]['icon'] = f'{p}'
            self.render.update({"units": self.infos + self.data})
        time.sleep(1)
        return p

    def update_chess(self, blue_point, red_point):
        blue_old_position =  self.data[1]['position']
        red_old_position =  self.data[2]['position']
        blue_new_postion = self.poses[blue_point]
        red_new_postion = self.poses[red_point]
        blues_x = np.linspace(blue_old_position[0], blue_new_postion[0], 10)
        blues_y = np.linspace(blue_old_position[1], blue_new_postion[1], 10)
        reds_x = np.linspace(red_old_position[0], red_new_postion[0], 10)
        reds_y = np.linspace(red_old_position[1], red_new_postion[1], 10)
        for i in range(10):
            self.data[1]['position'] = [blues_x[i]-2, blues_y[i]]
            self.data[2]['position'] = [reds_x[i]+2, reds_y[i]]
            self.render.update({"units": self.infos + self.data})

    def init_text(self):
        infos = []
        for i in range(50):
            block = [
                {'icon': 'nothing', 'name': '这是测试文本', 'position': [self.poses[i][0]-5, self.poses[i][1]-5],  'side':'blue', 'iconsize': 1, 'textsize': 15},
                {'icon': 'nothing', 'name': '这是测试文本', 'position': [self.poses[i][0]-5, self.poses[i][1]-35],  'side':'blue', 'iconsize': 1, 'textsize': 15},
                {'icon': 'nothing', 'name': '这是测试文本', 'position': [self.poses[i][0]-5, self.poses[i][1]-65],  'side':'blue', 'iconsize': 1, 'textsize': 15}
            ]
            infos.extend(block)
        self.infos = infos

    def update_text(self, info):
        info_data = [
            {'icon': 'nothing', 'name': '这是测试文本'*2, 'position': [250, 30],  'side':'blue', 'iconsize': 1, 'textsize': 28},
            {'icon': 'nothing', 'name': '这是测试文本'*2, 'position': [250, -30],   'side':'blue', 'iconsize': 1, 'textsize': 28},
            {'icon': 'nothing', 'name': '这是测试文本'*2, 'position': [250, -90], 'side':'blue', 'iconsize': 1, 'textsize': 28},
        ]
        self.render.update({"units": self.infos + self.data + info_data})
        time.sleep(1)

if __name__ == '__main__':
    game = Shower()
    game.init_text()
    while True:
        game.throw_show()
        game.update_chess(random.randint(0,49), random.randint(0,49))
        game.update_text('')




