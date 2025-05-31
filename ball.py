import random
import math

class Ball:
  def __init__(self):
    self.x = float(210)
    self.y = float(370)
    self.direction_x = random.randrange(400)
    self.direction_y = random.randrange(380)
