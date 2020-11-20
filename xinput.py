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
    api = ctypes.windll.xinput1_4
    AXES_MAPPING = {
        'LEFT_TRIGGER': 'bLeftTrigger',
        'RIGHT_TRIGGER': 'bRightTrigger',
        'LEFT_THUMB_X': 'sThumbLX',
        'LEFT_THUMB_-X': 'sThumbLX',
        'LEFT_THUMB_Y': 'sThumbLY',
        'LEFT_THUMB_-Y': 'sThumbLY',
        'RIGHT_THUMB_X': 'sThumbRX',
        'RIGHT_THUMB_-X': 'sThumbRX',
        'RIGHT_THUMB_Y': 'sThumbRY',
        'RIGHT_THUMB_-Y': 'sThumbRY',
    }
    GAMEPAD_CODES = {
        'XINPUT_GAMEPAD_DPAD_UP': 0x0001,
        'XINPUT_GAMEPAD_DPAD_DOWN': 0x0002,
        'XINPUT_GAMEPAD_DPAD_LEFT': 0x0004,
        'XINPUT_GAMEPAD_DPAD_RIGHT': 0x0008,
        'XINPUT_GAMEPAD_START': 0x0010,
        'XINPUT_GAMEPAD_BACK': 0x0020,
        'XINPUT_GAMEPAD_LEFT_THUMB': 0x0040,
        'XINPUT_GAMEPAD_RIGHT_THUMB': 0x0080,
        'XINPUT_GAMEPAD_LEFT_SHOULDER': 0x0100,
        'XINPUT_GAMEPAD_RIGHT_SHOULDER': 0x0200,
        'XINPUT_GAMEPAD_A': 0x1000,
        'XINPUT_GAMEPAD_B': 0x2000,
        'XINPUT_GAMEPAD_X': 0x4000,
        'XINPUT_GAMEPAD_Y': 0x8000
    }

    def __init__(self, profile):
        self.state = XINPUT_STATE()
        self.gamepad = self.state.Gamepad
        self.config = ConfigParser()
        self.config.read(profile)

    def set_vibration(self, left_motor, right_motor):
        vibration = XINPUT_VIBRATION()
        vibration.wLeftMotorSpeed = left_motor
        vibration.wRightMotorSpeed = right_motor
        self.api.XInputSetState(0, ctypes.byref(vibration))

    def is_button_press(self, button):
        self.get_state()
        if self.GAMEPAD_CODES['XINPUT_GAMEPAD_' + button] & self.gamepad.wButtons:
            return True
        if 'TRIGGER' in button:
            return self.is_trigger_pressed(button)
        return False

    def is_thumb_move(self, thumb):
        position = getattr(self.gamepad, self.AXES_MAPPING[thumb])
        if '-' in thumb:
            return -position > self.get_thumbs_dead_zone()
        return position > self.get_thumbs_dead_zone()

    def is_trigger_pressed(self, trigger):
        return self.get_trigger_value(trigger) > self.get_triggers_dead_zone()

    def get_trigger_value(self, trigger):
        return getattr(self.gamepad, self.AXES_MAPPING[trigger]) & self.config['general'].getint('TRIGGERS_MAGNITUDE')

    def get_axis_value(self, item):
        return getattr(self.gamepad, self.AXES_MAPPING[item])

    def get_normalised_thumb_value(self, thumb):
        value = float(self.get_axis_value(thumb))
        magnitude = int(self.config['general']['THUMBS_MAGNITUDE'])
        sensitivity = float(self.config['general']['SENSITIVITY'])
        return (value / magnitude) * sensitivity

    def get_normalised_trigger_value(self, trigger):
        value = float(self.get_trigger_value(trigger) & 0xff)
        magnitude = int(self.config['general']['TRIGGERS_MAGNITUDE'])
        sensitivity = float(self.config['general']['SENSITIVITY'])
        return (value / magnitude) * sensitivity

    def get_thumbs_dead_zone(self):
        dead_zone = self.config['general'].getfloat('THUMBS_DEAD_ZONE')
        magnitude = self.config['general'].getint('THUMBS_MAGNITUDE')
        return dead_zone * magnitude

    def get_triggers_dead_zone(self):
        dead_zone = self.config['general'].getfloat('TRIGGERS_DEAD_ZONE')
        magnitude = self.config['general'].getint('TRIGGERS_MAGNITUDE')
        return dead_zone * magnitude

    def get_state(self):
        self.api.XInputGetState(ctypes.wintypes.WORD(0), ctypes.pointer(self.state))
