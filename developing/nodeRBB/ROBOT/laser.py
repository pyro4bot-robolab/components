#!/usr/bin/env python
# -*- coding: utf-8 -*-
#lock().acquire()
#____________developed by paco andres____________________
#All datas defined in json configuration are atributes in you code object
import time
from nodeRBB.LIBS import control
import Pyro4

@Pyro4.expose
class laser (control.control):
    @control.loadconfig

    def __init__(self,data,**kwargs):
        self.send_subscripcion(self.arduino,"LASER")

        #this line is the last line in constructor method
        super(laser,self).__init__(self.worker)
    def worker(self):
        while self.worker_run:
            time.sleep(self.frec)

    def get_laser(self):
        return self.LASER


if __name__ == "__main__":
    pass