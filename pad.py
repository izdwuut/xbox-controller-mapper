import keyboard, inputs, mouse
from inputs import get_gamepad


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


while True:
    for event in get_gamepad():
        # print(event.ev_type)
        handle_input(event.code, event.state)
        if 'BTN' in event.code:
            print(event.ev_type)



