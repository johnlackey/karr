# Simple two DC motor car class.  Exposes a simple LOGO turtle-like API for
# moving a car forward, backward, and turning.  See CarTest.py for an
# example of using this class.
# Author: Tony DiCola
# License: MIT License https://opensource.org/licenses/MIT
import array
import atexit
import time
import RPi.GPIO as GPIO
#import statistics

from Adafruit_MotorHAT import Adafruit_MotorHAT


class Car(object):
    def __init__(self, addr=0x60, drive_id=2, steer_id=1, drive_trim=0, steer_trim=0,
                 stop_at_exit=True):
        """Create an instance of the car.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - drive_id: The ID of the drive motor, default is 1.
         - steer_id: The ID of the steer motor, default is 2.
         - drive_trim: Amount to offset the speed of the drive motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - steer_trim: Amount to offset the speed of the steer motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and drive, steer motor.
        self._mh = Adafruit_MotorHAT(addr)
        self._drive = self._mh.getMotor(drive_id)
        self._steer = self._mh.getMotor(steer_id)
        self._drive_trim = drive_trim
        self._steer_trim = steer_trim
        # Start with motors turned off.
        self._drive.run(Adafruit_MotorHAT.RELEASE)
        self._steer.run(Adafruit_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)
	# setup ultrasonic sensor
        self.TRIG = [11, 15, 18]
        self.ECHO = [12, 16, 22]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.TRIG[0], GPIO.OUT)
        GPIO.setup(self.ECHO[0], GPIO.IN)
        GPIO.setup(self.TRIG[1], GPIO.OUT)
        GPIO.setup(self.ECHO[1], GPIO.IN)
        GPIO.setup(self.TRIG[2], GPIO.OUT)
        GPIO.setup(self.ECHO[2], GPIO.IN)
        #
        #https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-25-ultrasonic-ranging-module-sensor-kit-v2-0-for-b-plus.html


    def _drive_speed(self, speed):
        """Set the speed of the drive motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._drive_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._drive.setSpeed(speed)

    def _steer_speed(self, speed):
        """Set the speed of the steer motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._steer_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._steer.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._drive.run(Adafruit_MotorHAT.RELEASE)
        self._steer.run(Adafruit_MotorHAT.RELEASE)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the car will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._drive_speed(speed)
        #self._steer_speed(speed)
        self._drive.run(Adafruit_MotorHAT.FORWARD)
        #self._steer.run(Adafruit_MotorHAT.RELEASE)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the car will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._drive_speed(speed)
        #self._steer_speed(speed)
        self._drive.run(Adafruit_MotorHAT.BACKWARD)
        #self._steer.run(Adafruit_MotorHAT.RELEASE)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def straight(self):
        self._steer.run(Adafruit_MotorHAT.RELEASE)

    def right(self, speed, seconds=None):
        """Drive to the right at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the car will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        #self._drive_speed(speed)
        self._steer_speed(255)
        self._steer.run(Adafruit_MotorHAT.FORWARD)
        #self._drive.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def left(self, speed, seconds=None):
        """Drive to the left at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the car will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        #self._drive_speed(speed)
        self._steer_speed(255)
        self._steer.run(Adafruit_MotorHAT.BACKWARD)
        #self._drive.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def raw_distance(self, sensor = 0):
        if GPIO.input(self.ECHO[sensor]):
            return(100)
        distance = 0
        GPIO.output(self.TRIG[sensor], 0)
        time.sleep(0.05)
        GPIO.output(self.TRIG[sensor], 1)
        dummy_variable = 0
        dummy_variable = 0
        #time.sleep(0.00001)
        GPIO.output(self.TRIG[sensor], 0)
        time1, time2 = time.time(), time.time()
        while GPIO.input(self.ECHO[sensor]) == 0:
            a = 0
            time1 = time.time()
            if time1 - time2 > 0.02:
                distance = 100
                break
        if distance == 100:
            return (distance)
        while GPIO.input(self.ECHO[sensor]) == 1:
            a = 1
            time2 = time.time()
            if time2 - time1 > 0.02:
                distance = 500
                break
        if distance == 500:
            return(distance)
        during = time2 - time1
        distance_value = during / 0.00000295 / 2 / 10
        #print( "Raw Distance: %d" % distance_value )
        return distance_value

    def distance(self, sensor = 0):
	#sum = 0.0
	list = []
	for i in range(1):
            #sum += self.raw_distance(sensor)
            value = 100
            while value == 100:
                value = self.raw_distance(sensor)
	    if value != 500:
                list.append(value)
        list.sort()
	#print( "Length of list: %d" % len(list) )
        if len(list) > 0:
            index = len(list) // 2
            #print( "Index: %d" % index )
            print( "Distance%d: %d" % (sensor, list[len(list)//2]) )
            return list[index]
        return 9999
        #return sum / 10

    def destroy():
        GPIO.cleanup()

