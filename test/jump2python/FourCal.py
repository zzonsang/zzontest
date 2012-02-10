'''
Created on 2012. 1. 24.

@author: kobe
'''

class FourCal:
    def setdata(self, a, b):
        self.a = a 
        self.b = b 
        
    def sum(self):
        result = self.a + self.b
        return result
    
    def mul(self): 
        return self.a * self.b
    
    def sub(self):
        return self.a - self.b
    
    def div(self):
        return self.a / self.b
    