#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Created on 2012. 1. 30.

@author: kobe
'''
from jump2python.HousePark import HousePark

class HouseKim(HousePark):
    lastname = '김'

def main():
    pef = HouseKim('Taesoo')
    pef.travel('test')

if __name__ == '__main__':
    main()
