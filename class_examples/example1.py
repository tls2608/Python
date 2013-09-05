# Class as a data container
# Example is point in 2D space (x,y)

from math import sqrt

class Point(): # () is for if you want to inheret from another class
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
# __ means its a special method a class knows how to deal with
# p1 will be defined to self
# self.x is the attribute of x (p1.x = 1.0)

    def norm(self):
        return sqrt(self.x**2 + self.y**2)
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
        
# a1+a2 is the same as a1.__add__(a2) 
# have to have special method __add__ defined for instances p1 and p2
        
    def __repr__(self):
        print 'Point(%f %f)' % (self.x, self.y) # %5.3f
   
    def __str__(self):
        return '(%f %f)' % (self.x, self.y) # %5.3f
        
p1 = Point(1.0, 3.0)
p2 = Point(3.0, 4.0)

print 'p1 = ', p1.x, p1.y
print 'p2 = ', p2.x, p2.y

print 'p1.norm() = ', p1.norm()
print 'p2.norm() = ', p2.norm()

print 'p1 + p2 = ', p1 + p2

p3 = p1 + p2