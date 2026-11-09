# Generic Dungeon Game - Player Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 08/11/2026

# Imports
import pyxel as px

class Player:
  def __init__(self):
    self.location = [72.0, 72.0]
    self.face = 'South'
    self.health = 8

  def takeDamage(self, damage) -> None: #Fpr taking damage (to be used by enemy class)
    self.health = max(0, self.health - damage)

  def heal(self) -> None: #For healing the player
    self.health = min(8, self.health + 5)

  def move(self) -> None: #Gets player input and moves player
    if px.btn(px.KEY_SPACE):
      return

    speed = 0.3125

    if px.btn(px.KEY_UP) and not px.btn(px.KEY_DOWN):
      self.location[1] += speed
    elif px.btn(px.KEY_DOWN) and not px.btn(px.KEY_UP):
      self.location[1] -= speed
    if px.btn(px.KEY_RIGHT) and not px.btn(px.KEY_LEFT):
      self.location[0] += speed
    elif px.btn(px.KEY_LEFT) and not px.btn(px.KEY_RIGHT):
      self.location[0] -= speed

  def nearestTiles(self, pos) -> list[list[float]]: #Finds the nearest tiles
    posInTile = [pos[0] - pos[0]%1 >= 0.5, pos[1] - pos[1]%1]
    
    for axis in range(2):
      if posInTile[axis]:
        posInTile[axis] = 1
      else:
        posInTile[axis] = -1
    
    tile = [pos[0]//1, pos[1]//1]
    return [
      [tile[0] + posInTile[0], tile[1] + posInTile[1]],
      [tile[0] + posInTile[0], tile[1]],
      [tile[0], tile[1] + posInTile[1]],
      tile
      ]

  def closestPoints(self, tile, pos):
    points = [[tile[0], tile[1]]]

  def collision(self, room) -> None: #Moves the player back to avoid walking into solid objects
    solidTiles = ['Wall Top', 'Wall Bottom', 'Wall Left', 'Wall Right', 'Corner Inner', 'Corner Outer', 'Pillar', 'Boss Door', 'Self Locking Door']
    pos = [self.location[0]/16, self.location[1]/16]

    nearest = self.nearestTiles(pos)

    for tile in nearest:
      if tile in solidTiles:
        # collision...
        pass

  def update(self, gameMap) -> None:
    self.move()

    # self.collision(gameMap)

  def draw(self, SCREENHEIGHT, shift) -> None:
    locX = SCREENHEIGHT*7/9 + self.location[0]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2 - shift[0]
    locY = SCREENHEIGHT     - self.location[1]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2 + shift[1]
    img = 0
    w = 16
    h = 16
    scale = SCREENHEIGHT/9/16
    
    px.blt(locX, locY, img, 0, 48, w, h, px.COLOR_BLACK, scale=scale)
