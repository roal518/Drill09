# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *

def space_down(e):
    return e[0] =='INPUT' and e[1].type ==SDL_KEYDOWN and e[1].key ==SDLK_SPACE
def time_out(e):
    return e[0] == 'TIME_OUT'
def auto(e):
    return e[0] =='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def time_out(e):
    return e[0] == 'TIME_OUT'
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Idle:
    @staticmethod
    def enter(boy, e):
        boy.action = 3
        boy.start_time = get_time()
        print('Idle Enter - 고개숙이기')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit - 고개 들기')

    @staticmethod
    def do(boy):
        print('Idle Do - ZZZ')
        boy.frame = (boy.frame+1) % 7
        if get_time()-boy.start_time > 4:
            boy.state_machine.handle_event(('TIME_OUT',0))
    @staticmethod
    def draw(boy):
        if boy.state == 0:
            boy.image.clip_draw(boy.frame*100,boy.action*100,100,100,boy.x,boy.y)
        elif boy.state == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          0, 'h', boy.x, boy.y, 100, 100)
        pass
class Auto_Run:
    @staticmethod
    def enter(boy,e):
        boy.action = 1
        boy.auto_start_time = get_time()
    @staticmethod
    def exit(boy,e):
        print('Idle Exit - 고개 들기')

    @staticmethod
    def do(boy):
        print('Idle Do - ZZZ')
        boy.frame = (boy.frame+1) % 7

        if boy.state == 0:
            boy.x += 3
            if boy.x > 800:
                boy.state = 1
        elif boy.state == 1:
            boy.x -= 3
            if boy.x < 0:
                boy.state = 0
        if get_time() - boy.auto_start_time > 3:
            boy.state_machine.handle_event(("TIME_OUT",0))
    @staticmethod
    def draw(boy):
        if boy.state == 0:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y*1.3-25,130,130)
        elif boy.state == 1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                          0, 'h', boy.x, boy.y*1.3-25, 130, 130)
class Sleep:
    @staticmethod
    def enter(boy,e):
        boy.frame = 0
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1) % 8

    @staticmethod
    def draw(boy):
        if boy.state == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
            boy.state = 0
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0
            boy.state = 1
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
class StateMachine:
    def __init__(self,boy):
        #boy는 소년 객체
        self.cur_state = Idle
        self.boy = boy
        self.transitions = {
            Sleep: {space_down:Idle,right_down:Run,left_down:Run,
                    right_up:Run,left_up:Run,auto:Auto_Run},
            Idle: {auto: Auto_Run, right_down:Run, left_down:Run,
                   right_up:Run,left_up:Run,time_out:Sleep},
            Run:{right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Auto_Run: {time_out: Idle}
        }
    def handle_event(self,e):
        for check_event,next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy,e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy,e)
                return True
        return False
    def start(self):
        self.cur_state.enter(self.boy,('NONE',0))
    def update(self):
        self.cur_state.do(self.boy)
    def draw(self):
        self.cur_state.draw(self.boy)




class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 1
        self.action = 3 #SHEET LOCATION
        self.state = 0 #LEFT or RIGHT with start right
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        #
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()
