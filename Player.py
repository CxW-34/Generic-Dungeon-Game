# Generic Dungeon Game - Player Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 10/11/2026

# Imports
import pyxel as px

class Player:
  def __init__(self):
    self.location = [72.0, 72.0] #Shown as player centre
    self.face = 'South'
    self.health = 8
    self.radius = 0.5

  def takeDamage(self, damage) -> None: #Fpr taking damage (to be used by enemy class)
    self.health = max(0, self.health - damage)

  def heal(self) -> None: #For healing the player
    self.health = min(8, self.health + 5)

  def move(self) -> None: #Gets player input and moves player
    if px.btn(px.KEY_SPACE):
      return

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
    posInTile = [pos[0] - pos[0]%1 >= 0.5, pos[1] - pos[1]%1]
    
    for axis in range(2):
      if posInTile[axis]:
        posInTile[axis] = 1
      else:
        posInTile[axis] = -1
    
    tile = [int(pos[0]), int(pos[1])]
    return [
      [tile[0] + posInTile[0], tile[1] + posInTile[1]],
      [tile[0] + posInTile[0], tile[1]],
      [tile[0], tile[1] + posInTile[1]],
      tile
      ]

  def dist(self, pos1, pos2=None): #Returns distance between two points using pythag (or a vectors length)
    if pos2 != None:
      return (  (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2  )**0.5
    return (pos1[0]**2 + pos1[1]**2)**0.5

  def closestPoints(self, tile, pos) -> list[list[float]]: #Finds the closest point/two points on a tile to the player
    points = [
      [tile[0] + 1, tile[1] + 1],
      [tile[0] + 1, tile[1]],
      [tile[0], tile[1] + 1],
      tile
      ]

    # Gets the distances from the player centre
    distances = [self.dist(pos, points[i]) for i in range(4)]

    # Finds the closest
    closest = [] 
    minDist = 10 # Arbitrary larger than 1.5?
    for i in range(4):
      if distances[i] < minDist:
        minDist = distances[i]
        closest = [points[i]]
      elif distances[i] == minDist:
        closest.append(points[i])

    return closest

  def doCollision(self, room) -> None: #Moves the player back to avoid walking into solid objects
    solidTiles = ['Wall Top', 'Wall Bottom', 'Wall Left', 'Wall Right', 'Corner Inner', 'Corner Outer', 'Pillar', 'Boss Door', 'Self Locking Door']
    pos = [self.location[0]/16, self.location[1]/16]

    nearest = self.nearestTiles(pos)
    for tile in nearest:
      if tile[0] in range(1, 9) and tile[1] in range(1, 9):
        if room.tiles[tile[0]][tile[1]] in solidTiles:

          closest = self.closestPoints(tile, pos)
          if len(closest) == 1: #If in range, move player by unit vector * (player rad - |vector|) according to pseudocode
            closest = closest[0]
            if self.dist(pos, closest) < self.radius:
              vector = [closest[i] - pos[i] for i in range(2)]
              vector = [vector[i]/self.dist(vector) for i in range(2)]
              magnitude = self.radius - self.dist(pos, closest)

              self.location = [self.location[i] - vector[i]*magnitude for i in range(2)]
              px.rect(720*7/9 + closest[0]*720/9, 720 - closest[1]*720/9, 1, 1, px.COLOR_WHITE)

  def update(self, gameMap) -> None:
    self.move()

    self.doCollision(gameMap)

  def draw(self, SCREENHEIGHT, shift) -> None:
    locX = SCREENHEIGHT*7/9 + self.location[0]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2 - shift[0]
    locY = SCREENHEIGHT     - self.location[1]*SCREENHEIGHT/9/16 - SCREENHEIGHT/9/8 + 2 + shift[1]
    img = 0
    w = 16
    h = 16
    scale = SCREENHEIGHT/9/16
    
    px.blt(locX, locY, img, 0, 48, w, h, px.COLOR_BLACK, scale=scale)
