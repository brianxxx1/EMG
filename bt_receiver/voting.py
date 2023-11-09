# 0-2000  10  10  thresholds 30%    max - min (global)
# diff = max - min
# perc = (element - min) / diff    loop    25次投票
import numpy as np
from car_controller import car
def fill(LeftBuffer, LeftInput, RightBuffer, RightInput):
    LeftBuffer.append(LeftInput)
    RightBuffer.append(RightInput)

def vote(Left, Right):
    MaxL, MinL, MaxR, MinR = float('-inf'), float('inf'), float('-inf'), float('inf')
    threshold = 0.3

    MaxL = max(np.max(Left), MaxL)
    MinL = min(np.min(Left), MinL)
    MaxR = max(np.max(Right), MaxR)
    MinR = min(np.min(Right), MinR)
    diffL = MaxL - MinL
    diffR = MaxR - MinR
    countL, countR = 0, 0

    for i in range(25):
        if (Left[i] - MinL) / diffL > threshold:
            countL += 1 
        elif (Left[i] - MinL) / diffL < threshold:
            countL -= 1 
        if (Right[i] - MinR) / diffR > threshold:
            countR += 1
        elif (Right[i] - MinR) / diffR < threshold:
            countR -= 1
    if countL > 0 and countR > 0:
        action = 'Forward'
        car.Motor_Forward()
    elif countL > 0 and countR < 0:
        action = 'Left'
        car.Motor_TurnLeft()
    elif countL < 0 and countR > 0:
        action = 'Right'
        car.Motor_TurnRight()
    else:
        action = 'Stop'
        car.Motor_Stop()


    print(action)
