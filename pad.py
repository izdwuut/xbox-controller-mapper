import keyboard, inputs, mouse
from inputs import get_gamepad


# map BTN_SOUTH to 'A' etc.
def handle_input(event, value):
    # print(event, value)
    max = 32767
    if event == 'BTN_SOUTH':
        mouse.click()
    if event == 'BTN_EAST':
        mouse.click(button='right')
    if event == 'ABS_X':
        x = (value / max) * 10
        print(x)
        mouse.move(x, 0, absolute=False)
    if event == 'ABS_Y':
        y = (value / max) * (-10)
        mouse.move(0, y, absolute=False)


while True:
    for event in get_gamepad():
        # print(event.ev_type)
        handle_input(event.code, event.state)

