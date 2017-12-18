#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lock().acquire()
#____________developed by paco andres____________________
# All datas defined in json configuration are atributes in you code object
import time
from node.libs import control
import Pyro4

"""
JSON_DOCUMENTATION
{SENSOR_NAME} : laser
{c} cls : laser
{d} --> : ["arduino"]
{m} LASER : [0,0,0]
{m} frec : 0.02
{m} worker_run : true
{m} enable : true
END_JSON_DOCUMENTATION
"""

@Pyro4.expose
class laser (control.Control):
    @control.load_config
    def __init__(self, data, **kwargs):
        self.send_subscripcion(self.arduino, "LASER")

        # this line is the last line in constructor method
        super(laser, self).__init__(self.worker)

    def worker(self):
        while self.worker_run:
            time.sleep(self.frec)

    def get_laser(self):
        return self.LASER


if __name__ == "__main__":
    pass
