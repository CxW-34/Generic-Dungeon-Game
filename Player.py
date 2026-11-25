# Generic Dungeon Game - Player Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 25/11/2026

# Imports
import pyxel as px
from sharedFunctions import posNeg

class Player:
  def __init__(self):
    self.location = [72.0, 72.0] #Shown as player centre
    self.face = 'South'
    self.health = 8
    self.radius = 0.5
    
    self.isDash = False
    self.dashTimer = 32
    self.maxDash = 32
    self.dashDirection = [0.0, 0.0]

    self.attackFrame = -1
    self.shield = False

  def takeDamage(self, damage) -> None: #Fpr taking damage (to be used by enemy class)
    self.health = max(0, self.health - damage)

  def heal(self) -> None: #For healing the player
    self.health = min(8, self.health + 5)

  def doMovement(self) -> None: #Handles player movement
    if px.btnp(px.KEY_C): #Enter/exit dash state
      if self.isDash:
        self.isDash = False
      else:
        if self.dashTimer == self.maxDash:
          self.isDash = True
      
          self.dashDirection = [0.0, 0.0]
          if px.btn(px.KEY_UP):
            self.dashDirection[1] += 1
          if px.btn(px.KEY_DOWN):
            self.dashDirection[1] -= 1
          if px.btn(px.KEY_LEFT):
            self.dashDirection[0] -= 1
          if px.btn(px.KEY_RIGHT):
            self.dashDirection[0] += 1

          if self.dashDirection[0] and self.dashDirection[1]:
            for axis in range(2):
              self.dashDirection[axis] = self.dashDirection[axis]/(2**0.5)

          if (not self.dashDirection[0]) and (not self.dashDirection[1]):
            self.isDash = False


    if self.isDash:
      for axis in range(2):
        self.location[axis] += self.dashDirection[axis]
      return

    #If not dashing have usual controls

    #Movement
    velocity = [0.0, 0.0]
    if px.btn(px.KEY_UP) and not px.btn(px.KEY_DOWN):
      velocity[1] += 0.25
    elif px.btn(px.KEY_DOWN) and not px.btn(px.KEY_UP):
      velocity[1] -= 0.25
    if px.btn(px.KEY_RIGHT) and not px.btn(px.KEY_LEFT):
      velocity[0] += 0.25
    elif px.btn(px.KEY_LEFT) and not px.btn(px.KEY_RIGHT):
      velocity[0] -= 0.25

    if velocity[0] and velocity[1]:
      for axis in range(2):
        velocity[axis] = velocity[axis]/(2**0.5)

    for axis in range(2):
      self.location[axis] += velocity[axis]

    if not (self.shield or self.attackFrame > -1): #When holding the shield, the player keeps facing the same direction
      match [posNeg(velocity[axis]) for axis in range(2)]:
        case [0, 1]:
          self.face = 'North'
        case [0, -1]:
          self.face = 'South'
        case [-1, 0]:
          self.face = 'West'
        case [1, 0]:
          self.face = 'East'
        case _:
          pass

  def doAttack(self) -> None: #Attacks if attacking
    if px.btnp(px.KEY_X):
      if self.attackFrame == -1:
        self.attackFrame = 36

  def doShield(self) -> None: #Shields if shielding
    self.shield = px.btn(px.KEY_Z)

  def doInputs(self) -> None: #Gets player input and moves player
    if px.btn(px.KEY_SPACE):
      return

    self.doMovement()
    self.doAttack()
    self.doShield()

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
        if room.tiles[tile[0]][tile[1]] in solidTiles or (room.tiles[tile[0]][tile[1]] == 'Hole' and not self.isDash): #Start box collision here
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
    if self.isDash:
      self.dashTimer  -= 1
    else:
      self.dashTimer = min(self.dashTimer + 1, self.maxDash)
    if self.dashTimer <= 0:
      self.isDash = False

    if self.attackFrame > -1:
      self.attackFrame -= 1

  def draw(self, HEIGHT, shift, layer) -> None:
    if layer != 2:
      return
    
    locX = HEIGHT*7/9 + self.location[0]*HEIGHT/9/16 - HEIGHT/9/8 + 2 - shift[0]
    locY = HEIGHT     - self.location[1]*HEIGHT/9/16 - HEIGHT/9/8 + 2 + shift[1]
    img = 0
    w = 16
    h = 16
    scale = HEIGHT/9/16
    rotate = 0
    match self.face:
      case 'North':
        rotate = 0
      case 'South':
        rotate = 180
      case 'East':
        rotate = 90
      case 'West':
        rotate = 270

    px.blt(locX, locY, img, 0, 48, w, h, px.COLOR_BLACK, rotate=rotate, scale=scale)
