# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *


def auto_run(e):
    return e[0] =='INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def time_out(e):
    return e[0] == 'TIME_OUT'
class Idle:
    @staticmethod
    def enter(boy):
        print('Idle Enter - 고개숙이기')
        boy.idle_start_time = get_time()

    @staticmethod
    def exit(boy):
        print('Idle Exit - 고개 들기')

    @staticmethod
    def do(boy):
        print('Idle Do - ZZZ')
        boy.frame=(boy.frame+1)%7
        if get_time() - boy.idle_start_time > 3:
            boy.state_machine.handle_event(("TIME_OUT",0))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100,boy.action*100,100,100,boy.x,boy.y)
        pass




class StateMachine:
    def __init__(self,boy):
        #boy는 소년 객체
        self.cur_state = Sleep
        self.boy = boy
        self.transitions = {
            Sleep: {space_down: Idle},
            Idle: {time_out: Sleep},

        }
    def handle_event(self,e):
        for check_event,next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
                return True
        return False
    def start(self):
        self.cur_state.enter(self.boy)
    def update(self):
        self.cur_state.do(self.boy)
    def draw(self):
        self.cur_state.draw(self.boy)




class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 1
        self.action = 3
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
