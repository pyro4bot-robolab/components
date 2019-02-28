#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ____________developed by paco andres____________________
# _________collaboration with cristian vazquez____________
# All data defined in json configuration are attributes in your code object
import time
from node.libs import control
import Pyro4
from node.libs.gpio.GPIO import *


@Pyro4.expose
class alphal298n(control.Control):
    """Control L298N (Alphabot) through GPIO."""

    __REQUIRED = ["IN1", "IN2", "IN3", "IN4", "ENA", "ENB", "gpioservice"]

    def __init__(self):
        self.GPIO = GPIOCLS(self.gpioservice, self.pyro4id)
        self.GPIO.setup([self.IN1, self.IN2, self.IN3,
                         self.IN4, self.ENA, self.ENB], OUT)
        self.motor_a = self.GPIO.PWM(self.ENA, 500)
        self.motor_b = self.GPIO.PWM(self.ENB, 500)
        self.motor_a.start(20)
        self.motor_b.start(50)
        self.stop()

    @control.flask("actuator")
    def forward(self, DCA=100, DCB=100):
        self.motor_a.ChangeDutyCycle(DCA)
        self.motor_b.ChangeDutyCycle(DCB)
        self.GPIO.output(self.IN1, HIGH)
        self.GPIO.output(self.IN2, LOW)
        self.GPIO.output(self.IN3, LOW)
        self.GPIO.output(self.IN4, HIGH)

    @control.flask("actuator")
    def stop(self):
        self.motor_a.ChangeDutyCycle(0)
        self.motor_b.ChangeDutyCycle(0)
        self.GPIO.output(self.IN1, LOW)
        self.GPIO.output(self.IN2, LOW)
        self.GPIO.output(self.IN3, LOW)
        self.GPIO.output(self.IN4, LOW)

    @control.flask("actuator")
    def backward(self, DCA=100, DCB=100):
        self.motor_a.ChangeDutyCycle(DCA)
        self.motor_b.ChangeDutyCycle(DCB)
        self.GPIO.output(self.IN1, LOW)
        self.GPIO.output(self.IN2, HIGH)
        self.GPIO.output(self.IN3, HIGH)
        self.GPIO.output(self.IN4, LOW)

    @control.flask("actuator")
    def set_vel(self, DCA, DCB, forwardA=True, forwardB=True):
        if DCA > 100:
            DCA = 100
        elif DCA < 0:
            DCA = 0
        if DCB > 100:
            DCB = 100
        elif DCB < 0:
            DCB = 0
        self.motor_a.ChangeDutyCycle(DCA)
        self.motor_b.ChangeDutyCycle(DCB)
        if forwardA:
            self.GPIO.output(self.IN1, HIGH)
            self.GPIO.output(self.IN2, LOW)
        else:
            self.GPIO.output(self.IN1, LOW)
            self.GPIO.output(self.IN2, HIGH)

        if forwardB:
            self.GPIO.output(self.IN3, LOW)
            self.GPIO.output(self.IN4, HIGH)
        else:
            self.GPIO.output(self.IN3, HIGH)
            self.GPIO.output(self.IN4, LOW)

    @control.flask("actuator")
    def left(self, DC=100):
        self.set_vel(0, DC)

    @control.flask("actuator")
    def right(self, DC=100):
        self.set_vel(DC, 0)
