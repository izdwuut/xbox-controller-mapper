import ctypes
from input import KeyboardInput, Inputs, Input


class Keyboard:
    api = SendInput = ctypes.windll.user32

    KEYEVENTF_SCANCODE = 0x008
    SCAN_CODES = {
        'ESCAPE': 0x01,
        '1': 0x02,
        '2': 0x03,
        '3': 0x04,
        '4': 0x05,
        '5': 0x06,
        '6': 0x07,
        '7': 0x08,
        '8': 0x09,
        '9': 0x0A,
        '0': 0x0B,
        '-': 0x0C,
        '=': 0x0D,
        'BACKSPACE': 0x0E,
        'TAB': 0x0F,
        'Q': 0x10,
        'W': 0x11,
        'E': 0x12,
        'R': 0x13,
        'T': 0x14,
        'Y': 0x15,
        'U': 0x16,
        'I': 0x17,
        'O': 0x18,
        'P': 0x19,
        '<': 0x1A,
        '>': 0x1B,
        'ENTER': 0x1C,
        'CONTROL': 0x1D,
        'A': 0x1E,
        'S': 0x1F,
        'D': 0x20,
        'F': 0x21,
        'G': 0x22,
        'H': 0x23,
        'J': 0x24,
        'K': 0x25,
        'L': 0x26,
        ';': 0x27,
        "'": 0x28,
        '`': 0x29,
        'SHIFT': 0x2A,
        '\\': 0x2B,
        'Z': 0x2C,
        'X': 0x2D,
        'C': 0x2E,
        'V': 0x2F,
        'B': 0x30,
        'N': 0x31,
        'M': 0x32,
        ',': 0x33,
        '.': 0x34,
        '/': 0x35,
        'LEFT_ALT': 0x38,
        'SPACE': 0x39,
        'F1': 0x3B,
        'F2': 0x3C,
        'F3': 0x3D,
        'F4': 0x3E,
        'F5': 0x3F,
        'F6': 0x40,
        'F7': 0x41,
        'F8': 0x42,
        'F9': 0x43,
        'F10': 0x44,
        'F11': 0x57,
        'F12': 0x58,
        'UP': 0xC8,
        'LEFT': 0xCB,
        'RIGHT': 0xCD,
        'DOWN': 0xD0,
        'PGUP': 0xC9,
        'END': 0xCF,
        'PGDN': 0xD1,
        'INSERT': 0xD2,
        'DELETE': 0xD3,
        'HOME': 0xC7,
        'RIGHT_ALT': 0xB8,
        'WINDOWS': 0xDB
    }

    @classmethod
    def key_down(cls, key):
        if key.upper() not in cls.SCAN_CODES:
            raise Exception('Invalid key')
        inputs = Inputs()
        inputs.ki = KeyboardInput(0, cls.SCAN_CODES[key.upper()], cls.KEYEVENTF_SCANCODE, 0, ctypes.pointer(ctypes.c_ulong(0)))
        input_ = Input(ctypes.c_ulong(1), inputs)
        cls.api.SendInput(1, ctypes.pointer(input_), ctypes.sizeof(input_))

    @classmethod
    def key_up(cls, key):
        if key.upper() not in cls.SCAN_CODES:
            raise Exception('Invalid key')
        inputs = Inputs()
        inputs.ki = KeyboardInput(0, cls.SCAN_CODES[key.upper()], cls.KEYEVENTF_SCANCODE | 0x0002, 0, ctypes.pointer(ctypes.c_ulong(0)))
        input_ = Input(ctypes.c_ulong(1), inputs)
        cls.api.SendInput(1, ctypes.pointer(input_), ctypes.sizeof(input_))