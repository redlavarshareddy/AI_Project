import random
import sys
import copy
import time


class Team32():

    def __init__(self):
        self.MaxDepth = 3
        self.Util_Matrix = [[0, -1, -10, -100, -1000], [1, 0, 0, 100, 0], [
            10, 0, 0, 0, 0], [100, 0, 0, 0, 0], [1000, 0, 0, 0, 0]]
        self.waysH = [[[0, 0], [0, 1], [0, 2], [0, 3]],
                    [[1, 0], [1, 1], [1, 2], [1, 3]],
                    [[2, 0], [2, 1], [2, 2], [2, 3]],
                    [[3, 0], [3, 1], [3, 2], [3, 3]]
                    ]
        self.waysV = [[[0, 0], [1, 0], [2, 0], [3, 0]],
                    [[0, 1], [1, 1], [2, 1], [3, 1]],
                    [[0, 2], [1, 2], [2, 2], [3, 2]],
                    [[0, 3], [1, 3], [2, 3], [3, 3]]
                    ]
        self.cnto = self.num = self.cntp = 0
        self.ourFlag = None
        pass

    def MinMax(self, board, old_move, node_type_maxnode, player_sign, opponent_sign, depth, alpha, beta, best_row, best_coloumn, itr_max_depth, st_time):
        curr_time = time.time()
        if curr_time - st_time > 14.7:
            utility = 0
            ret_tup = (utility, best_row, best_coloumn)
            return ret_tup

        if depth == itr_max_depth:
            utility = self.utility_get(board, player_sign, opponent_sign)
            return (utility, best_row, best_coloumn)

        elif depth != itr_max_depth:
            available_moves = board.find_valid_move_cells(old_move)

            if not len(available_moves):
                utility = self.utility_get(board, player_sign, opponent_sign)
                ret_tup = (utility, best_row, best_coloumn)
                return ret_tup

            if not depth:
                if len(available_moves) > 17:
                    self.MaxDepth = min(self.MaxDepth, 2)

            for move in available_moves:
                temp_board = copy.deepcopy(board)

                sign = player_sign
                if not node_type_maxnode:
                	sign = opponent_sign

                temp_board.update(old_move, move, sign)

                if node_type_maxnode:
                    node_type_maxnode1 = False
                elif not node_type_maxnode:
                    node_type_maxnode1 = True

                utility = self.MinMax(
                    temp_board, move, node_type_maxnode1, player_sign, opponent_sign,
                                      depth + 1, alpha, beta, best_row, best_coloumn, itr_max_depth, st_time)  # agains call MinMax

                if node_type_maxnode:
                    if utility[0] > alpha:
                        alpha = utility[0]
                        best_row = move[0]
                        best_coloumn = move[1]
                elif not node_type_maxnode:
                    if utility[0] < beta:
                        beta = utility[0]
                        best_row = move[0]
                        best_coloumn = move[1]

                if not (alpha <= beta):
                    break;

                if (time.time() - st_time) > 14:
                    return (utility, best_row, best_coloumn)
            if node_type_maxnode:
                return (alpha, best_row, best_coloumn)
            elif not node_type_maxnode:
                return (beta, best_row, best_coloumn)

    def move(self, board, old_move, player_flag):
        if old_move == (-1, -1):
            return (4, 4)
        startt = time.time()
        if player_flag != 'x':
            flag2 = 'x'
        elif player_flag == 'x':
            flag2 = 'o'
        self.num = self.num + 1
        max_MaxDepth = 4
        self.cntp = sum(blocks.count(player_flag)
                        for blocks in board.block_status)
        self.cnto = sum(blocks.count(flag2) for blocks in board.block_status)

        self.ourFlag = player_flag
        temp_board = copy.deepcopy(board)
        temp_block = copy.deepcopy(board.block_status)

        elapsed = (time.time() - startt)
        temp_move = (0, 0, 0)
        itr_max_depth = 2
        while(elapsed < 14):
            next_move = temp_move
            temp_move = self.MinMax(
                temp_board, old_move, True, player_flag, flag2, 0, -
                    100000000000000.0, 10000000000000.0, -1,
                                     -1, itr_max_depth, startt)
            itr_max_depth = itr_max_depth + 1
            curr_time = time.time()
            elapsed = curr_time - startt
        ret_tup = next_move[1], next_move[2]
        return ret_tup

    def utility_get(self, board, playerFlag, opFlag):
        utility_values_block = [0 for j in range(16)]
        for i in range(16):
            utility_values_block[i] = self.calc_utility(board, i, playerFlag)
        gain = 0
        lim = 1000.0
        for i in range(16):
            utility_values_block[i] = utility_values_block[i] / lim

        # DIAMOND1
        p = negative = positive = 0

        p = p + utility_values_block[4]
        if board.block_status[1][0] == playerFlag:
            positive = positive + 1
        elif board.block_status[1][0] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[1]
        if board.block_status[0][1] == playerFlag:
            positive = positive + 1
        elif board.block_status[0][1] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[9]
        if board.block_status[2][1] == playerFlag:
            positive = positive + 1
        elif board.block_status[2][1] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[6]
        if board.block_status[1][2] == playerFlag:
            positive = positive + 1
        elif board.block_status[1][2] == opFlag:
            negative = negative + 1

        gain = self.get_factor(p, gain)
        gain = self.calculate(positive, negative, gain, 1)

        p = negative = positive = 0
        # DIAMOND2

        p = p + utility_values_block[5]
        if board.block_status[1][1] == playerFlag:
            positive = positive + 1
        elif board.block_status[1][1] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[2]
        if board.block_status[0][2] == playerFlag:
            positive = positive + 1
        elif board.block_status[0][2] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[10]
        if board.block_status[2][2] == playerFlag:
            positive = positive + 1
        elif board.block_status[2][2] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[7]
        if board.block_status[1][3] == playerFlag:
            positive = positive + 1
        elif board.block_status[1][3] == opFlag:
            negative = negative + 1

        gain = self.get_factor(p, gain)
        gain = self.calculate(positive, negative, gain, 1)

        # DIAMOND3
        p = negative = positive = 0

        p = p + utility_values_block[8]
        if board.block_status[2][0] == playerFlag:
            positive = positive + 1
        elif board.block_status[2][0] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[5]
        if board.block_status[1][1] == playerFlag:
            positive = positive + 1
        elif board.block_status[1][1] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[13]
        if board.block_status[3][1] == playerFlag:
            positive = positive + 1
        elif board.block_status[3][1] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[10]
        if board.block_status[2][2] == playerFlag:
            positive = positive + 1
        elif board.block_status[2][2] == opFlag:
            negative = negative + 1

        gain = self.get_factor(p, gain)
        gain = self.calculate(positive, negative, gain, 1)

        # DIAMOND4
        p = positive = negative = 0

        p = p + utility_values_block[9]
        if board.block_status[2][1] == playerFlag:
            positive = positive + 1
        elif board.block_status[2][1] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[6]
        if board.block_status[1][2] == playerFlag:
            positive = positive + 1
        elif board.block_status[1][2] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[14]
        if board.block_status[3][2] == playerFlag:
            positive = positive + 1
        elif board.block_status[3][2] == opFlag:
            negative = negative + 1

        p = p + utility_values_block[11]
        if board.block_status[2][3] == playerFlag:
            positive = positive + 1
        elif board.block_status[2][3] == opFlag:
            negative = negative + 1

        gain = self.get_factor(p, gain)
        gain = self.calculate(positive, negative, gain, 1)

        for i in range(4):
            p = positive = negative = 0
            for j in range(4):
                p = p + utility_values_block[j * 4 + i]
                if board.block_status[j][i] == playerFlag:
                    positive = positive + 1
                elif board.block_status[j][i] == opFlag:
                    negative = negative + 1
            gain = self.get_factor(p, gain)
            gain = self.calculate(positive, negative, gain, 1)

        for j in range(4):
            p = 0
            positive = 0
            negative = 0
            for i in range(4):
                p = p + utility_values_block[j * 4 + i]
                if board.block_status[j][i] == playerFlag:
                    positive = positive + 1
                elif board.block_status[j][i] == opFlag:
                    negative = negative + 1
            gain = self.get_factor(p, gain)
            gain = self.calculate(positive, negative, gain, 1)

        cnt1 = sum(blocks.count(playerFlag) for blocks in board.block_status)
        cnt2 = sum(blocks.count(opFlag) for blocks in board.block_status)
        if self.cntp < cnt1 and cnt2 == self.cnto:
            gain = gain + 50
        elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
            gain = gain - 20
        elif cnt1 < self.cntp and cnt2 > self.cnto:
            gain = gain - 50
        # print "Gain Returned by Get utility is: ", gain
        return gain

    def calc_utility(self, board, boardno, playerFlag):
        gain = 0
        startx = boardno / 4
        starty = boardno % 4
        starty = starty * 4
        startx = startx * 4

        for i in range(startx, startx + 4):
            positive = negative = neutral = 0
            for j in range(starty, starty + 4):
                if board.board_status[i][j] == '-':
                    neutral = neutral + 1
                elif board.board_status[i][j] == playerFlag:
                    positive = positive + 1
                else:
                    negative = negative + 1
            gain = self.calculate(positive, negative, gain, 0)

        for j in range(starty, starty + 4):
            positive = negative = neutral = 0
            for i in range(startx, startx + 4):
                if board.board_status[i][j] == '-':
                    neutral = neutral + 1
                elif board.board_status[i][j] == playerFlag:
                    positive = positive + 1
                else:
                    negative = negative + 1
            gain = self.calculate(positive, negative, gain, 0)

        # DIAMOND1
        positive = neutral = negative = 0

        if board.board_status[startx + 1][starty + 0] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 1][starty + 0] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 0][starty + 1] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 0][starty + 1] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 2][starty + 1] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 2][starty + 1] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 1][starty + 2] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 1][starty + 2] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        gain = self.calculate(positive, negative, gain, 0)

        # DIAMOND2
        positive = neutral = negative = 0

        if board.board_status[startx + 1][starty + 1] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 1][starty + 1] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 0][starty + 2] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 0][starty + 2] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 2][starty + 2] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 2][starty + 2] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 1][starty + 3] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 1][starty + 3] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        gain = self.calculate(positive, negative, gain, 0)

        # DIAMOND3
        positive = neutral = negative = 0

        if board.board_status[startx + 2][starty + 0] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 2][starty + 0] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 1][starty + 1] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 1][starty + 1] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 3][starty + 1] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 3][starty + 1] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 2][starty + 2] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 2][starty + 2] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        gain = self.calculate(positive, negative, gain, 0)

        # DIAMOND4
        positive = neutral = negative = 0

        if board.board_status[startx + 2][starty + 1] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 2][starty + 1] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 1][starty + 2] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 1][starty + 2] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 3][starty + 2] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 3][starty + 2] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        if board.board_status[startx + 2][starty + 3] == playerFlag:
            positive = positive + 1
        elif board.board_status[startx + 2][starty + 3] == '-':
            neutral = neutral + 1
        else:
            negative = negative + 1

        gain = self.calculate(positive, negative, gain, 0)

        pf = playerFlag
        if playerFlag != 'o':
            of = 'o'
        elif playerFlag == 'o':
            of = 'x'
        i = j = tempy = tempx = 0
        for lineh in self.waysH:
            for linev in self.waysV:
                cntph = cntoh = cntov = cntpv = 0
                for point in lineh:
                    tempx = point[0]
                    if board.board_status[startx + point[0]][starty + point[1]] == pf:
                        cntph = cntph + 1
                    elif board.board_status[startx + point[0]][starty + point[1]] == of:
                        cntoh = cntoh + 1

                for point in linev:
                    tempy = point[1]
                    if board.board_status[startx + point[0]][starty + point[1]] == pf:
                        cntpv = cntpv + 1
                    elif board.board_status[startx + point[0]][starty + point[1]] == of:
                        cntov = cntov + 1

                if not cntov and not cntph:
                	temp_x = tempx + startx
                    temp_y = tempy + starty
                    if cntoh==2 and cntpv==3 and board.board_status[temp_x][temp_y]==pf:
                        gain = gain + 10

                if not cntpv and not cntoh:
                	temp_x = tempx + startx
                	temp_y = tempy + starty
                    if cntph==3 and cntov==2 and board.board_status[temp_x][temp_y] == pf:
                        gain = gain + 10
        return gain

    def calculate(self, positive, negative, gain, flag_m):
        if flag_m==0:
            gain += self.Util_Matrix[positive][negative]
        else:
            gain += 10 * self.Util_Matrix[positive][negative]

        return gain


    def get_factor1(self, p_gain, gain):

        if p_gain < 1 and p_gain >= -1:
            gain =gain + p_gain

        if p_gain >= 3 and p_gain < 4:
            val = 100
            val =val + (p_gain - 3) * 900
            gain =gain +  val

        if p_gain >= -2 and p_gain < -1:
            val = -1
            val =val - (abs(p_gain) - 1) * 9
            gain =gain +  val

        if p_gain < -3 and p_gain >=-4:
            val = -100
            val =val - (abs(p_gain) - 3) * 900
            gain = gain + val

        if p_gain >= 1 and p_gain < 2:
            val = 1
            val = val + (p_gain - 1) * 9
            gain =gain +  val

        if p_gain >= 4:
            val = 1000
            val = val + (p_gain - 4) * 9000
            gain =gain + val
        if p_gain >= 2 and p_gain < 3:
            val = 10
            val = val + (p_gain - 2) * 90
            gain = gain + val


        if p_gain < -4:
            val = -1000
            val -= (abs(p_gain) - 4) * 9000
            gain =gain + val
        if p_gain >= -3 and p_gain < -2:
            val = -10
            val =val - (abs(p_gain) - 2) * 90
            gain =gain + val
        return gain

    def get_factor(self, util, gain):
        limit1, limit2 = 4, -4
        for i in range(-4,-1):
            if (util >= i and util < i+1):
            	power = abs(i)-2
                factr = pow(10, power)
                ret = (util-i-1)*9*factr - factr

        for i in range(1,4):
            if (util >= i and util < i+1):
            	power = abs(i)-1
                factr = pow(10, power)
                temp = (util-i)*9*factr
                ret = temp + factr

        if abs(util) < 1 or util == -1:
            ret = util

        if util < limit2:
            factr = pow(10,3)
            temp = (util-limit2)*9*factr
            ret = temp - factr

        if util >= limit1:
            factr = pow(10,3)
            temp = (util-limit1)*9*factr
            ret = temp + factr

        return ret + gain
