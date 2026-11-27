# Generic Dungeon Game - Player Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 27/11/2026

# Imports
from math import e, log
import pyxel as px
from sharedFunctions import posNeg

class Player:
  def __init__(self):
    self.location = [72.0, 72.0] #Shown as player centre
    self.velocity = [0.0, 0.0]
    self.face = 'South'
    self.health = 8
    self.damageCooldown = 0
    self.radius = 0.5
    self.lastDoor = [72.0, 72.0]
    
    self.isDash = False
    self.dashTimer = 32
    self.maxDash = 32
    self.dashDirection = [0.0, 0.0]

    self.friction = [0.01, 0.18]

    self.attackFrame = -1
    self.shield = False

  def takeDamage(self, damage, ignoreCooldown=False) -> None: #Fpr taking damage (to be used by enemy class)
    if not (self.damageCooldown and ignoreCooldown):
      self.health = max(0, self.health - damage)
      self.damageCooldown = 32

  def heal(self) -> None: #For healing the player
    self.health = min(8, self.health + 5)


  def doDash(self) -> None: #Handles dash
    if self.isDash:
      self.isDash = False
    else:
      if self.dashTimer == self.maxDash:
        self.isDash = True
    
        self.dashDirection = [0.0, 0.0]
        if px.btn(px.KEY_UP):
          self.dashDirection[1] += 0.06
        if px.btn(px.KEY_DOWN):
          self.dashDirection[1] -= 0.06
        if px.btn(px.KEY_LEFT):
          self.dashDirection[0] -= 0.06
        if px.btn(px.KEY_RIGHT):
          self.dashDirection[0] += 0.06

        if self.dashDirection[0] and self.dashDirection[1]:
          for axis in range(2):
            self.dashDirection[axis] = self.dashDirection[axis]/(2**0.5)

        if (not self.dashDirection[0]) and (not self.dashDirection[1]):
          self.isDash = False

  def doWalk(self) -> list[float]: #Handles walking
    walk = [0.0, 0.0]
    if px.btn(px.KEY_UP) and not px.btn(px.KEY_DOWN):
      walk[1] += 0.1
    elif px.btn(px.KEY_DOWN) and not px.btn(px.KEY_UP):
      walk[1] -= 0.1
    if px.btn(px.KEY_RIGHT) and not px.btn(px.KEY_LEFT):
      walk[0] += 0.1
    elif px.btn(px.KEY_LEFT) and not px.btn(px.KEY_RIGHT):
      walk[0] -= 0.1

    if walk[0] and walk[1]:
      for axis in range(2):
        walk[axis] = walk[axis]/(2**0.5)

    return walk

  def doFriction(self, room) -> None: #Handles friction
    if self.tileOn(room)[0] == 'Hole' or self.isDash:
      return
    
    match self.tileOn(room)[1]:
      case 'Cold':
        friction = self.friction[0]
      case _:
        friction = self.friction[1]
    for axis in range(2):
      self.velocity[axis] -= friction*self.velocity[axis]

  def changeFacing(self, walk) -> str: #Changes which way the player is facing based on where they are walking
    if not (self.shield or self.attackFrame > -1): #When holding the shield, the player keeps facing the same direction
      match [posNeg(walk[axis]) for axis in range(2)]:
        case [0, 1]:
          return 'North'
        case [0, -1]:
          return 'South'
        case [-1, 0]:
          return 'West'
        case [1, 0]:
          return 'East'
    return self.face

  def doMovement(self, room) -> None: #Handles player movement
    if px.btnp(px.KEY_C): #Enter/exit dash state
      self.doDash()

    match self.tileOn(room)[1]:
      case 'Cold':
        friction = self.friction[0]*3
      case _:
        friction = self.friction[1]*4

    if self.isDash:
      for axis in range(2):
        if self.tileOn(room)[1] == 'Cold':
          self.velocity[axis] += self.dashDirection[axis]*friction*10 #Needs the extra boost on ice
        else:
          self.velocity[axis] += self.dashDirection[axis]*friction
    else: #If not dashing have usual controls
      walk = self.doWalk()
      for axis in range(2):
        self.velocity[axis] += walk[axis]*friction
      self.face = self.changeFacing(walk) #Player faces direction of walking


    #Friction and movement
    self.doFriction(room)
    for axis in range(2):
      self.location[axis] += self.velocity[axis]


  def doAttack(self) -> None: #Attacks if attacking
    if px.btnp(px.KEY_X) and not self.shield:
      if self.attackFrame == -18:
        self.attackFrame = 36

  def doShield(self) -> None: #Shields if shielding
    self.shield = px.btn(px.KEY_Z)
    if self.attackFrame >= 0:
      self.shield = False

  def doInputs(self, room) -> None: #Gets player input and moves player
    if px.btn(px.KEY_SPACE):
      return

    self.doMovement(room)
    self.doAttack()
    self.doShield()

  def tileOn(self, room) -> list[str]: #Checks what tile type the player is on.
    try:
      loc = [int(self.location[0]//16), int(self.location[1]//16)]
      return [room.tiles[loc[0]][loc[1]], room.tileVars[loc[0]][loc[1]]]
    except:
      return ['Tile', 'Warm']

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

  def dist(self, pos1, pos2=None) -> float: #Returns distance between two points using pythag (or a vectors length)
    if pos2 != None:
      return (  (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2  )**0.5
    return (pos1[0]**2 + pos1[1]**2)**0.5

  def doCollision(self, room) -> None: #Moves player to avoid sitting inside
    solidTiles = [
      'Wall Top', 'Wall Bottom', 'Wall Left', 'Wall Right', 'Corner Inner', 'Corner Outer',
      'Pillar', 'Boss Door', 'Self Locking Door'
      ]
    pos = [self.location[0]/16, self.location[1]/16]

    nearest = self.nearestTiles(pos)

    for tile in nearest:
      if tile[0] in range(9) and tile[1] in range(9):
        if room.tiles[tile[0]][tile[1]] in solidTiles: #Start box collision here
          tile = [tile[i] + 0.5 for i in range(2)]

          for axis in range(2):
            axis2 = 0 if axis else 1
              
            if tile[axis] - 0.5 < pos[axis] < tile[axis] + 0.5:
              if tile[axis2] < pos[axis2] < tile[axis2] + self.radius + 0.5:
                pos[axis2] = tile[axis2] + self.radius + 0.5
                self.velocity[axis2] = 0
              elif tile[axis2] - 0.5 - self.radius < pos[axis2] < tile[axis2]:
                pos[axis2] = tile[axis2] - self.radius - 0.5
                self.velocity[axis2] = 0

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
              # px.rect(720*7/9 + corner[0]*720/9, 720 - corner[1]*720/9, 1, 1, px.COLOR_WHITE) #Not sure how this went unnoticed for 2 phases but I think it gets overdrawn by other stuff during the draw phase

    self.location = [pos[0]*16, pos[1]*16]

    if self.tileOn(room)[0] == 'Hole' and not self.isDash:
      self.location = self.lastDoor
      self.velocity = [0.0, 0.0]
      self.takeDamage(1, True)


  def update(self, gameMap) -> None:
    self.doInputs(gameMap)

    self.doCollision(gameMap)
    
    if self.isDash:
      self.dashTimer  -= 1
    else:
      self.dashTimer = min(self.dashTimer + 0.5, self.maxDash)
    if self.dashTimer <= 0:
      self.isDash = False

    if self.attackFrame > -18:
      self.attackFrame -= 1

    self.damageCooldown = max(0, self.damageCooldown - 1)

    if self.location[0]%144 != self.location[0] or self.location[1]%144 != self.location[1]:
      self.lastDoor = [self.location[0]%144, self.location[1]%144]

  def draw(self, HEIGHT, shift, layer) -> None:
    if layer != 2:
      return
    #      Initial shift|Location shift|Shift for room slide|Shift to fix pos
    # locX = HEIGHT*7/9 + self.location[0]*HEIGHT/9/16 - HEIGHT/9/8 + 2 - shift[0]
    # locY = HEIGHT     - self.location[1]*HEIGHT/9/16 - HEIGHT/9/8 + 2 + shift[1]
    scale = HEIGHT/9/16 #Width of a pixel
    locX = HEIGHT*7/9 + self.location[0]*HEIGHT/9/16 - shift[0] + (scale/2 - 0.5)*16 - HEIGHT/18
    locY = HEIGHT     - self.location[1]*HEIGHT/9/16 + shift[1] + (scale/2 - 0.5)*16 - HEIGHT/18
    img = 0
    w = 16
    h = 16
    
    rotate = 0
    
    match self.face:
      case 'North':
        rotate = 0
        sword = [-2, 8]
        shield = [2, 4]
        px.blt(locX, locY, img, 16, 48, w, h, px.COLOR_WHITE, scale=scale) #Player sprite
      case 'South':
        rotate = 180
        sword = [2, -8]
        shield = [-2, -4]
        px.blt(locX, locY, img, 32, 48, w, h, px.COLOR_WHITE, scale=scale)
      case 'East':
        rotate = 90
        sword = [8, 2]
        shield = [4, -2]
        px.blt(locX, locY, img, 0, 48, w, h, px.COLOR_WHITE, scale=scale)
      case _: #West
        rotate = 270
        sword = [-8, -2]
        shield = [-4, 2]
        px.blt(locX, locY, img, 0, 48, -w, h, px.COLOR_WHITE, scale=scale)

    for axis in range(2):
      try:
        sword[axis] = sword[axis]*HEIGHT/9/16
      except:
        print(self.face)
      shield[axis] = shield[axis]*HEIGHT/9/16

    
    
    if self.attackFrame >= 0: #Sword
      px.blt(locX + sword[0], locY - sword[1], img, 0, 64, w, h, px.COLOR_BLACK, rotate, scale)
    if self.shield: #Shield
      px.blt(locX + shield[0], locY - shield[1], img, 16, 64, w, h, px.COLOR_BLACK, rotate, scale)
