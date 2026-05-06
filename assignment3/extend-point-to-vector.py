#Task 5
import math

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def distance(self, other):
    return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
  
class Vector(Point):
  def __str__(self):
    return f"Vector<{self.x}, {self.y}>"  
  def __add__(self, other):
    new_x = self.x + other.x
    new_y = self.y + other.y
    return Vector(new_x, new_y)
  
if __name__ == "__main__":
  p1 = Point(3, 4)
  p2 = Point(3, 4)
  p3 = Point(0, 0)

  print("--- Point Demonstration ---")
  print(f"p1: {p1}")
  print(f"p1 == p2: {p1 == p2}")  
  print(f"p1 == p3: {p1 == p3}")  
  print(f"Distance from p1 to p3: {p1.distance(p3)}")

  print("\n--- Vector Demonstration ---")
  v1 = Vector(5, 10)
  v2 = Vector(1, 2)

  print(f"v1: {v1}") 
  print(f"v1 Distance to origin: {v1.distance(p3)}")

  v3 = v1 + v2
  print(f"v1 + v2 = {v3}")
  print(f"Is result a Vector? {isinstance(v3, Vector)}")
