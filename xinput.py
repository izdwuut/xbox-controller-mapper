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
    axes_mapping = {
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

    def __init__(self):
        self.state = XINPUT_STATE()
        self.gamepad = self.state.Gamepad
        self.config = ConfigParser()
        self.config.read('settings.ini')

    def set_vibration(self, left_motor, right_motor):
        vibration = XINPUT_VIBRATION()
        vibration.wLeftMotorSpeed = left_motor
        vibration.wRightMotorSpeed = right_motor
        self.api.XInputSetState(0, ctypes.byref(vibration))

    def is_button_press(self, button):
        self.get_state()
        if int(self.config['gamepad']['XINPUT_GAMEPAD_' + button], base=16) & self.gamepad.wButtons:
            return True
        if 'TRIGGER' in button:
            return self.is_trigger_pressed(button)
        return False

    def is_thumb_move(self, thumb):
        position = abs(getattr(self.gamepad, self.axes_mapping[thumb]))
        if '-' in thumb:
            position = -position # wwdwdwwdwwdwddwdwdwdwdwdwdwdddwdwdw
        if position > self.get_thumbs_dead_zone():
            return True
        return False

    def is_trigger_pressed(self, trigger):
        if self.get_trigger_value(trigger) > self.get_triggers_dead_zone():
            return True
        return False

    def get_trigger_value(self, trigger):
        return getattr(self.gamepad, self.axes_mapping[trigger]) & self.config['general'].getint('TRIGGERS_MAGNITUDE')

    def get_axis_value(self, item):
        return getattr(self.gamepad, self.axes_mapping[item])

    def get_normalised_thumb_value(self, value):
        return (float(value) / int(self.config['general']['THUMBS_MAGNITUDE'])) * float(
            self.config['general']['SENSITIVITY'])

    # TODO: change API: take triger as argument (merge with get_trigger_value)
    def get_normalised_trigger_value(self, value):
        return (float(value & 0xff) / int(self.config['general']['TRIGGERS_MAGNITUDE'])) * 10 * float(
            self.config['general']['SENSITIVITY'])

    def get_thumbs_dead_zone(self):
        return float(self.config['general']['THUMBS_DEAD_ZONE']) * int(self.config['general']['THUMBS_MAGNITUDE'])

    def get_triggers_dead_zone(self):
        return float(self.config['general']['TRIGGERS_DEAD_ZONE']) * int(self.config['general']['TRIGGERS_MAGNITUDE'])

    def get_state(self):
        self.api.XInputGetState(ctypes.wintypes.WORD(0), ctypes.pointer(self.state))

