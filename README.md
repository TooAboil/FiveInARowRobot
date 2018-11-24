# FiveInARowRobot

机电自动化实践课程设计，利用四自由度机器人和工业相机搭建样机，为有眼疾的退休老大爷提供帮助。

A class assignment to build a robot for a retired man with eye illness by SCARA and industrial camera. 

据人口普查数据，中国老年人口数量庞大并逐年增加，有老龄化趋势，针对老年人口的科技产品开发有着良好前景。对互联网老人社区进行的爬虫与分析表明，身心健康是老人的需求。
本课题针对患眼疾的退休老人设计了一款基于四自由度机器人与工业相机的语音播报五子棋人机对弈机器人。该机器人能在10×10格棋盘上识别老人下棋位置，通过智能算法计算己方应下棋位置，使机械臂运动在棋盘下棋且播报该坐标，能判断并播报输赢。
为了实现功能，本文在可达空间内对机器人进行建模，运用查表法建立其运动关系，使用Canny算法、霍夫变换、透视变换进行相机标定，基于像素运算与开运算进行图像识别，建立五子棋优先级算法计算下棋位置，通过上位机与下位机的通讯驱动机械臂运动，利用pygame库实现语音合成。
对该机器人的测试表明其具有操作简单、位置识别与运动准确、对弈过程具有挑战性等优点。

According to the census, there's a tendency of aging in China as population over 60 is large and balloons still. Therefore, the technology aims at the old will have bright prospects. It's demonstrated that the retired consider physical and mental health as their necessity by crawling into a forum of retired people on the Internet and analysizing it's statistics.
The project builds a Five-In-A-Row(also known as Gobang or Gomoku) robot with voice function based on the SCARA and camera from Mind Vision, which is designed for retired people with eye illness and able to recognize the coordinations where the competitor place his stone in a 10 × 10 chessboard, choose the best position for its own stones to win the game with strategy and algorithm, move its arms to draw the stone at the specified position and inform the opponent of the coordinations by voice, and determine whether there's a winner.
To do these, we modeled the SCARA and connected points in its work space and angular displacement of its arms using table look-up scheme. Camera calibration is conducted by Canny Edge Detector, Hough Line Transform and Perspective Transformation and image recognition is based on pixel operation and morphology transformations as opening transformation. A new priority algorithm is constructed to decide where to place shones for a Five-In-A-Row game. Serial communication between host computer and slave computer is established to monitor the movement of the arms. The voice synthesis is built on pygame.
During the process of testing, the robot showed the property of amenity, accuracy in coordination recognizing and motion, and challenge.
