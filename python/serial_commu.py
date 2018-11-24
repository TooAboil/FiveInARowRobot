import serial
import time
import numpy as np


class ComData:

    def __init__(self, flag, cord, serialPort, baudRate):
        self.cord = cord  # 用数组存储坐标
        self.flag = flag  # 表示状态为接收中(1(接收完成)\2(运动完成))或是发送中(0) 0-1-2-0
        self.serialPort = serialPort  # 串口
        self.baudRate = baudRate  # 波特率
        self.ser = serial.Serial(self.serialPort, self.baudRate, timeout=0.5)
        self.signal = ''

    def send(self):
        # 用于串口通讯发送数据
        if self.flag == 0:
            # content = str(self.cord[0]) + '-' + str(self.cord[1]) + '\n'  # 以角度1-角度二字符串形式传输
            accessory = [1000, 100, 10, 1]
            for i in [0, 1]:
                if self.cord[i] >= 0:
                    self.ser.write('0'.encode())
                else:
                    self.ser.write('1'.encode())
                    self.cord[i] = abs(self.cord[i])
                num = np.zeros(4, dtype=np.int)
                for digit in range(4):  # 将坐标从高位到低位写为xx.xx格式发送
                    remnant = np.sum(np.multiply(num, accessory))
                    num[digit] = int((int(self.cord[i] * 100) - remnant) / accessory[digit])  # 取出当前位并存储
                    self.ser.write(str(num[digit]).encode())  # 发送数据
                    # self.ser.write(str(self.cord[0]).encode())
            # self.ser.write(str(self.cord[1]).encode())
            self.flag = 1

        else:
            print("error in status flag during sending")

    def receive(self):
        time_start = time.time()
        # 用于串口通讯接收数据
        if self.flag == 0:
            print("error in status flag during receiving")

        while self.flag == 1:
            message = self.ser.readline()
            message = message.decode()
            if message:
                if message == 'B':  # 判断是否接收到正确回执
                    self.signal = message
                    self.flag = 2

            time_cost = time.time() - time_start
            if time_cost > 5:  # 判断是否超时，若超时，重新发送坐标信息
                self.flag = 0
                self.send()
                time_start = time.time()

        while self.flag == 2:
            message = self.ser.readline()
            message = message.decode()
            if message:
                if message == 'C':  # 判断是否接收到运动完成回执
                    self.signal = message
                    self.flag = 0

    def close_ser(self):
        # 用于关闭串口
        self.ser.close()


def main():
    data = ComData(0, [26.46, -57.27], 'COM3', 9600)
    data.send()
    data.receive()
    print(data.signal)


if __name__ == '__main__':
    main()