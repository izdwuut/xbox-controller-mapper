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
        handle_trackball(event, value, prev)


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


# 2 kierunki osi
def handle_trackball(event, value, prev):
    if event not in prev:
        prev[event] = 0.0
    max = 32767
    ratio = 1
    if event == 'ABS_X':
        prev['ABS_X'] = prev['ABS_X'] + (value / max / ratio)
        print(prev['ABS_X'])
        if prev['ABS_X'] >= 1:
            mouse.move(1, 0, absolute=False)
            prev['ABS_X'] = 0
        elif prev['ABS_X'] <= -1:
            mouse.move(-1, 0, absolute=False)
            prev['ABS_X'] = 0
    if event == 'ABS_Y':
        prev['ABS_Y'] = prev['ABS_Y'] + (-value / max / ratio)
        if prev['ABS_Y'] >= 1:
            mouse.move(0, 1, absolute=False)
            prev['ABS_Y'] = 0
        elif prev['ABS_Y'] <= -1:
            mouse.move(0, -1, absolute=False)
            prev['ABS_Y'] = 0


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
    while True:
        i = i + 1
        for code, state in events.items():
            handle_input(code, state, prev)


def buffer_input(event, events):
    events[event.code] = event.state


if __name__ == '__main__':
    e = Manager().dict()
    prev = Manager().dict()
    p = Process(target=f, args=(e, prev))
    p.start()
    while True:
        for event in get_gamepad():
            # print(event.ev_type, event.code, event.state)
            buffer_input(event, e)
