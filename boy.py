# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *


def auto(e):
    return e[0] =='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def time_out(e):
    return e[0] == 'TIME_OUT'
class Idle:
    @staticmethod
    def enter(boy, e):
        print('Idle Enter - 고개숙이기')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit - 고개 들기')

    @staticmethod
    def do(boy):
        print('Idle Do - ZZZ')
        boy.frame = (boy.frame+1) % 7
    @staticmethod
    def draw(boy):
        if boy.action == 3:
            boy.action= 3
            boy.image.clip_draw(boy.frame*100,boy.action*100,100,100,boy.x,boy.y)
        elif boy.action == 3:

            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          0, 'h', boy.x, boy.y, 100, 100)
        pass

class Auto_Run:
    @staticmethod
    def enter(boy,e):
        boy.auto_start_time = get_time()

    @staticmethod
    def exit(boy,e):
        print('Idle Exit - 고개 들기')

    @staticmethod
    def do(boy):
        print('Idle Do - ZZZ')
        boy.frame = (boy.frame+1) % 7


        if get_time() - boy.auto_start_time > 3:
            boy.state_machine.handle_event(("TIME_OUT",0))
    @staticmethod
    def draw(boy):
        if boy.action == 1:
            boy.image.clip_draw(boy.frame*100,boy.action*100,100,100,boy.x,boy.y)
        elif boy.action == 1:
            boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class StateMachine:
    def __init__(self,boy):
        #boy는 소년 객체
        self.cur_state = Idle
        self.boy = boy
        self.transitions = {
            Idle: {auto: Auto_Run},
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
        self.state = 0 #IDLE or AUTO
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
