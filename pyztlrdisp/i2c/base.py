import time
import smbus

class CharDispBase(object):

    data_addr_cmd = 0x00

    def __init__(self, chip_addr=0x3e, bus=1, booster=False, follower=False):
        self.bus = bus
        self.chip_addr = chip_addr
        self.i2c = smbus.SMBus(bus)

        init_cmd = []
        # Initialize command
        init_cmd.append(0x38)
        # Extend command
        init_cmd.append(0x39)
        init_cmd.append(0x14)
        init_cmd.append(0x73)
        bon = 0x56 if booster else 0x51
        init_cmd.append(bon)
        init_cmd.append(0x6c)
        init_cmd.append(0x38)

        self.command(self.data_addr_cmd, init_cmd)
        self.clear()

    def command(self, data_addr, data_list, sleep_sec=0.1):
        chip_addr = self.chip_addr
        i2c = self.i2c
        for data in data_list:
            i2c.write_byte_data(chip_addr, data_addr, data)
            time.sleep(sleep_sec)

    def clear(self):
        self.command(self.data_addr_cmd, [0x01])

    def return_home(self):
        self.command(self.data_addr_cmd, [0x02])

    def display_control(self, on=True, cursor=True, cursor_blink=False):
        code = 0x08 | on << 2 | cursor << 1 | cursor_blink
        self.command(self.data_addr_cmd, [code])

    def cursor_display_shift(self, sc=False, left_align=True):
        """

        Args:
            sc(bool): Default to False.
            left_align(bool): 文字を左揃えにするか右揃えにするか. Default to True.
        """
        code = 0x10 | sc << 3 | left_align << 2
        self.command(self.data_addr_cmd, [code])

    def function_set(self, data_length=True, display_line=True, font_type=True):
        code = 0x20 | data_length << 4 | display_line << 3 | font_type << 2
        self.command(self.data_addr_cmd, [code])

    def write(self, message):
        chip_addr = self.chip_addr
        i2c = self.i2c
        char_list = [ord(c) for c in message]
        i2c.write_i2c_block_data(chip_addr, 0x40, char_list)
        time.sleep(0.1)
