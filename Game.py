# Generic Dungeon Game - Game Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 27/11/2026

# Imports
from datetime import datetime
import pyxel as px
import random as rng

from sharedFunctions import hash, posNeg, length
from Room import Room
from Player import Player

#Classes
class Game(): #Main Game class. Initialising a Game object runs the game
  def __init__(self):
    # constants
    SCALE = 5
    self.HEIGHT = 144*SCALE
    self.WIDTH = int(self.HEIGHT/9*16)
    self.TIMECONSTANT = 2.75
    self.gameState = 'play'

    self.expectedLength = 15 # int(input('How long will the game be? (minutes): '))

    # Initialise everything
    self.seed = hash(str(datetime.now())[:10]) # yyyy-mm-dd hh:mm:ss.ssssss
    self.totalRooms = int(self.TIMECONSTANT*self.expectedLength)
    self.map = {}
    self.toAdd = []
    
    self.createMap()
    self.cRoom = [0, 0]
    for room in self.map:
      self.map[room].buildRoom()

    self.player = Player()

    self.perlinNoise(5, 0.025)
    self.perlinNoise(4, 0.05)
    self.perlinNoise(3, 0.075)
    self.perlinNoise(2, 0.6)
    self.perlinNoise(1, 0.8)
    self.makeTemperament()

    px.init(width=self.WIDTH, height=self.HEIGHT, title='Generic Dungeon Game', fps=144)
    px.load('Assets.pyxres')
    px.run(self.update, self.draw)

  def makeRoom(self, loc, roomType='Normal') -> None: #Makes a room and checks if more rooms are due to be added
    self.map[str(loc)] = Room(location=loc, totalRooms=self.totalRooms, map=self.map, toAdd=self.toAdd, roomType=roomType)
    
    if self.map[str(loc)].North != 'None':
      if (not [loc[0], loc[1] + 1] in self.toAdd) and (not str([loc[0], loc[1] + 1]) in self.map):
        self.toAdd.append([loc[0], loc[1] + 1])
    
    if self.map[str(loc)].South != 'None':
      if (not [loc[0], loc[1] - 1] in self.toAdd) and (not str([loc[0], loc[1] - 1]) in self.map):
        self.toAdd.append([loc[0], loc[1] - 1])
    
    if self.map[str(loc)].West != 'None':
      if (not [loc[0] - 1, loc[1]] in self.toAdd) and (not str([loc[0] - 1, loc[1]]) in self.map):
        self.toAdd.append([loc[0] - 1, loc[1]])
    
    if self.map[str(loc)].East != 'None':
      if (not [loc[0] + 1, loc[1]] in self.toAdd) and (not str([loc[0] + 1, loc[1]]) in self.map):
        self.toAdd.append([loc[0] + 1, loc[1]])

  def createMap(self) -> None: #Used at start
    self.makeRoom([0, 0], roomType='Node')
    self.makeRoom([0, 1], roomType='Boss')
    self.toAdd.remove([0, 1])
    self.map['[0, 0]'].roomFound = True
    self.map['[0, 1]'].roomFound = True

    while len(self.toAdd):
      self.makeRoom(self.toAdd[0])
      self.toAdd = self.toAdd[1:]


  def devTools(self) -> None: #To test room generation and drawings and stuff
    if False: #False for devTools, True for normal
      return

    if px.btn(px.KEY_SPACE):
      if px.btnp(px.KEY_UP):
        if str([self.cRoom[0], self.cRoom[1] + 1]) in self.map:
          self.cRoom = [self.cRoom[0], self.cRoom[1] + 1]
      if px.btnp(px.KEY_DOWN):
        if str([self.cRoom[0], self.cRoom[1] - 1]) in self.map:
          self.cRoom = [self.cRoom[0], self.cRoom[1] - 1]
      if px.btnp(px.KEY_LEFT):
        if str([self.cRoom[0] - 1, self.cRoom[1]]) in self.map:
          self.cRoom = [self.cRoom[0] - 1, self.cRoom[1]]
      if px.btnp(px.KEY_RIGHT):
        if str([self.cRoom[0] + 1, self.cRoom[1]]) in self.map:
          self.cRoom = [self.cRoom[0] + 1, self.cRoom[1]]


  def generateVectorMap(self, scale) -> list[list[float]]: #Generates the vectorMap
    leftMost, rightMost, upMost, bottomMost = self.getBounds()
    width = (rightMost - leftMost)*2
    height = (upMost - bottomMost)*2
    hashMap = [[hash(str(x) + str(y) + str(scale) + self.seed) for y in range(height)] for x in range(width)]
    
    vectorMap = []
    for x in range(len(hashMap)):
      row = []
      for y in range(len(hashMap)): #Makes a singular random gradient vector

        rng.seed = self.seed + str(x) + str(scale)
        vectorX = rng.random() - 0.5
        rng.seed = self.seed + str(y) + str(scale)
        vectorY = rng.random() - 0.5
        size = (vectorX**2 + vectorY**2)**0.5
        vectorX = vectorX/size
        vectorY = vectorY/size
        row.append([vectorX, vectorY])
      vectorMap.append(row)
    
    return vectorMap

  def dotProduct(self, a, b) -> float: #Returns the dot product of two 2D vectors, a and b
    if a == [0, 0]:
      return 0
    if b == [0, 0]:
      return 0
    return (a[0]*b[0] + a[1]*b[1])/ (length(a) * length(b))

  def getCorners(self, vectorMap, mapLoc, scale, x, y) -> list[float]: #Gets the four values from the tile location and the corner vectors
    relLoc = [mapLoc[0] + x/9, mapLoc[1] + y/9] #Location of the tile within the whole map, shifted such that min(x, y)=0

    pos = [int(relLoc[0]//scale), int(relLoc[1]//scale)]
    positions = [ #Top Left, Top Right, Bottom Left, Bottom Right - These are the positions of the gradients in the gradient map to look at
      [pos[0], pos[1] + 1],
      [pos[0] + 1, pos[1] + 1],
      [pos[0], pos[1]],
      [pos[0] + 1, pos[1]]
    ]
    
    displacement = [[relLoc[axis] - positions[i][axis]*scale for axis in range(2)] for i in range(4)]

    return [self.dotProduct(displacement[i], vectorMap[int(positions[i][0]/scale)][int(positions[i][1]/scale)]) for i in range(4)]

  def interPolate(self, corners, x, y) -> None: #Interpolates between the four corners
    top = corners[0] + (corners[1] - corners[0]) * (0.5 + ((x - 0.5)/(0.5 + abs(x - 0.5))))
    bottom = corners[2] + (corners[3] - corners[2]) * (0.5 + ((x - 0.5)/(0.5 + abs(x - 0.5))))
    return bottom + (top - bottom) * (0.5 + ((y - 0.5)/(0.5 + abs(y - 0.5))))

  def perlinNoise(self, scale, strength) -> None: #To make different rooms/tiles different heats
    vectorMap = self.generateVectorMap(scale)
    leftMost, rightMost, upMost, bottomMost = self.getBounds()

    for room in self.map:
      room = self.map[room].location
      mapLoc = [room[0] - leftMost, room[1] - bottomMost]
      for x in range(9):
        for y in range(9):
          
          corners = self.getCorners(vectorMap, mapLoc, scale, x, y)
          self.map[str(room)].tileVars[x][y] += self.interPolate(corners, (mapLoc[0] + x/9)%scale, (mapLoc[1] + y/9)%scale)*strength

  def makeTemperament(self) -> None:
    for room in self.map:
      for x in range(9):
        for y in range(9):
          if self.map[room].tileVars[x][y] < -0.24:
            self.map[room].tileVars[x][y] = 'Cold'
          elif self.map[room].tileVars[x][y] > 0.24:
            self.map[room].tileVars[x][y] = 'Hot'
          else:
            self.map[room].tileVars[x][y] = 'Warm'


  def getBounds(self) -> tuple[int, int, int, int]: #Gets the bounds of the map in integer room locations
    rightMost = 0
    leftMost = 0
    upMost = 0
    bottomMost = 0
    for room in self.map:
      loc = self.map[room].location
      rightMost = max(rightMost, loc[0])
      leftMost = min(leftMost, loc[0])
      upMost = max(upMost, loc[1])
      bottomMost = min(bottomMost, loc[1])

    return leftMost, rightMost, upMost, bottomMost

  def drawMapRoom(self, scale, centre, room) -> None: #Draws a room on the map
    room = self.map[room]
    
    #Find location and choose colour
    locX = room.location[0]*scale + centre[0] - (scale*0.4)
    locY = self.HEIGHT - (room.location[1]*scale + centre[1] + (scale*0.4))

    colour = px.COLOR_GRAY

    if room.roomType == 'Node':
      colour = px.COLOR_DARK_BLUE
    elif room.roomType == 'Boss':
      colour = px.COLOR_RED
    elif room.roomFound == True:
      colour = px.COLOR_GREEN

    px.rect(locX, locY, scale*0.8, scale*0.8, colour) #Make the box
    
    if room.North in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(locX+scale*0.3, locY-scale*0.125, scale*0.2, scale*0.325, colour)
    elif room.North == 'Seamless':
      px.rect(locX, locY-scale*0.125, scale*0.8, scale*0.325, colour)

    if room.South in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(locX+scale*0.3, locY+scale*0.7, scale*0.2, scale*0.225, colour)
    elif room.South == 'Seamless':
      px.rect(locX, locY+scale*0.7, scale*0.8, scale*0.225, colour)

    if room.East in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(locX+scale*0.7, locY+scale*0.3, scale*0.225, scale*0.2, colour)
    elif room.East == 'Seamless':
      px.rect(locX+scale*0.7, locY, scale*0.225, scale*0.8, colour)

    if room.West in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(locX-scale*0.125, locY+scale*0.3, scale*0.225, scale*0.2, colour)
    elif room.West == 'Seamless':
      px.rect(locX-scale*0.125, locY, scale*0.225, scale*0.8, colour)

    if room.location == self.cRoom:
      px.circ(locX + scale*0.4, locY + scale*0.4, scale*0.15, px.COLOR_LIGHT_BLUE)

  def drawMap(self) -> None: # We have 280:280px to work with to draw the map
    px.rect(0,self.HEIGHT*2/9,self.HEIGHT*7/9,self.HEIGHT*7/9,px.COLOR_NAVY)

    leftMost, rightMost, upMost, bottomMost = self.getBounds()

    scale = self.HEIGHT*7/9/(max((rightMost-leftMost), (upMost-bottomMost)) + 1)
    centre = [0.0, 0.0]
    
    centre[0] = self.HEIGHT*7/9*(  (-leftMost + 0.5)/(rightMost - leftMost + 1)  )
    centre[1] = self.HEIGHT*7/9*(  (-bottomMost + 0.5)/(upMost - bottomMost + 1)  )
    
    for room in self.map:
      self.drawMapRoom(scale, centre, room)

  def getShift(self) -> list[float]: #Gets the room shift
    shift = [0.0, 0.0]
    for axis in range(2):
      if self.player.location[axis] > 16*8 - 8:
        shift[axis] += (self.player.location[axis] - 16*8 + 8)*self.HEIGHT/48
      elif self.player.location[axis] < 24:
        shift[axis] += (self.player.location[axis] - 24)*self.HEIGHT/48
    return shift

  def drawGame(self) -> None:
    for layer in range(1, 5):
      shift = self.getShift()

      if shift[0]:
        try:
          self.map[str([self.cRoom[0] + posNeg(shift[0]), self.cRoom[1]])].draw(self.HEIGHT, [shift[0] - self.HEIGHT*posNeg(shift[0]), shift[1]], layer)
        except:
          pass
      if shift[1]:
        try:
          self.map[str([self.cRoom[0], self.cRoom[1] + posNeg(shift[1])])].draw(self.HEIGHT, [shift[0], shift[1] - self.HEIGHT*posNeg(shift[1])], layer)
        except:
          pass
      try: #possible there is no room in the corner
        if shift[0] and shift[1]:
          self.map[str([self.cRoom[0] + posNeg(shift[0]), self.cRoom[1] + posNeg(shift[1])])].draw(self.HEIGHT, [shift[0] - self.HEIGHT*posNeg(shift[0]), shift[1] - self.HEIGHT*posNeg(shift[1])], layer)
      except:
        pass
      
      self.map[str(self.cRoom)].draw(self.HEIGHT, shift, layer)
      self.player.draw(self.HEIGHT, shift, layer)

    self.drawMap()
    px.rect(0, 0, self.WIDTH*7/16, self.HEIGHT*2/9, px.COLOR_BLACK)


  def update(self) -> None:
    if self.gameState == 'play':
      self.devTools()
      self.map[str(self.cRoom)].update()

      self.player.update(self.map[str(self.cRoom)])

      for axis in range(2):
        if self.player.location[axis] > 144:
          self.cRoom[axis] += 1
          self.player.location[axis] -= 144
        elif self.player.location[axis] < 0:
          self.cRoom[axis] -= 1
          self.player.location[axis] += 144

      if self.player.health == 0:
        self.gameState = 'dead'

  def draw(self) -> None:
    px.cls(px.COLOR_BLACK)

    if self.gameState == 'play':
      self.drawGame()#Main map room placed afterwards so if shift defaults to 0 the map is not shifted
    elif self.gameState == 'dead':
      px.text(self.WIDTH/2, self.HEIGHT/2, 'YOU DIED', px.COLOR_RED)


