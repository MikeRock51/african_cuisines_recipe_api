#!/usr/bin/env python3

from enum import Enum


class Color(Enum):
    red = 1
    blue = 2
    green = 3

    def val(self):
        print(self.__members__.values())

if __name__ == "__main__":
    c = Color.red
    c.val()


'''def decorate(f):
    def wrapper():
        print("Bout to run up")
        f()
        print("Hope you're satisfied")

    return wrapper

@decorate
def sayMyName():
    print("Mike Rock")

sayMyName()'''
