import ctypes
import ctypes.wintypes


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

    def __init__(self, config):
        self.state = XINPUT_STATE()
        self.gamepad = self.state.Gamepad
        self.config = config

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
        return abs(self.get_trigger_value(trigger)) > self.get_triggers_dead_zone()

    def get_trigger_value(self, trigger):
        return float(getattr(self.gamepad, self.AXES_MAPPING[trigger]) & 0xFF)

    def get_axis_value(self, item):
        return float(getattr(self.gamepad, self.AXES_MAPPING[item]))

    @classmethod
    def get_normalised_value(cls, raw_value, magnitude, sensitivity):
        return (raw_value / magnitude) * sensitivity

    def get_normalised_thumb_value(self, thumb):
        return self.get_normalised_value(
            self.get_axis_value(thumb),
            self.config.getint('THUMBS_MAGNITUDE'),
            self.config.getfloat('SENSITIVITY')
        )

    def get_normalised_trigger_value(self, trigger):
        return self.get_normalised_value(
            self.get_trigger_value(trigger),
            self.config.getint('TRIGGERS_MAGNITUDE'),
            self.config.getfloat('SENSITIVITY')
        )

    @classmethod
    def get_dead_zone(cls, raw_dead_zone, magnitude):
        return raw_dead_zone * magnitude

    def get_thumbs_dead_zone(self):
        return self.get_dead_zone(
            self.config.getfloat('THUMBS_DEAD_ZONE'),
            self.config.getint('THUMBS_MAGNITUDE')
        )

    def get_triggers_dead_zone(self):
        return self.get_dead_zone(
            self.config.getfloat('TRIGGERS_DEAD_ZONE'),
            self.config.getint('TRIGGERS_MAGNITUDE')
        )

    def get_state(self):
        self.api.XInputGetState(ctypes.wintypes.WORD(0), ctypes.pointer(self.state))
