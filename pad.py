import ctypes, ctypes.wintypes
import mouse, keyboard
from configparser import ConfigParser
from time import sleep
SETTINGS = 'settings.ini'


class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('wButtons', ctypes.wintypes.WORD),
        ('bLeftTrigger', ctypes.wintypes.BYTE),
        ('bRightTrigger', ctypes.wintypes.BYTE),
        ('sThumbLX', ctypes.wintypes.SHORT),
        ('sThumbLY', ctypes.wintypes.SHORT),
        ('sThumbRX', ctypes.wintypes.SHORT),
        ('sThumbRY', ctypes.wintypes.SHORT)
    ]


class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('dwPacketNumber', ctypes.wintypes.DWORD),
        ('Gamepad', XINPUT_GAMEPAD),
    ]


class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [
        ('wLeftMotorSpeed', ctypes.wintypes.WORD),
        ('wRightMotorSpeed', ctypes.wintypes.WORD)
    ]


class XInput:
    XINPUT_GAMEPAD_DPAD_UP = 0x0001
    XINPUT_GAMEPAD_DPAD_DOWN = 0x0002
    XINPUT_GAMEPAD_DPAD_LEFT = 0x0004
    XINPUT_GAMEPAD_DPAD_RIGHT = 0x0008
    XINPUT_GAMEPAD_START = 0x0010
    XINPUT_GAMEPAD_BACK = 0x0020
    XINPUT_GAMEPAD_LEFT_THUMB = 0x0040
    XINPUT_GAMEPAD_RIGHT_THUMB = 0x0080
    XINPUT_GAMEPAD_LEFT_SHOULDER = 0x0100
    XINPUT_GAMEPAD_RIGHT_SHOULDER = 0x0200
    XINPUT_GAMEPAD_A = 0x1000
    XINPUT_GAMEPAD_B = 0x2000
    XINPUT_GAMEPAD_X = 0x4000
    XINPUT_GAMEPAD_Y = 0x8000

    api = ctypes.windll.xinput1_4

    def set_vibration(self, left_motor, right_motor):
        vibration = XINPUT_VIBRATION()
        vibration.wLeftMotorSpeed = left_motor
        vibration.wRightMotorSpeed = right_motor
        self.api.XInputSetState(0, ctypes.byref(vibration))

    def is_button_pressed(self, button):
        if getattr(self, 'XINPUT_GAMEPAD_' + button) & self.gamepad.wButtons:
            return True
        return False

    def __init__(self):
        self.state = XINPUT_STATE()
        self.api.XInputGetState(ctypes.wintypes.WORD(0), ctypes.pointer(self.state))
        self.gamepad = self.state.Gamepad
        self.config = ConfigParser()
        self.config.read(SETTINGS)


class Gamepad():
    buttons = [
        'DPAD_UP',
        'DPAD_DOWN',
        'DPAD_LEFT',
        'DPAD_RIGHT',
        'START',
        'LEFT_THUMB',
        'RIGHT_THUMB',
        'LEFT_SHOULDER',
        'RIGHT_SHOULDER',
        'A',
        'B',
        'X',
        'Y'
    ]

    # TODO: add mouse scroll
    is_mouse_pressed = {
        'MOUSE_LEFT': False,
        'MOUSE_RIGHT': False,
        'MOUSE_MIDDLE': False
    }

    # move to a Keyboard class
    def is_keypress(self, action):
        return False

    def is_mouse_press(self, action):
        if action.upper() in ['MOUSE_LEFT', 'MOUSE_RIGHT', 'MOUSE_MIDDLE']:
            return True
        return False

    def press_key(self, key):
        keyboard.press(key)

    # TODO: refactor
    def press_mouse(self, button):
        if button == 'MOUSE_LEFT' and not self.is_mouse_pressed['MOUSE_LEFT']:
            mouse.hold(button='left')
            self.is_mouse_pressed['MOUSE_LEFT'] = True
        if button == 'MOUSE_RIGHT' and not self.is_mouse_pressed['MOUSE_RIGHT']:
            mouse.hold(button='right')
            self.is_mouse_pressed['MOUSE_RIGHT'] = True
        if button == 'MOUSE_MIDDLE' and not self.is_mouse_pressed['MOUSE_MIDDLE']:
            mouse.hold(button='middle')
            self.is_mouse_pressed['MOUSE_MIDDLE'] = True

    def press_button(self, button):
        action = self.config['controls'][button]
        if not action:
            return
        if self.is_mouse_press(action):
            self.press_mouse(action)
            return
        if self.is_key_press(action):
            self.press_key(action)

    # TODO: refactor
    def release_button(self, button):
        action = self.config['controls'][button]
        if action == 'MOUSE_LEFT' and self.is_mouse_pressed[action]:
            mouse.release(button='left')
        if action == 'MOUSE_RIGHT' and self.is_mouse_pressed[action]:
            mouse.release(button='right')
        if action == 'MOUSE_MIDDLE' and self.is_mouse_pressed[action]:
            mouse.release(button='middle')
        self.is_mouse_pressed[action] = False

    def detect_button_press(self):
        for button in self.buttons:
            if self.xinput.is_button_pressed(button):
                print(button)
                self.press_button(button)
            else:
                self.release_button(button)

    def detect_thumb_move(self):
        pass

    def run(self):
        self.detect_button_press()
        self.detect_thumb_move()

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(SETTINGS)
        self.xinput = XInput()


if __name__ == '__main__':
    xinput = XInput()

    while True:
        gamepad = Gamepad()
        gamepad.run()
        sleep(float(gamepad.config['general']['DELAY']))
