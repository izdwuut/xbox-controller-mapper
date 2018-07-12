import keyboard, inputs, mouse
from inputs import get_gamepad
from multiprocessing import Process, Manager
from constants import *


# map BTN_SOUTH to 'A' etc.
def handle_input(event, value):
    if 'BTN' in event:
        handle_button(event, value)
    if 'ABS' in event:
        handle_trackball(event, value)


def handle_trackball(event, value):
    max = 32767
    if event == 'ABS_X':
        x = (value / max) * 10
        mouse.move(x, 0, absolute=False)
    if event == 'ABS_Y':
        y = (value / max) * (-10)
        mouse.move(0, y, absolute=False)


def handle_button(event, state):
    if not state:
        return
    if event == 'BTN_SOUTH':
        mouse.click()
    if event == 'BTN_EAST':
        mouse.click(button='right')


class Events:
    def __init__(self):
        self.events = {}


def f(events):
    i = 1
    print(events)
    while True:
        i = i + 1
        # print(events.events)
        # print(str(i))
        for code, state in events.items():
            handle_input(code, state)


def buffer_input(event, events):
    events[event.code] = event.state


if __name__ == '__main__':
    e = Manager().dict()
    print(e)
    p = Process(target=f, args=(e,))
    p.start()

    while True:
        for event in get_gamepad():
            # print(event.ev_type)
            # handle_input(event.code, event.state)
            # print(event.ev_type, event.code, event.state)
            buffer_input(event, e)
            # p.join()
            print(e)


