"""
This is the car control system. CarControllingAgent has a built-in voting system
that decides and control the car action.
"""
# import threading
# import time
from datetime import datetime
from enum import Enum
from statistics import median

import car
import numpy as np


class MotorActions(Enum):
    STOP = "Motor_Stop"
    TURNRIGHT = "Motor_TurnRight"
    TURNLEFT = "Motor_TurnLeft"
    FORWARD = "Motor_Forward"


class CarControllingAgent:
    def __init__(
        self,
        voting_num=5,
        activate_threshold_left=0.5,
        activate_threshold_right=0.3,
        left_range=255,
        right_rang=255,
    ):
        self.data = []

        # number of votes for one round of voting
        self.voting_num = voting_num
        self.left_buffer = []
        self.right_buffer = []
        self.voting_buffer_length = 0
        self.voting_result = MotorActions.STOP

        self.left_max = float("-inf")
        self.left_min = float("inf")
        self.right_max = float("inf")
        self.right_min = float("-inf")
        # EMG reading activate threshold, a percentage of muscle pressure
        # Muscle with EMG Reading beyond this threshold are considered as active.
        self.activate_threshold_left = activate_threshold_left
        self.activate_threshold_right = activate_threshold_right
        # activation range for car movements
        self.left_range = left_range
        self.right_range = right_rang

    def reset_voting_buffer(self):
        self.voting_buffer_length = 0
        self.left_buffer = []
        self.right_buffer = []

    def fill_readings(self, left_reading, right_reading):
        self.data.append([left_reading, right_reading])
        self.left_max = max(left_reading, self.left_max)
        self.left_min = min(left_reading, self.left_min)
        self.right_max = max(right_reading, self.right_max)
        self.right_min = min(right_reading, self.right_min)

        self.left_buffer.append(left_reading)
        self.right_buffer.append(right_reading)
        self.voting_buffer_length += 1

    def vote(self):
        if self.voting_buffer_length < self.voting_num:
            return

        left_count, right_count = 0, 0
        left_diff, right_diff = 0, 0
        l_c, r_c = 0, 0
        for i in range(self.voting_num):
            if self.left_buffer[i] >= self.activate_threshold_left:
                left_count += 1
                left_diff += self.left_buffer[i] - self.activate_threshold_left
                l_c += 1
            else:
                left_count -= 1

            if self.right_buffer[i] >= self.activate_threshold_right:
                right_count += 1
                right_diff += self.right_buffer[i] - self.activate_threshold_right
                r_c += 1
            else:
                right_count -= 1

        direction = self.decide_action(left_count, right_count)

        if direction == "FORWARD":
            left_diff_mean = left_diff / l_c
            right_diff_mean = right_diff / r_c

            left_ratio = left_diff_mean / self.left_range
            right_ratio = right_diff_mean / self.right_range

            forward_ratio = (left_ratio + right_ratio) / 2
            if forward_ratio >= 1:
                forward_ratio = 1
            self.refresh_car_action(forward_ratio)

        else:
            self.refresh_car_action()

        # print(self.left_buffer)
        # print(self.right_buffer)

        self.reset_voting_buffer()

    def decide_action(self, left_count, right_count):
        if left_count > 0 and right_count > 0:
            self.voting_result = MotorActions.FORWARD
            return "FORWARD"
        elif left_count > 0 and right_count < 0:
            self.voting_result = MotorActions.TURNLEFT
            return "TURNLEFT"
        elif left_count < 0 and right_count > 0:
            self.voting_result = MotorActions.TURNRIGHT
            return "TURNRIGHT"
        else:
            self.voting_result = MotorActions.STOP
            return "STOP"

    def refresh_car_action(self, forward_ratio=0):
        """
        refresh car action based on the voting result, and send signal to control the car
        """
        if self.voting_result == MotorActions.FORWARD:
            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            car.Motor_Forward(forward_ratio)
        elif self.voting_result == MotorActions.TURNLEFT:
            # print("<<<<<<<<<<<<<<-------------")
            car.Motor_TurnLeft()
        elif self.voting_result == MotorActions.TURNRIGHT:
            # print("--------------->>>>>>>>>>>>")
            car.Motor_TurnRight()
        else:
            # print("stop")
            car.Motor_Stop()

        # print(f"Voting result is {self.voting_result}")

    # def stop_car(self):
    #     self.voting_result = MotorActions.STOP
    #     print("Stop")
    #     # car.Motor_Stop()
