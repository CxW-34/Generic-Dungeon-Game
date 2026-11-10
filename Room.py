# Generic Dungeon Game - Room Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 10/11/2026

# Imports
import random as rng
from math import e
from datetime import datetime
import pyxel as px
from sharedFunctions import hash

class Room(): #Room class
  def __init__(self, location, totalRooms, map, toAdd, roomType='Normal'):
    self.location = location
    self.hash = hash(str(location) + str(datetime.now())[:10])
    
    self.makeConnections(location, totalRooms, map, toAdd, roomType)
    self.roomType = roomType
    self.roomFound = False

  def choiceConnection(self, totalRooms, roomsAdded, direction='') -> str: #Chooses what type of connection to put
    rng.seed = hash(self.hash + direction + 'Change')
    if totalRooms > roomsAdded:
      probability = 1-e**((-1)*(totalRooms - roomsAdded)*2/totalRooms)
      if rng.binomialvariate(p=probability):
        if rng.binomialvariate(p=0.8):
          return 'Arch'
        return 'Seamless'
    return 'None'
  
  def makeConnections(self, location, totalRooms, map, toAdd, roomType) -> None: #Chooses what connections the room will have and returns rooms to make
    if roomType == 'Normal':
      self.North = 'None'
      self.South = 'None'
      self.West = 'None'
      self.East = 'None'
      
      #Try adding connections
      try: # Main: North
        self.North = map[str([location[0], location[1] + 1])].South
      except:
        self.North = self.choiceConnection(totalRooms, len(map) + len(toAdd), 'North')

      try: # Main: South
        self.South = map[str([location[0], location[1] - 1])].North
      except:
        self.South = self.choiceConnection(totalRooms, len(map) + len(toAdd), 'South')

      try: # Main: West
        self.West = map[str([location[0] - 1, location[1]])].East
      except:
        self.West = self.choiceConnection(totalRooms, len(map) + len(toAdd), 'West')

      try: # Main: East
        self.East = map[str([location[0] + 1, location[1]])].West
      except:
        self.East = self.choiceConnection(totalRooms, len(map) + len(toAdd), 'East')
      
    
    elif roomType == 'Node':
      self.North = 'Boss Door'

      #50% chance for each of the rooms to have a link
      rng.seed(hash(str(self.hash) + 'South'))
      if rng.binomialvariate(p=0.95):
        self.South = 'Arch'
      else:
        self.South = 'None'
      rng.seed(hash(str(self.hash) + 'West'))
      if rng.binomialvariate(p=0.95):
        self.West = 'Arch'
      else:
        self.West = 'None'
      rng.seed(hash(str(self.hash) + 'East'))
      if rng.binomialvariate(p=0.95):
        self.East = 'Arch'
      else:
        self.East = 'None'
    
    elif roomType == 'Boss':
      self.North = 'None'
      self.South = 'Self Locking Door'
      self.East = 'None'
      self.West = 'None'

  def roomSides(self) -> None: #Fixes the sides of the room
    for i in range(1, 8): #Make walls
      self.tiles[0][i] = 'Wall Left'
      self.tiles[8][i] = 'Wall Right'
      self.tiles[i][0] = 'Wall Bottom'
      self.tiles[i][8] = 'Wall Top'
    
    self.tiles[0][0] = 'Corner Inner'
    self.tiles[8][8] = 'Corner Inner'
    self.tiles[0][8] = 'Corner Inner'
    self.tiles[8][0] = 'Corner Inner'

    #Connections
    if self.North == 'Seamless':
      for x in range(1, 8):
        self.tiles[x][8] = 'Tile'
      self.tiles[0][8] = 'Wall Left'
      self.tiles[8][8] = 'Wall Right'
    elif self.North != 'None':
      self.tiles[4][8] = self.North

    if self.South == 'Seamless':
      for x in range(1, 8):
        self.tiles[x][0] = 'Tile'
      self.tiles[0][0] = 'Wall Left'
      self.tiles[8][0] = 'Wall Right'
    elif self.South != 'None':
      self.tiles[4][0] = self.South

    if self.West == 'Seamless':
      for y in range(1, 8):
        self.tiles[0][y] = 'Tile'
      if self.tiles[0][0] == 'Wall Left':
        self.tiles[0][0] = 'Corner Outer'
      else:
          self.tiles[0][0] = 'Wall Bottom'
      if self.tiles[0][8] == 'Wall Left':
        self.tiles[0][8] = 'Corner Outer'
      else:
        self.tiles[0][8] = 'Wall Top'
    elif self.West != 'None':
      self.tiles[0][4] = self.West

    if self.East == 'Seamless':
      for y in range(1, 8):
        self.tiles[8][y] = 'Tile'
      if self.tiles[8][8] == 'Wall Right':
        self.tiles[8][8] = 'Corner Outer'
      else:
        self.tiles[8][8] = 'Wall Top'
      if self.tiles[8][0] == 'Wall Right':
        self.tiles[8][0] = 'Corner Outer'
      else:
        self.tiles[8][0] = 'Wall Bottom'
    elif self.East != 'None':
      self.tiles[8][4] = self.East

  def extras(self, tileType) -> None: #Adds holes
    if self.roomType in ['Node', 'Boss']:
      return
    p = 0.0
    match tileType:
      case 'Hole':
        p = 0.2
      case 'Pillar':
        p = 0.06
    rng.seed = hash(self.hash + tileType)
    holesToAdd = rng.binomialvariate(n=49, p=p)
    while holesToAdd:
      rng.seed = hash(rng.seed)
      x = rng.randrange(1, 8)
      rng.seed = hash(rng.seed)
      y = rng.randrange(1, 8)
      if self.tiles[x][y] == 'Tile' and not [x, y] in [[1, 4], [4, 1], [4, 7], [7, 4]]:
        self.tiles[x][y] = tileType
        holesToAdd -= 1

  def buildRoom(self) -> None: #Builds the room
    self.tiles = [['Tile' for i in range(9)] for j in range(9)]
    self.roomSides()
    self.extras('Hole')
    self.extras('Pillar')

  def drawTile(self, x, y, SCREENHEIGHT, layer, shift) -> None: #Draws a tile
    #      Initial shift     |Location shift    |Shift by a little over tile/2 to fix pos|Shift for room slide
    locX = SCREENHEIGHT*7/9 + x*SCREENHEIGHT/9 + SCREENHEIGHT/18 - SCREENHEIGHT/9/8 + 2 - shift[0]
    locY = SCREENHEIGHT     - y*SCREENHEIGHT/9 - SCREENHEIGHT/18 - SCREENHEIGHT/9/8 + 2 + shift[1]
    img = 0 #All images are on 0
    w = 16 #16x16 tiles
    h = 16 #16x16 tiles
    scale = SCREENHEIGHT/9/16 #Width of a pixel

    # Funny debug white dot - top left corner of tile
    # px.rect(SCREENHEIGHT*7/9 + x*SCREENHEIGHT/9 - shift[0], SCREENHEIGHT - y*SCREENHEIGHT/9 + shift[1], 1, 1, px.COLOR_WHITE)

    match layer:
      case 1: #Room
        match self.tiles[x][y]:
          case 'Tile':
            px.blt(locX, locY, img, 16, 0, w, h, scale=scale)
          case 'Hole':
            px.blt(locX, locY, img, 0, 0, w, h, scale=scale)
          case 'Pillar':
            px.blt(locX, locY, img, 32, 16, w, h, scale=scale)
          
          case 'Corner Inner':
            if x == y == 0:
              px.blt(locX, locY, img, 0, 16, -w, -h, scale=scale)
            elif x == 0 and y == 8:
              px.blt(locX, locY, img, 0, 16, -w, h, scale=scale)
            elif x == 8 and y == 0:
              px.blt(locX, locY, img, 0, 16, w, -h, scale=scale)
            elif x == y == 8:
              px.blt(locX, locY, img, 0, 16, w, h, scale=scale)
          
          case 'Corner Outer':
            if x == 0 and y == 0:
              px.blt(locX, locY, img, 16, 16, -w, -h, scale=scale)
            elif x == 8 and y == 0:
              px.blt(locX, locY, img, 16, 16, w, h, scale=scale, rotate=90)
            elif x == 0 and y == 8:
              px.blt(locX, locY, img, 16, 16, w, h, scale=scale, rotate=270)
            else:
              px.blt(locX, locY, img, 16, 16, w, h, scale=scale)
          
          case 'Wall Top':
            px.blt(locX, locY, img, 48, 0, w, h, scale=scale)
          case 'Wall Bottom':
            px.blt(locX, locY, img, 48, 0, w, -h, scale=scale)
          case 'Wall Left':
            px.blt(locX, locY, img, 48, 0, w, h, scale=scale, rotate=270)
          case 'Wall Right':
            px.blt(locX, locY, img, 48, 0, w, h, scale=scale, rotate=90)

      case 2: #Pillar
        match self.tiles[x][y]:
          case 'Pillar':
            px.blt(locX, locY - SCREENHEIGHT/9, img, 48, 16, w, h, px.COLOR_BLACK, scale=scale) #For top bit of the pillar

      case 3: #Doors
        match self.tiles[x][y]:
          case 'Arch' | 'Boss Door' | 'Self Locking Door':
            if self.tiles[x][y] == 'Arch':
              u, v = 0, 32
            else:
              u, v = 16, 32
            if y == 8:
              px.blt(locX, locY, img, u, v, w, h, scale=scale)
            elif y == 0:
              px.blt(locX, locY, img, u, v, w, h, scale=scale, rotate=180)
            elif x == 0:
              px.blt(locX, locY, img, u, v, w, h, scale=scale, rotate=270)
            elif x == 8:
              px.blt(locX, locY, img, u, v, w, h, scale=scale, rotate=90)

  def update(self) -> None:
    pass

  def draw(self, SCREENHEIGHT, shift) -> None:
    for layer in range(1, 4):
      for x in range(9):
        for y in range(9):
          self.drawTile(x, y, SCREENHEIGHT, layer, shift)
