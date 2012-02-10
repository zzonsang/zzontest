#!/usr/bin/env python
# -*- coding: EUC-KR -*-
'''
Created on 2012. 1. 24.

@author: kobe
'''

class HousePark(object):
    lastname = 'Park 박'
    
    def __init__(self, name):
        self.fullname = self.lastname + name
    
    def travel(self, where):
        print "%s, %s travel." % (self.fullname, where) 

    def __del__(self):
        print "%s del" % self.fullname
        
    def __add__(self, other):
        print '%s + %s' % ( self.fullname, other.fullname)

    def __sub__(self, other):
        print '%s - %s' % ( self.fullname, other.fullname)
        
class HouseKim(HousePark):
    lastname = 'Kim'
    
    def travel(self, where, day):
        print '%s, %s여행 %d일 가네.' % (self.fullname, where, day)

def main():
    pef = HousePark('test')
    pef.travel('Pusan')

    print '=' * 50
    
    kim = HouseKim('taesoo2')
    kim.travel('Suwon', 5)

    print '+' * 50
    pef + kim
    
    print '-' * 50
    
    
if __name__ == "__main__":
    main()

    