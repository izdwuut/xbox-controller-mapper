import keyboard, mouse
from inputs import get_gamepad
from multiprocessing import Process, Manager
from constants import BTN_PRESSED, BTN_NOT_PRESSED

# map BTN_SOUTH to 'A' etc.
def handle_input(event, value, prev):
    if 'BTN' in event:
        handle_button(event, value, prev)
    if 'HAT' in event:
        handle_hat(event, value)
    if 'ABS' in event:
        handle_trackball(event, value)


def handle_hat(event, state):
    if not state:
        return
    if 'X' in event:
        if state == 1:
            x = 1
        elif state == -1:
            x = -1
        mouse.move(x, 0, absolute=False)
    elif 'Y' in event:
        if state == 1:
            y = 1
        elif state == -1:
            y = -1
        mouse.move(0, y, absolute=False)


def handle_trackball(event, value):
    max = 32767
    if event == 'ABS_X':
        x = (value / max) * 10
        mouse.move(x, 0, absolute=False)
    if event == 'ABS_Y':
        y = (value / max) * (-10)
        mouse.move(0, y, absolute=False)


        # y = (value / max) * (-10)
        s[1] = s[1] + (value / max /10000)
        if s[1] > 1:
            s[1] = 1
        mouse.move(0, int(s[1]), absolute=False)


def handle_button(event, state, prev):
    if state == BTN_PRESSED:
        if event not in prev or prev[event] == BTN_NOT_PRESSED:
            if event == 'BTN_SOUTH':
                mouse.press()
            if event == 'BTN_EAST':
                mouse.press(button='right')
            prev[event] = BTN_PRESSED
    else:
        if mouse.is_pressed():
            mouse.release()
        if mouse.is_pressed(button='right'):
            mouse.release(button='right')
        prev[event] = BTN_NOT_PRESSED


def f(events, prev):
    i = 1
    # print(events)
    while True:
        i = i + 1
        # print(events.events)
        # print(str(i))
        for code, state in events.items():
            handle_input(code, state, prev)


def buffer_input(event, events):
    events[event.code] = event.state


if __name__ == '__main__':
    e = Manager().dict()
    prev = Manager().dict()
    # s = Array('d', [0.0, 0.0])
    # print(e)
    p = Process(target=f, args=(e, prev))
    p.start()

    while True:
        for event in get_gamepad():
            # print(event.ev_type)
            # handle_input(event.code, event.state)
            print(event.ev_type, event.code, event.state)
            buffer_input(event, e)
            # p.join()
            # print(e)


