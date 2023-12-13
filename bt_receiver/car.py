import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


ENA = 27  # 13  # L298 Enable A
ENB = 22  # 15  # L298 Enable B
IN1 = 6  # 31  # Input 1
IN2 = 13  # 33  # Input 2
IN3 = 19  # 35  # Input 3
IN4 = 26  # 37  # Input 4

PWM_FREQUENCY = 30
FORWARD_DC = 100
TURNING_DC = 55
# Initialize motor A
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
ENA_pwm = GPIO.PWM(ENA, PWM_FREQUENCY)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(TURNING_DC)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

# Initialize motor B
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
ENB_pwm = GPIO.PWM(ENB, PWM_FREQUENCY)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(TURNING_DC)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)


def Motor_Forward(forward_ratio):
    
    ENA_pwm.ChangeDutyCycle(forward_ratio)
    ENB_pwm.ChangeDutyCycle(forward_ratio)
    # print("motor forward")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


def Motor_Backward():
    # print("motor_backward")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


def Motor_TurnRight():
    ENA_pwm.ChangeDutyCycle(TURNING_DC)
    ENB_pwm.ChangeDutyCycle(TURNING_DC)
    # print("motor_turnright")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


def Motor_TurnLeft():
    ENA_pwm.ChangeDutyCycle(TURNING_DC)
    ENB_pwm.ChangeDutyCycle(TURNING_DC)
    # print("motor_turnleft")
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


def Motor_Stop():
    # print("motor_stop")
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)
