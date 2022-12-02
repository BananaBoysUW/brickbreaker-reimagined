import serial
import serial.tools.list_ports
import utils
import paddle_pb2


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
        USB_ports = [i for i in ports if "usbserial" in i.device]

        # TODO: check to see if we need to iterate through all the ports
        if USB_ports:
            self.arduino = serial.Serial(port=USB_ports[0].device, baudrate=115200, timeout=0.1)
            self.arduino.timeout = 0.05
            self.arduino.read_all()  # clear the serial buffer

    def display_serial(self):
        while True:
            if not self.arduino.readable():
                continue
            data = self.arduino.readline()
            if not data or not data.strip():
                continue
            self.arduino.read_all()  # Clears the serial buffer (IMPORTANT!)
            print(data)
            # time.sleep(0.5)

    def is_active(self):
        return bool(self.arduino)

    def reset(self):
        self.x = self.initial_x

    def update(self):
        # Do not block if the serial buffer is empty
        if self.arduino.in_waiting == 0:
            return

        if not self.arduino.readable():
            return

        data = self.arduino.readline()
        if not data or not data.strip():
            return

        data = data[:-1]  # strip newline character

        # Attempt to serialize the received data
        paddleOut = paddle_pb2.PaddleOut()
        try:
            data = bytearray.fromhex(data.decode())
            paddleOut.ParseFromString(bytes(data))
        except Exception as e:
            print(e)
            return

        data = paddleOut.distance
        data = utils.map_val(self.min_x, self.max_x, 0, 100, data)

        if abs(self.x - data) > 30:
            print(abs(data - self.x))
            return

        self.x = data

    def vibrate(self):
        paddleIn = paddle_pb2.PaddleIn()
        paddleIn.buzz.durationMillis = 110
        paddleIn.buzz.motors.extend([1, 2, 3, 4])

        data = paddleIn.SerializeToString()

        data = data.hex().encode()
        self.arduino.write(data)
        self.arduino.write('\n'.encode())

    def get_x(self):
        """range: [0, 100]"""
        self.update()
        return self.x


if __name__ == "__main__":
    SerialGloveController().display_serial()
