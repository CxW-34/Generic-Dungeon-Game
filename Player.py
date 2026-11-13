# Generic Dungeon Game - Player Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 13/11/2026

# Imports
import pyxel as px

class Player:
  def __init__(self):
    self.location = [72.0, 72.0] #Shown as player centre
    self.face = 'South'
    self.health = 8
    self.radius = 0.5
    self.dashTimer = 0

  def takeDamage(self, damage) -> None: #Fpr taking damage (to be used by enemy class)
    self.health = max(0, self.health - damage)

  def heal(self) -> None: #For healing the player
    self.health = min(8, self.health + 5)

  def doInputs(self) -> None: #Gets player input and moves player
    if px.btn(px.KEY_SPACE):
      return

    if px.btn(px.KEY_C):
      pass
    speed = 0.25

    if px.btn(px.KEY_UP) and not px.btn(px.KEY_DOWN):
      self.location[1] += speed
    elif px.btn(px.KEY_DOWN) and not px.btn(px.KEY_UP):
      self.location[1] -= speed
    if px.btn(px.KEY_RIGHT) and not px.btn(px.KEY_LEFT):
      self.location[0] += speed
    elif px.btn(px.KEY_LEFT) and not px.btn(px.KEY_RIGHT):
      self.location[0] -= speed

  def nearestTiles(self, pos) -> list[list[int]]: #Finds the nearest tiles
    tile = [int(pos[0]), int(pos[1])]

    return [
      [tile[0] + 1, tile[1] + 1],
      [tile[0] + 1, tile[1] - 1],
      [tile[0] + 1, tile[1]],
      [tile[0] - 1, tile[1] + 1],
      [tile[0] - 1, tile[1] - 1],
      [tile[0] - 1, tile[1]],
      [tile[0], tile[1] + 1],
      [tile[0], tile[1] - 1],
      tile
    ]

  def dist(self, pos1, pos2=None): #Returns distance between two points using pythag (or a vectors length)
    if pos2 != None:
      return (  (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2  )**0.5
    return (pos1[0]**2 + pos1[1]**2)**0.5

  def doCollision(self, room) -> None:
    solidTiles = [
      'Wall Top', 'Wall Bottom', 'Wall Left', 'Wall Right', 'Corner Inner', 'Corner Outer',
      'Pillar', 'Boss Door', 'Self Locking Door'
      ]
    pos = [self.location[0]/16, self.location[1]/16]

    nearest = self.nearestTiles(pos)

    for tile in nearest:
      if tile[0] in range(9) and tile[1] in range(9):
        if room.tiles[tile[0]][tile[1]] in solidTiles or (room.tiles[tile[0]][tile[1]] == 'Hole' and self.dashTimer == 0): #Start box collision here
          tile = [tile[i] + 0.5 for i in range(2)]

          for axis in range(2):
            axis2 = 0 if axis else 1
              
            if tile[axis] - 0.5 < pos[axis] < tile[axis] + 0.5:
              if tile[axis2] < pos[axis2] < tile[axis2] + self.radius + 0.5:
                pos[axis2] = tile[axis2] + self.radius + 0.5
              elif tile[axis2] - 0.5 - self.radius < pos[axis2] < tile[axis2]:
                pos[axis2] = tile[axis2] - self.radius - 0.5

          #If in range, move player by unit vector * (player rad - |vector|) according to pseudocode
          corners = [
            [tile[0] + 0.5, tile[1] + 0.5],
            [tile[0] + 0.5, tile[1] - 0.5],
            [tile[0] - 0.5, tile[1] + 0.5],
            [tile[0] - 0.5, tile[1] - 0.5]
          ]
          for corner in corners:
            if self.dist(pos, corner) < self.radius:
              vector = [corner[i] - pos[i] for i in range(2)]
              vector = [vector[i]/self.dist(vector) for i in range(2)]
              magnitude = self.radius - self.dist(pos, corner)

              pos = [pos[i] - vector[i]*magnitude for i in range(2)]
              px.rect(720*7/9 + corner[0]*720/9, 720 - corner[1]*720/9, 1, 1, px.COLOR_WHITE)

    self.location = [pos[0]*16, pos[1]*16]

  def update(self, gameMap) -> None:
    self.doInputs()

    self.doCollision(gameMap)
    if self.dashTimer:
      self.dashTimer -= 1

  def draw(self, SCREENHEIGHT, shift) -> None:
    locX = SCREENHEIGHT*7/9 + self.location[0]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2 - shift[0]
    locY = SCREENHEIGHT     - self.location[1]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2 + shift[1]
    img = 0
    w = 16
    h = 16
    scale = SCREENHEIGHT/9/16
    
    px.blt(locX, locY, img, 0, 48, w, h, px.COLOR_BLACK, scale=scale)
