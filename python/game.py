import numpy as np
import random


class Chess:

    def __init__(self):
        self.boardA = np.zeros((10, 10))  # 老人的棋盘
        self.boardB = np.zeros((10, 10))  # 电脑的棋盘
        self.boardC = np.zeros((10, 10))  # 总的棋盘
        self.abstractA = []  # 抽取出的老人棋盘
        self.abstractB = []  # 抽取出的电脑棋盘
        self.abstractC = []  # 抽取出的总棋盘
        self.flag = 0  # 棋局的状态，0为未出现输赢，-1为机器人赢，1为老人赢
        self.coord = [0, 0]  # 返回的落子坐标位置
        self.flag2 = 0

    def abstract(self):
        self.abstractA = extract(self.boardA)
        self.abstractB = extract(self.boardB)
        self.abstractC = extract(self.boardC)

    def move(self, coordination):
        self.boardA[coordination[0]][coordination[1]] = 1
        self.boardC[coordination[0]][coordination[1]] = 1

    def delete(self, coordination):
        self.boardA[coordination[0]][coordination[1]] = 0
        self.boardC[coordination[0]][coordination[1]] = 0

    def win(self):
        # 用于判断输赢

        # 老人赢？
        for i in range(42):
            occupied = 0
            for j in range(10):
                if self.abstractA[i][j] == 1:
                    occupied = occupied + 1
                    if occupied == 5:
                        self.flag = 1  # 老人赢
                        break
                else:
                    occupied = 0
            if self.flag == 1:
                break  # 跳过之后所有循环语音宣告老人赢
        # 机器赢？
        for i in range(42):
            occupied = 0
            for j in range(10):
                if self.abstractB[i][j] == 1:
                    occupied = occupied + 1
                    if occupied == 5:
                        self.flag = -1  # 老人输
                        break
                else:
                    occupied = 0
            if self.flag == -1:
                break  # 跳过之后所有循环语音宣告老人输

    def process(self):
        # 用于输出落子位置坐标
        if not self.flag2:
            self.coord = [random.randint(3, 6), random.randint(3, 6)]
        else:
            result_list = self.prior()
            # for p in range(8):
            #     # 遍历优先级
            #     for result in result_list:
            #         if result.priority != p:
            #             continue
            #         else:
            #             if fringe(self, result):
            #                 result.unavailable()
            #             else:
            #                 self.coord = result.coordination
            dic = {}
            for result in result_list:
                fringe(self, result)
                index = result.coordination_10[0] * 10 + result.coordination_10[1]
                if index not in dic.keys():
                    dic[index] = result.priority
                else:
                    dic[index] += result.priority
            coord_index = max(dic, key=lambda x: dic[x])
            self.coord[0] = int(coord_index / 10)
            self.coord[1] = int(coord_index % 10)
        self.flag2 = 1
        self.boardB[self.coord[0]][self.coord[1]] = 1
        self.boardC[self.coord[0]][self.coord[1]] = 1

    def prior(self):
        # 用于判断优先级，最后返回可行解的列表
        result_list = []
        # 己方（B棋盘）连子情况判断与优先级设定
        for i in range(42):
            occupied = 0
            for j in range(10):
                if self.abstractB[i][j] == 1:
                    occupied = occupied + 1
                    if j < 9:
                        if self.abstractB[i][j + 1] == 0:
                            if occupied == 4:  # 己方有四连子
                                if j == 3:  # 左侧是边，只检测右侧(第五位)
                                    if self.abstractC[i][4] == 0:  # 右侧空
                                        result_list.append(Result(1, [i, 4]))
                                        # print("#1己方四连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 4] == 0):
                                    if self.abstractC[i][j + 1] == 0:
                                        result_list.append(Result(1, [i, j + 1]))
                                    else:
                                        result_list.append(Result(1, [i, j - 4]))
                                    # print("# 己方四连单或双空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                            # 以上三情况均不满足，则此四连子两侧非空，不做处理

                            elif occupied == 3:  # 己方有三连子
                                if j == 2:  # 左侧是边，只可能单空
                                    if self.abstractC[i][3] == 0:  # 右侧空
                                        if self.abstractB[i][4] == 1:
                                            result_list.append(Result(1, [i, 3]))
                                            # print("#|o|o|o|_|o|，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                        # print("#1己方三连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为5")
                                        result_list.append(Result(5, [i, 3]))
                                elif (self.abstractC[i][j + 1] == 0) and (self.abstractC[i][j - 3] == 0):
                                    if ((j + 2) <= 9) or ((j - 4) >= 0):
                                        if (j + 2) <= 9 and self.abstractB[i][j + 2] == 1:  # 右侧不是边且有己方棋子
                                            result_list.append(Result(1, [i, j+1]))
                                            # print("#  |_|o|o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                        elif (j - 4) >= 0 and self.abstractB[i][j - 4] == 1:  # 左侧不是边且有己方棋子
                                            result_list.append(Result(1, [i, j - 3]))
                                            # print("#  |o|_|o|o|o|_|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                    # print("# 己方三连双空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                    result_list.append(Result(3, [i, j + 1]))
                                    result_list.append(Result(3, [i, j - 3]))
                                elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 3] == 0):
                                    if ((j + 2) <= 9) or ((j - 4) >= 0):
                                        if (j + 2) <= 9 and self.abstractB[i][j + 2] == 1:  # 右侧不是边且有己方棋子
                                            result_list.append(Result(1, [i, j+1]))
                                            # print("#  |o|o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                        elif ((j - 4) >= 0) and self.abstractB[i][j - 4] == 1:  # 左侧不是边且有己方棋子
                                            result_list.append(Result(1, [i, j-3]))
                                            # print("#  |o|_|o|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                    if self.abstractC[i][j + 1] == 0:
                                        result_list.append(Result(5, [i, j+1]))
                                    if self.abstractC[i][j - 3] == 0:
                                        result_list.append(Result(5, [i, j-3]))
                                    # print("#2己方三连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为5")
                            # 以上四情况均不满足，则此三连子两侧非空，不做处理

                            elif occupied == 2:  # 己方有两连子 ！若以下if语句任一满足则不执行跳过之后同缩进的if！
                                if j == 1:  # 左侧是边，只可能单空
                                    if self.abstractC[i][2] == 0:  # 右侧空
                                        if (self.abstractB[i][3] == 1) and (self.abstractB[i][4] == 0):
                                            result_list.append(Result(3, [i, j+1]))
                                            # print("#1  |o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                        elif (self.abstractB[i][3] == 1) and (self.abstractB[i][4] == 1):
                                            result_list.append(Result(1, [i, j+1]))
                                            # print("#1  |o|o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                        result_list.append(Result(7, [i, j+1]))
                                        # print("#1己方两连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                                elif (self.abstractC[i][j + 1] == 0) and (self.abstractC[i][j - 2] == 0):
                                    if j + 2 <= 9:
                                        if self.abstractB[i][j + 2] == 1:
                                            if (j + 3) <= 9:  # 往右三个都是格
                                                if self.abstractB[i][j + 3] == 0:  # 右第三格不是边缘但没有己方棋子
                                                    result_list.append(Result(3, [i, j+1]))
                                                    # print("#1  |_|o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                                elif self.abstractB[i][j + 3] == 1:  # 右第三格不是边缘且有己方棋子
                                                    result_list.append(Result(1, [i, j+1]))
                                                    # print("#1  |_|o|o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                            else:  # 最右侧是边缘
                                                result_list.append(Result(3, [i, j+1]))
                                                # print("#1  |_|o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                    if j - 3 >= 0:
                                        if self.abstractB[i][j - 3] == 1:
                                            if (j - 4) >= 0:  # 往左三个都是格
                                                if (self.abstractB[i][j - 4] == 0) & (self.abstractC[i][j - 3] == 0):  # 左第三格不是边缘但没有己方棋子
                                                    result_list.append(Result(3, [i, j-2]))
                                                    # print("#1  |o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                                elif (self.abstractB[i][j - 4] == 1) & (self.abstractC[i][j - 3] == 0):  # 左第三格不是边缘且有己方棋子
                                                    result_list.append(Result(1, [i, j-2]))
                                                    # print("#1  |o|o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                            else:  # 往左三格是边缘
                                                result_list.append(Result(3, [i, j-2]))
                                                # print("#1  |o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                    result_list.append(Result(6, [i, j+1]))
                                    result_list.append(Result(6, [i, j - 2]))
                                    # print("# 己方两连双空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为6")
                                elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 2] == 0):
                                    if j + 2 <= 9:
                                        if self.abstractB[i][j + 2] == 1:
                                            if (j + 3) <= 9:  # 往右三个都是格
                                                if self.abstractB[i][j + 3] == 0:  # 右第三格不是边缘但没有己方棋子
                                                    result_list.append(Result(3, [i, j+1]))
                                                    # print("#1  |o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                                elif self.abstractB[i][j + 3] == 1:  # 右第三格不是边缘且有己方棋子
                                                    result_list.append(Result(1, [i, j+1]))
                                                    # print("#1  |o|o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                            else:  # 最右侧是边缘
                                                result_list.append(Result(3, [i, j+1]))
                                                # print("#1  |o|o|_|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                    if j - 3 >= 0:
                                        if self.abstractB[i][j - 3] == 1:
                                            if j - 4 >= 0:  # 往左三个都是格
                                                if self.abstractB[i][j - 4] == 0:  # 左第三格不是边缘但没有己方棋子
                                                    result_list.append(Result(3, [i, j-2]))
                                                    # print("#1  |o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                                elif self.abstractB[i][j - 4] == 1:  # 左第三格不是边缘且有己方棋子
                                                    result_list.append(Result(1, [i, j-2]))
                                                    # print("#1  |o|o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                            else:  # 往左三格是边缘
                                                result_list.append(Result(3, [i, j-2]))
                                                # print("#1  |o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                    if self.abstractC[i][j + 1] == 0:
                                        result_list.append(Result(7, [i, j+1]))
                                    if self.abstractC[i][j -2] == 0:
                                        result_list.append(Result(7, [i, j - 2]))
                                    # print("#2己方两连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                            # 以上四情况均不满足，则此两连子两侧非空，不做处理

                            elif occupied == 1:  # 己方单子
                                if j == 0:  # 左侧是边，只可能单空
                                    if self.abstractC[i][1] == 0:  # 右侧空
                                        if self.abstractB[i][2] == 1 and self.abstractC[i][2] == 0:
                                            result_list.append(Result(7, [i, j+1]))
                                            # print("# |o|_|o|_|，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                                        result_list.append(Result(9, [i, j+1]))
                                        # print("#1己方单子单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为9")
                                elif (self.abstractC[i][j + 1] == 0) and (self.abstractC[i][j - 1] == 0):
                                    result_list.append(Result(8, [i, j+1]))
                                    result_list.append(Result(8, [i, j - 1]))
                                    # print("# 己方单子双空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为8")
                                elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 1] == 0):
                                    if (j + 2) <= 9:
                                        if (self.abstractC[i][j + 1] == 0) and (self.abstractB[i][j + 2] == 1):
                                            result_list.append(Result(7, [i, j+1]))
                                            # print("# |o|_|o|，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                                    if (j - 2) >= 0:
                                        if (self.abstractC[i][j - 1] == 0) and (self.abstractB[i][j - 2] == 1):
                                            result_list.append(Result(7, [i, j-2]))
                                            # print("# |o|_|o|，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                                    if self.abstractC[i][j + 1] == 0:
                                        result_list.append(Result(9, [i, j + 1]))
                                    if self.abstractC[i][j - 1] == 0:
                                        result_list.append(Result(9, [i, j-1]))
                                    # print("#2己方单子单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为9")
                            # 以上四情况均不满足，则此两连子两侧非空，不做处理
                    else:
                        if self.abstractC[i][8] == 0:  # 左侧空
                            if self.abstractB[i][7] == 1:
                                result_list.append(Result(7, [i, j-1]))
                                # print("# |o|_|o|，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                            result_list.append(Result(9, [i, j-1]))
                            # print("#3己方单子单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为9")
                        elif self.abstractC[i][7] == 0:  # 左侧空
                            if (self.abstractB[i][6] == 1) and (self.abstractB[i][5] == 0):
                                result_list.append(Result(3, [i, j-2]))
                                # print("#1  |o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                            elif (self.abstractB[i][6] == 1) and (self.abstractB[i][5] == 1):
                                result_list.append(Result(1, [i, j-2]))
                                # print("#1  |o|o|_|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                            result_list.append(Result(7, [i, j-2]))
                            # print("#3己方两连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为7")
                        elif self.abstractC[i][6] == 0:  # 左侧空
                            if self.abstractB[i][5] == 1:
                                result_list.append(Result(1, [i, 6]))
                                # print("#  |o|_|o|o|o|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                            result_list.append(Result(5, [i, j-3]))
                            # print("#3己方三连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为5")
                        elif self.abstractC[i][5] == 0:  # 左侧空
                            result_list.append(Result(1, [i, j-4]))
                            # print("#2己方四连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")

                else:
                    occupied = 0

        # 对方（A棋盘）连子情况判断与优先级设定
        for i in range(42):
            occupied = 0
            for j in range(10):
                if self.abstractA[i][j] == 1:
                    occupied = occupied + 1
                    if j < 9:
                        if self.abstractA[i][j + 1] == 0:
                            if occupied == 4:  # 对方有四连子 ！若以下if语句任一满足则不执行跳过之后同缩进的if！
                                if j == 3:  # 左侧是边，只检测右侧(第五位)
                                    if self.abstractC[i][4] == 0:  # 右侧空
                                        result_list.append(Result(2, [i, j+1]))
                                        # print("# 对方四连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 4] == 0):
                                    if self.abstractC[i][j + 1] == 0:
                                        result_list.append(Result(2, [i, j+1]))
                                    if self.abstractC[i][j - 4] == 0:
                                        result_list.append(Result(2, [i, j-4]))
                                    # print("# 对方四连单或双空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                            # 以上两情况均不满足，不做处理

                            elif occupied == 3:  # 对方有三连子
                                if j == 2:  # 左侧是边，只可能单空
                                    if self.abstractC[i][3] == 0:  # 右侧空
                                        if self.abstractA[i][4] == 1:
                                            result_list.append(Result(2, [i, j+1]))
                                            # print("#|*|*|*|_|*|，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                        # print("#不收入表D")
                                elif (self.abstractC[i][j + 1] == 0) and (self.abstractC[i][j - 3] == 0):
                                    if (j + 2 <= 9) or (j - 4 >= 0):
                                        if (self.abstractA[i][j + 2] == 1) and (j + 2 <= 9):  # 右侧不是边且有对方棋子
                                            result_list.append(Result(2, [i, j+1]))
                                            # print("#  |_|*|*|*|_|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                        elif (self.abstractA[i][j - 4] == 1) and ((j - 4) >= 0):  # 左侧不是边且有对方棋子
                                            result_list.append(Result(2, [i, j-4]))
                                            # print("#  |*|_|*|*|*|_|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                        result_list.append(Result(4, [i, j+1]))
                                        result_list.append(Result(4, [i, j - 4]))
                                        # print("# 对方三连双空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为4")
                                elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 3] == 0):  # 三连单空
                                    if ((j + 2) <= 9) or ((j - 4) >= 0):
                                        if (self.abstractA[i][j + 2] == 1) and (j + 2 <= 9):  # 右侧不是边且有对方棋子
                                            result_list.append(Result(2, [i, j+1]))
                                            # print("#  |*|*|*|_|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                        elif (self.abstractA[i][j - 4] == 1) and ((j - 4) >= 0):  # 左侧不是边且有对方棋子
                                            result_list.append(Result(2, [i, j-4]))
                                            # print("#  |*|_|*|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                            # 对方三连子其他情况不做处理

                            elif occupied == 2:  # 对方有两连子
                                if j == 1:  # 左侧是边，只可能单空
                                    if self.abstractC[i][2] == 0:  # 右侧空
                                        if (self.abstractA[i][3] == 1) and (self.abstractA[i][4] == 1):
                                            result_list.append(Result(2, [i, j+1]))
                                            # print("#1  |*|*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                elif (self.abstractC[i][j + 1] == 0) and (self.abstractC[i][j - 2] == 0):
                                    if j + 2 <= 9:
                                        if self.abstractA[i][j + 2] == 1:
                                            if (j + 3) <= 9:  # 往右三个都是格
                                                if self.abstractA[i][j + 3] == 0:  # 右第三格不是边缘但没有棋子
                                                    if self.abstractC[i][j + 3] == 0:  # 右第三格为空格
                                                        result_list.append(Result(4, [i, j+1]))
                                                        # print("#1  |_|*|*|_|*|_|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为4")
                                                elif self.abstractA[i][j + 3] == 1:  # 右第三格不是边缘且有棋子
                                                    result_list.append(Result(2, [i, j+1]))
                                                    # print("#1  |_|*|*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                                            # else:  # 最右侧是边缘
                                                # print("#1  |_|*|*|_|*||  ，不处理")
                                    if j - 3 >= 0:
                                        if self.abstractA[i][j - 3] == 1:
                                            if (j - 4) >= 0:  # 往左三个都是格
                                                if self.abstractA[i][j - 4] == 0:  # 左第三格不是边缘但没有棋子
                                                    result_list.append(Result(2, [i, j-4]))
                                                    # print("#1  |_|*|_|*|*|_|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为4")
                                                elif self.abstractA[i][j - 4] == 1:  # 左第三格不是边缘且有己方棋子
                                                    result_list.append(Result(1, [i, j-4]))
                                                    # print("#1  |*|*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                            # else:  # 往左三格是边缘
                                            #     print("#1  |*|_|*|*|_|  ，不处理")
                                    # print("# 不处理")
                                        elif (self.abstractC[i][j + 1] == 0) or (self.abstractC[i][j - 2] == 0):
                                            if j + 2 <= 9:
                                                if self.abstractA[i][j + 2] == 1:
                                                    if (j + 3) <= 9:  # 往右三个都是格
                                                        if self.abstractA[i][j + 3] == 0:  # 右第三格不是边缘但没有对方棋子
                                                            result_list.append(Result(4, [i, j + 1]))
                                                            # print("#1  |*|*|_|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                                        elif self.abstractA[i][j + 3] == 1:  # 右第三格不是边缘且有对方棋子
                                                            result_list.append(Result(2, [i, j + 1]))
                                                            # print("#1  |*|*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                                    else:  # 最右侧是边缘
                                                        result_list.append(Result(4, [i, j + 1]))
                                                        # print("#1  |*|*|_|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                            if j - 3 >= 0:
                                                if self.abstractA[i][j - 3] == 1:
                                                    if j - 4 >= 0:  # 往左三个都是格
                                                        if self.abstractA[i][j - 4] == 0:  # 左第三格不是边缘但没有对方棋子
                                                            result_list.append(Result(4, [i, j - 2]))
                                                            # print("#1  |*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                                        elif self.abstractA[i][j - 4] == 1:  # 左第三格不是边缘且有对方棋子
                                                            result_list.append(Result(2, [i, j - 2]))
                                                            # print("#1  |*|*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为1")
                                                    else:  # 往左三格是边缘
                                                        result_list.append(Result(4, [i, j - 2]))
                                                        # print("#1  |*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为3")
                                    # 以上四情况均不满足，则此两连子两侧非空，不做处理# 以上四情况均不满足，则此两连子两侧非空，不做处理
                    else:
                        if self.abstractC[i][5] == 0:  # 左侧空
                            result_list.append(Result(2, [i, j]))
                            # print("# 对方四连单空，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                        elif (self.abstractC[i][6] == 0) and (self.abstractA[i][5] == 1):
                            result_list.append(Result(2, [i, j]))
                            # print("# |*|_|*|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                        elif ((self.abstractC[i][7] == 0) and (self.abstractA[i][6] == 1) and (
                                self.abstractA[i][6] == 1)):
                            result_list.append(Result(2, [i, j]))
                            # print("# |*|*|_|*|*|  ，计算并记录（i，j）对应的棋盘坐标放入表D，设置优先级为2")
                else:
                    occupied = 0

        return result_list


class Result:
    def __init__(self, priority, coordination):
        self.priority = 10 - priority  # 优先级
        self.coordination_10 = reflect(coordination)  # 10*10棋盘上结果坐标
        self.coordination_42 = reflect(coordination)  # 42*10棋盘上结果坐标
        if priority == 8 | priority == 6:
            self.status = 0  # 攻棋或守棋，0为守棋
        else:
            self.status = 1

    def unavailable(self):
        # 用于降低优先级，不会被搜索到
        self.priority = 0


def fringe(chess, result):
    # 用于边缘检测，返回0表示该结果为堵死，不可行
    if result.status == 0:
        broad = chess.abstractB
    else:
        broad = chess.abstractA
    # 将棋盘边缘设置为-1，便于计算
    broad = nullify(broad)
    broad = np.insert(broad, 0, values=-1, axis=1)
    broad = np.insert(broad, 11, values=-1, axis=1)
    # 期望落子位置所在的行、列、斜线上已经有电脑落子的情况
    l = 0  # 期望位置离左边最近电脑棋子/边缘格数
    r = 0  # 期望位置离右边最近电脑棋子/边缘格数
    lineL = np.int8(broad[result.coordination_10[0], ::-1])
    lineR = np.int8(broad[result.coordination_10[0], :])
    for i in lineL[(12-result.coordination_10[1]):]:
        if i == -1 | i == 1:
            break
        l = l + 1
    for i in lineR[result.coordination_10[1]:]:
        if i == -1 | i == 1:
            break
        r = r + 1
    if l+r < 4:
        result.unavailable()


def nullify(broad):
    # 输入抽出的42*10矩阵，将其中无效的格点置为-1
    for i in range(21, 42):
        for j in range(10):
            c = reflect([i, j])
            if c[0] < 0 | c[1] < 0:
                broad[i, j] = -1
    return broad


def reflect(c):
    # 输入42*10变换后矩阵的坐标，映射原10*10棋盘坐标
    if (c[0] >= 0) & (c[0] <= 9):
        return c
    elif (c[0] >= 10) & (c[0] <= 19):
        return [c[1], c[0]-10]
    elif (c[0] >= 20) & (c[0] <= 25):
        return [c[0]-20, c[1]]
    elif (c[0] >= 26) & (c[0] <= 30):
        return [c[1], c[0]-25]
    elif (c[0] >= 31) & (c[0] <= 36):
        return [c[0]-27-c[1], c[1]]
    else:
        return [9-c[1], c[0]-36+c[1]]


def extract(broad):
    # 取出所有可行线（滤后棋盘矩阵）
    m = -1
    filtrated = np.zeros((42, 10))  # 定义a的大小
    # 取行
    for i in range(10):
        m = m + 1
        filtrated[m] = broad[i]  # m = 9

    # 取列
    n = 0  # 纵坐标标志
    for j in range(10):
        m = m + 1
        for i in range(10):
            filtrated[m][n + i] = broad[i][j]  # m= 19

    # 取主对角线
    # 先取左下角六根,从0，0那条取到5，0那条
    # n=0#a的纵坐标
    for j in range(6):
        m = m + 1
        i = j
        for i in range(i, 10):
            filtrated[m][i - j] = broad[i][i - j]  # m= 25

        # 取右上角5根,从0，1那条取到0，5那条
    for j in range(1, 6):
        m = m + 1
        i = j
        for i in range(i, 10):
            filtrated[m][i - j] = broad[i - j][i]  # m= 30

    # 取次对角线
    # 先取左上角6根，从4，0取到9，0
    for j in range(4, 10):
        m = m + 1
        for i in range(j + 1):
            filtrated[m][n + i] = broad[j - i][i]  # m= 36

    # 取右下角5根，从9，1取到9，5
    for j in range(1, 6):
        m = m + 1
        for i in range(10 - j):  # 在0到9-j变化
            filtrated[m][n + i] = broad[9 - i][j + i]  # m= 41

    return filtrated


