import ctypes
from input import MouseInput, Inputs, Input
import math

# TODO: global config (mouse left etc.)
# TODO: local config (constants = mouseeventf...)
class Mouse:
    api = ctypes.windll.user32

    click_events = [
        'MOUSE_LEFT',
        'MOUSE_MIDDLE',
        'MOUSE_RIGHT',
    ]
    move_events = [
        'MOUSE_MOVE_X',
        'MOUSE_MOVE_Y',
        'MOUSE_MOVE_-X',
        'MOUSE_MOVE_-Y'
    ]
    scroll_events = {
        'MOUSE_SCROLL_DOWN',
        'MOUSE_SCROLL_UP'
    }

    MOUSEEVENTF_WHEEL = 0x0800
    WHEEL_DELTA = 120

    def __init__(self, config):
        self.config = config

    def move(self, x, y):
        inputs = Inputs()
        inputs.mi = MouseInput(
            ctypes.c_long(x),
            ctypes.c_long(-y),
            ctypes.c_ulong(0),
            0x001,
            ctypes.c_ulong(0)
        )
        input_ = Input(ctypes.c_ulong(0), inputs)
        self.api.SendInput(1, ctypes.pointer(input_), ctypes.sizeof(input_))

    # TODO: make hardcoded values consts
    def button_down(self, button='MOUSE_LEFT'):
        inputs = Inputs()
        if button == 'MOUSE_LEFT':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                ctypes.c_ulong(0),
                0x002,
                ctypes.c_ulong(0)
            )
        elif button == 'MOUSE_MIDDLE':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                ctypes.c_ulong(0),
                0x020,
                ctypes.c_ulong(0)
            )
        elif button == 'MOUSE_RIGHT':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                ctypes.c_ulong(0),
                0x008,
                ctypes.c_ulong(0)
            )
        else:
            raise Exception('Invalid mouse button.')
        input = Input(ctypes.c_ulong(0), inputs)
        self.api.SendInput(1, ctypes.pointer(input), ctypes.sizeof(input))

    def button_up(self, button='MOUSE_LEFT'):
        inputs = Inputs()
        if button == 'MOUSE_LEFT':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                ctypes.c_ulong(0),
                0x004,
                ctypes.c_ulong(0)
            )
        elif button == 'MOUSE_MIDDLE':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                ctypes.c_ulong(0),
                0x040,
                ctypes.c_ulong(0)
            )
        elif button == 'MOUSE_RIGHT':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                ctypes.c_ulong(0),
                0x010,
                ctypes.c_ulong(0)
            )
        else:
            raise Exception('Invalid mouse button.')
        input_ = Input(ctypes.c_ulong(0), inputs)
        self.api.SendInput(1, ctypes.pointer(input_), ctypes.sizeof(input_))

    def click(self, button='MOUSE_LEFT'):
        self.button_down(button)
        self.button_up(button)

    def get_scroll_delta(self):
        return math.ceil(self.WHEEL_DELTA * self.config.getfloat('SCROLL_SPEED'))

    def scroll(self, button):
        inputs = Inputs()
        if button == 'MOUSE_SCROLL_UP':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                self.get_scroll_delta(),
                self.MOUSEEVENTF_WHEEL,
                ctypes.c_ulong(0)
            )
        elif button == 'MOUSE_SCROLL_DOWN':
            inputs.mi = MouseInput(
                ctypes.c_long(0),
                ctypes.c_long(0),
                -self.get_scroll_delta(),
                self.MOUSEEVENTF_WHEEL,
                ctypes.c_ulong(0)
            )
        else:
            raise Exception('Wrong scroll event.')
        input = Input(ctypes.c_ulong(0), inputs)
        self.api.SendInput(1, ctypes.pointer(input), ctypes.sizeof(input))