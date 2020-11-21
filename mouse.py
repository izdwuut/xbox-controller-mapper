import ctypes
from input import MouseInput, Inputs, Input


# TODO: global config (mouse left etc.)
# TODO: local config (constants = mouseeventf...)
class Mouse:
    api = ctypes.windll.user32

    click_events = [
        'MOUSE_LEFT',
        'MOUSE_MIDDLE',
        'MOUSE_RIGHT',
    ]
    move_events = {
        'MOUSE_MOVE_X': 1,
        'MOUSE_MOVE_Y': 1,
        'MOUSE_MOVE_-X': -1,
        'MOUSE_MOVE_-Y': -1
    }
    scroll_events = {
        'MOUSE_SCROLL_DOWN',
        'MOUSE_SCROLL_UP'
    }

    def move(self, x, y):
        inputs = Inputs()
        inputs.mi = MouseInput(
            ctypes.c_long(x),
            ctypes.c_long(-y),
            ctypes.c_ulong(0),
            0x001,
            ctypes.c_ulong(0)
        )
        input = Input(ctypes.c_ulong(0), inputs)
        self.api.SendInput(1, ctypes.pointer(input), ctypes.sizeof(input))

    @classmethod
    def button_down(cls, button='MOUSE_LEFT'):
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
        cls.api.SendInput(1, ctypes.pointer(input), ctypes.sizeof(input))

    @classmethod
    def button_up(cls, button='MOUSE_LEFT'):
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
        input = Input(ctypes.c_ulong(0), inputs)
        cls.api.SendInput(1, ctypes.pointer(input), ctypes.sizeof(input))

    @classmethod
    def click(cls, button='lmb'):
        cls.button_down(button)
        cls.button_up(button)
