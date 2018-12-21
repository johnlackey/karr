from gpiozero import DistanceSensor
import time

sensor = [
    DistanceSensor(18, 17),
    DistanceSensor(23, 22),
    DistanceSensor(25, 24)
]

for i in range(3):
    time.sleep(1)
    value = sensor[i-1].distance
    print(value)

