# 0-2000  10  10  thresholds 30%    max - min (global)
# diff = max - min
# perc = (element - min) / diff    loop    10次投票
import numpy as np

MaxL, MinL, MaxR, MinR = float('-inf'), float('inf'), float('-inf'), float('inf')
threshold = 0.3

for k in range(100):
    Left = np.random.randint(0, 2000, 10)  
    Right = np.random.randint(0, 2000, 10) 
    MaxL = max(np.max(Left), MaxL)
    MinL = min(np.min(Left), MinL)
    MaxR = max(np.max(Right), MaxR)
    MinR = min(np.min(Right), MinR)
    diffL = MaxL - MinL
    diffR = MaxR - MinR
    countL, countR = 0, 0

    for i in range(10):
        if (Left[i] - MinL) / diffL > threshold:
            countL += 1 
        elif (Left[i] - MinL) / diffL < threshold:
            countL -= 1 
        if (Right[i] - MinR) / diffR > threshold:
            countR += 1
        elif (Right[i] - MinR) / diffR < threshold:
            countR -= 1
    if countL > 0 and countR > 0:
        action = "Forward"
    elif countL < 0 and countR < 0:
        action = "Backward"
    elif countL > 0 and countR < 0:
        action = "Turn Left"
    elif countL < 0 and countR > 0:
        action = "Turn Right"
    elif countL == 0 and countR != 0:
        action = "Turn Right" if countR > 0 else "Turn Left"
    elif countR == 0 and countL != 0:
        action = "Turn Left" if countL > 0 else "Turn Right"
    else:
        action = "Stop"

    print(action)
