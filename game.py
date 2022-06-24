import json
import random
import time
import numpy as np
from tools import gen_position
from multiprocessing import Process, Queue
from render import pipeline as RenderFunc 


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
            "range_x": [0, 1920],
            "range_y": [0, 1080],
            "display_size": [2560, 1600],
            #"display_size": [160, 90],
            "tcolor": (0,0,0),
            'bg_img': 'new_bg.png',
            'fontsize': 28
        }

        self.qin = Queue()
        self.qout  = Queue()
        self.render_process = Process(target = RenderFunc, args = (self.qin, self.qout, config))     
        self.render_process.daemon = True
        self.render_process.start()
        self.now_blue = True
        self.blue_point = 0
        self.red_point = 0

        self.poses = gen_position()
        self.data = [
            { 'icon': 'obj',   'position': [1500, 770],      'side': 'white',    'iconsize': 96 },
            { 'icon': 'chess', 'position': self.poses[0],   'side': 'blue',     'iconsize': 128 },
            { 'icon': 'chess', 'position': self.poses[0],  'side': 'red',      'iconsize': 128 }
        ]

    def throw_show(self):
        for t in range(20):
            p = random.randint(1, 6)
            self.data[0]['icon'] = f'{p}'
            self.update({"units": self.infos + self.data})
        time.sleep(1)
        return p

    def update_chess(self, blue_point, red_point):
        blue_old_position =  self.data[1]['position'] 
        red_old_position =  self.data[2]['position']
        blue_new_postion = self.poses[blue_point]
        red_new_postion = self.poses[red_point]

        blues_x = np.linspace(blue_old_position[0]+20, blue_new_postion[0], 30)
        blues_y = np.linspace(blue_old_position[1], blue_new_postion[1], 30)
        reds_x = np.linspace(red_old_position[0]-20, red_new_postion[0], 30)
        reds_y = np.linspace(red_old_position[1], red_new_postion[1], 30)
        for i in range(30):
            self.data[1]['position'] = [blues_x[i]-20, blues_y[i]]
            self.data[2]['position'] = [reds_x[i]+20, reds_y[i]]
            self.update({"units": self.infos + self.data})

    def init_text(self):
        infos = []
        for i in range(1,49):
            block = [
                {'icon': 'nothing', 'name': '这是测试文本', 'position': [self.poses[i][0]-5, self.poses[i][1]-5],  'side':'blue', 'iconsize': 1, 'textsize': 26},
                {'icon': 'nothing', 'name': '这是测试文本', 'position': [self.poses[i][0]-5, self.poses[i][1]-35],  'side':'blue', 'iconsize': 1, 'textsize': 26},
                {'icon': 'nothing', 'name': '这是测试文本', 'position': [self.poses[i][0]-5, self.poses[i][1]-65],  'side':'blue', 'iconsize': 1, 'textsize': 26}
            ]
            infos.extend(block)
        self.infos = infos

    def update_text(self, info):
        info_data = [
            {'icon': 'nothing', 'name': '这是测试文本'*2, 'position': [1280, 590],  'side':'blue', 'iconsize': 1, 'textsize': 42},
            {'icon': 'nothing', 'name': '这是测试文本'*2, 'position': [1280, 515],   'side':'blue', 'iconsize': 1, 'textsize': 42},
            {'icon': 'nothing', 'name': '这是测试文本'*2, 'position': [1280, 440], 'side':'blue', 'iconsize': 1, 'textsize': 42},
        ]
        self.update({"units": self.infos + self.data + info_data})
        time.sleep(1)
        
    def update(self, obs):
        self.qin.put(obs)
        time.sleep(.03)

    def run(self):
        game.update_chess(0, 0)
        game.update_text('')
        while True:
            time.sleep(.05)
            if self.qout and not self.qout.empty():
                issue = self.qout.get()
                print(issue)
                point = self.throw_show()
                if self.now_blue :
                    self.blue_point += point
                else:
                    self.red_point += point
                self.now_blue = not self.now_blue
                game.update_chess(self.blue_point, self.red_point)
                game.update_text('')
            


if __name__ == '__main__':
    game = Shower()
    game.init_text()
    while True:
        game.run()
        #game.update_chess(random.randint(0,48), random.randint(0,48))
        #game.update_text('')




