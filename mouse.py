import ctypes


# TODO: use input module
class Mouse:
    api = ctypes.windll.user32

    def move(self, x, y):
        self.api.mouse_event(0x001, x, -y, 0, 0)

    @classmethod
    def button_down(cls, button='lmb'):
        if button == 'lmb':
            cls.api.mouse_event(0x002, 0, 0, 0, 0)
        elif button == 'mmb':
            cls.api.mouse_event(0x020, 0, 0, 0, 0)
        elif button == 'rmb':
            cls.api.mouse_event(0x008, 0, 0, 0, 0)
        else:
            raise Exception('Invalid mouse button.')

    @classmethod
    def button_up(cls, button='lmb'):
        if button == 'lmb':
            cls.api.mouse_event(0x004, 0, 0, 0, 0)
        elif button == 'mmb':
            cls.api.mouse_event(0x040, 0, 0, 0, 0)
        elif button == 'rmb':
            cls.api.mouse_event(0x010, 0, 0, 0, 0)
        else:
            raise Exception('Invalid mouse button.')

    @classmethod
    def click(cls, button='lmb'):
        cls.button_down(button)
        cls.button_up(button)

