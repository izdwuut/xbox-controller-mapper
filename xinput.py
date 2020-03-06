import ctypes, ctypes.wintypes
from configparser import ConfigParser


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
        self.get_state()
        if getattr(self, 'XINPUT_GAMEPAD_' + button) & self.gamepad.wButtons:
            return True
        return False

    def is_left_thumb_x_move(self):
        if abs(self.gamepad.sThumbLX) > self.get_dead_zone():
            return True
        return False

    # def get_value(self, button):

    def get_dead_zone(self):
        return float(self.config['general']['DEAD_ZONE']) * int(self.config['general']['MAGNITUDE'])

    def get_state(self):
        self.api.XInputGetState(ctypes.wintypes.WORD(0), ctypes.pointer(self.state))

    def __init__(self):
        self.state = XINPUT_STATE()
        self.gamepad = self.state.Gamepad
        from pad import SETTINGS
        self.config = ConfigParser()
        self.config.read(SETTINGS)