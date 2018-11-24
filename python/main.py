import cv2
import time
import os
import pygame
from serial_commu import ComData
import ImgProcess as ip
from SolveAngle import chart_search
import game


def capture():
    # 用于从摄像头获取图像
    camera_capture = cv2.VideoCapture(1)  # 设定采集的摄像头
    camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)  # 设定采集像素
    ret, img = camera_capture.read()  # 读取
    while not(ret & img.any()):
        ret, img = camera_capture.read()  # 读取
    img = img[280:1000, 280:1000]
    return img


def inverse_kinetics(coordination):
    # 运动学反解模块
    return chart_search(coordination)


def communication(angles):
    # 数据传输串口通讯模块
    data = ComData(0, angles, 'COM3', 9600)
    data.send()
    data.receive()


def play(words):
    # 语音合成模块
    pygame.mixer.init()
    for name in words:
        file = os.getcwd() + '\\audition\\' + name + '.mp3'
        track = pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        time.sleep(1.5)
        pygame.mixer.music.stop()


def main():
    # 开始，先对棋盘图像进行处理,得到透视变换矩阵image.m
    img = capture()
    image = ip.ImgStatus(img)
    image.trans_matrix()
    image.transform()
    image.old = image.trans

    # 初始化棋局
    chess = game.Chess()

    # 语音播报“请开始”
    play(['start'])

    # 等待5s，检测是否落棋，并判断先后手
    flag_shadow = 1
    while flag_shadow == 1:  # 若遇到遮挡，等待5s后重新检测
        time.sleep(5)
        img = capture()
        image.now = img
        image.transform()
        image.shadow_recog()
        flag_shadow = image.shadow

        if image.shadow == 0:  # 老人为后手，不对棋局对象进行修改
            play(['defence', 'my_turn'])
        elif image.shadow == 2:  # 老人为先手，对棋局对象进行修改
            play(['attack', 'my_turn'])
            image.cord_recog()
            chess.move(image.centre)
        image.old = image.trans

    # 进入循环，计算机器落子位置 - 运动学反解 - 串口发送信息 - 语音播报 - 等待老人落棋 - 判断落棋位置 - 输入棋盘 - 计算
    while chess.flag == 0:  # 未出现输赢
        chess.abstract()
        chess.process()
        angles = inverse_kinetics(chess.coord)
        communication(angles)
        chess.abstract()
        chess.win()
        if chess.flag == -1:
            words = [str(chess.coord[0]+1), 'row', str(chess.coord[1]+1), 'column', 'lose']
            play(words)
            break

        image.shadow = 0
        img = capture()
        image.now = img
        image.transform()
        image.old = image.trans

        words = [str(chess.coord[0]+1), 'row', str(chess.coord[1]+1), 'column', 'your_turn']
        play(words)

        while image.shadow != 2:  # 若遇到遮挡或老人还未下棋，等待10s后重新检测
            time.sleep(5)
            img = capture()
            image.now = img
            image.transform()
            image.shadow_recog()
            if image.shadow == 2:  # 老人下了棋
                image.cord_recog()

        image.old = image.trans

        chess.move(image.centre)
        chess.abstract()
        chess.win()
        if chess.flag == 1:
            words = [str(chess.coord[0]+1), 'row', str(chess.coord[1]+1), 'column', 'win']
            play(words)

        play([str(image.centre[0]+1), 'row', str(image.centre[1]+1), 'column', 'my_turn'])
        my_input = input("input:")
        numbers = [0, 0]
        i = 0
        if my_input:
            for number in my_input.split(','):
                numbers[i] = number
                i = i+1
            chess.move(numbers)


if __name__ == '__main__':
    main()