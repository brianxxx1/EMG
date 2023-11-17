"""
This is the car control system. CarControllingAgent has a built-in voting system
that decides and control the car action.
"""

from enum import Enum

from car_controller import car


class MotorActions(Enum):
    STOP = "Motor_Stop"
    TURNRIGHT = "Motor_TurnRight"
    TURNLEFT = "Motor_TurnLeft"
    FORWARD = "Motor_Forward"


class CarControllingAgent:
    def __init__(self, voting_num=25, activate_threshold=0.3):
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
        self.activate_threshold = activate_threshold

    def reset_voting_buffer(self):
        self.voting_buffer_length = 0
        self.left_buffer = []
        self.right_buffer = []

    def fill_readings(self, left_reading, right_reading):
        self.left_max = max(left_reading, self.left_max)
        self.left_min = min(left_reading, self.left_min)
        self.right_max = max(right_reading, self.right_max)
        self.right_min = min(right_reading, self.right_min)

        self.left_buffer.append(left_reading)
        self.right_buffer.append(right_reading)
        self.voting_buffer_length += 1

    def vote(self):
        # not start a voting round due to insufficient number of votes
        if self.voting_buffer_length < self.voting_num:
            return

        # count votes
        left_diff = self.left_max - self.left_min
        right_diff = self.right_max - self.right_min
        left_count, right_count = 0, 0
        for i in range(self.voting_num):
            left_change_percent = (self.left_buffer[i] - self.left_min) / left_diff
            if left_change_percent >= self.activate_threshold:
                left_count += 1
            else:
                left_count -= 1
            right_change_percent = (self.right_buffer[i] - self.right_min) / right_diff
            if right_change_percent >= self.activate_threshold:
                right_count += 1
            else:
                right_count -= 1

        # decide voting result
        if left_count > 0 and right_count > 0:
            self.voting_result = MotorActions.FORWARD
        elif left_count > 0 and right_count < 0:
            self.voting_result = MotorActions.TURNLEFT
        elif left_count < 0 and right_count > 0:
            self.voting_result = MotorActions.TURNRIGHT
        else:
            self.voting_result = MotorActions.STOP

        # finish one round of voting, and reset voting buffer
        self.reset_voting_buffer()

    def refresh_car_action(self):
        """
        refresh car action based on the voting result, and send signal to control the car
        """
        if self.voting_result == MotorActions.FORWARD:
            print("forward")
            #car.Motor_Forward()
        elif self.voting_result == MotorActions.TURNLEFT:
            print("left")
            # car.Motor_TurnLeft()
        elif self.voting_result == MotorActions.TURNRIGHT:
            print("right")
            # car.Motor_TurnRight()
        else:
            print("back")
            # car.Motor_Stop()
        print(f"Voting result is {self.voting_result}")

    def stop_car(self):
        self.voting_result = MotorActions.STOP
        print("Stop")
        # car.Motor_Stop()
