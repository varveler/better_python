## Dependency Inversion is a key principle to write code you can reuse more easly
## its part of the SOLID desging principles, represents the "D" it states according
## to Robert C. Martins:

## 1. High-level modules should not depend on low-level modules.
##    Both should depend on abstractions.

## 2. Abstractions should not depend on details. Details should depend on abstractions.


## (a module could be a function, a class, a file... a piece of code.)

## in order to do this we need a mecanism to separate
## description/definition from the actual implementation (abstraction)
## source: https://stackoverflow.com/questions/61358683/dependency-inversion-in-python
## source: https://youtu.be/Kv5jhbSkqLE
################################################################################
## BEFORE CODE

## In this example there is aclear dependancy between the classes
class LightBulb:
    def turn_on(self):
        print("LightBulb: turned on...")

    def turn_off(self):
        print("LightBulb: turned off...")


class ElectricPowerSwitch:

    def __init__(self, l: LightBulb):
        self.lightBulb = l
        self.on = False

    def press(self):
        if self.on:
            self.lightBulb.turn_off()
            self.on = False
        else:
            self.lightBulb.turn_on()
            self.on = True


## the dependency bewteewn classes because one needs the other to press on and off the lightbulb
l = LightBulb()
switch = ElectricPowerSwitch(l)
switch.press()
switch.press()
## it works but what if we wanted to create a Fan object, we would need to write
## a class named ElectricPowerSwitchFan or maybe put an if else statement on the
## init method wich would make code mesy

################################################################################
## AFTER CODE

from abc import ABC, abstractmethod

## Abstarct Base Class --> ABC
class Switchable(ABC):
    ## this class is like an intermidiary for switchables objects and the object itself
    ## By implementing this interface we make sure that every Switchable will have
    ## a turn on and turn of methods, otherwise will trhou an error when sublcassing
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class LightBulb(Switchable):
    def turn_on(self):
        print("LightBulb: turned on...")

    def turn_off(self):
        print("LightBulb: turned off...")


class ElectricPowerSwitch:

    def __init__(self, c: Switchable):
        self.client = c
        self.on = False

    def press(self):
        if self.on:
            self.client.turn_off()
            self.on = False
        else:
            self.client.turn_on()
            self.on = True

#s = Switchable() ## wont allow it becasue you cannot create instances of abstract classes
l = LightBulb()
switch = ElectricPowerSwitch(l)
switch.press()
switch.press()

## if we create a second object that is also switchable we can reuse code:

class Fan(Switchable):
    def turn_on(self):
        print("Fan: start spining now...")

    def turn_off(self):
        print("Fan: stoping spinning...")


f = Fan()
switch = ElectricPowerSwitch(f)
switch.press()
switch.press()
switch.press()
switch.press()
