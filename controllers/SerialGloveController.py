import serial
import serial.tools.list_ports
import utils


class SerialGloveController:
    def __init__(self):
        self.initial_x = 50
        self.arduino = None

        # TODO: calibrate these values with a button
        self.min_x = 5
        self.max_x = 60

        self.x = self.initial_x

        self.init_arduino()

    def init_arduino(self):
        ports = serial.tools.list_ports.comports()
        USB_ports = [i for i in ports if "usbserial" in i.usb_description()]

        # TODO: check to see if we need to iterate through all the ports
        if USB_ports:
            self.arduino = serial.Serial(port=USB_ports[0].device, baudrate=115200, timeout=0.1)

    def is_active(self):
        return bool(self.arduino)

    def reset(self):
        self.x = self.initial_x

    def update(self):
        data = self.arduino.readline()
        if not data:
            return
        data = float(data)
        self.x = utils.map_val(self.min_x, self.max_x, 0, 100, data)

    def get_x(self):
        """range: [0, 100]"""
        self.update()
        return self.x
