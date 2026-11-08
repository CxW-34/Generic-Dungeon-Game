# Generic Dungeon Game - Player Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 08/11/2026

# Imports
import pyxel as px

class Player:
  def __init__(self) -> Player:
    self.location = [72, 72]
    self.face = 'South'
    self.health = 8

  def takeDamage(self, damage) -> None: #Fpr taking damage (to be used by enemy class)
    self.health = max(0, self.health - damage)

  def heal(self) -> None: #For healing the player
    self.health = min(8, self.health + 5)

  def move(self) -> None: #Gets player input and moves player
    if px.btn(px.KEY_SPACE):
      return

    speed = 1.2

    if px.btn(px.KEY_UP) and not px.btn(px.KEY_DOWN):
      self.location[1] += speed
    elif px.btn(px.KEY_DOWN) and not px.btn(px.KEY_UP):
      self.location[1] -= speed
    if px.btn(px.KEY_RIGHT) and not px.btn(px.KEY_LEFT):
      self.location[0] += speed
    elif px.btn(px.KEY_LEFT) and not px.btn(px.KEY_RIGHT):
      self.location[0] -= speed

  def update(self) -> None:
    self.move()

  def draw(self, SCREENHEIGHT) -> None:
    locX = SCREENHEIGHT*7/9 + self.location[0]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2
    locY = SCREENHEIGHT     - self.location[1]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2
    img = 0
    w = 16
    h = 16
    scale = SCREENHEIGHT/9/16
    
    px.blt(locX, locY, img, 0, 48, w, h, px.COLOR_BLACK, scale=scale)
