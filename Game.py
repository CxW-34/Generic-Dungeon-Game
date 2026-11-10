# Generic Dungeon Game - Game Class
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 10/11/2026

# Imports
from datetime import datetime
import pyxel as px

from sharedFunctions import hash
from Room import Room
from Player import Player

#Classes
class Game(): #Main Game class. Initialising a Game object runs the game
  def __init__(self):
    # constants
    self.SCREENHEIGHT = 360*2
    self.SCREENWIDTH = int(self.SCREENHEIGHT/9*16)
    self.TIMECONSTANT = 2.75

    self.expectedLength = 15 # int(input('How long will the game be? (minutes): '))

    # Initialise everything
    self.seed = hash(str(datetime.now())[:10]) # yyyy-mm-dd hh:mm:ss.ssssss
    self.totalRooms = int(self.TIMECONSTANT*self.expectedLength)
    self.map = {}
    self.toAdd = []
    
    self.createMap()
    self.currentRoom = [0, 0]
    for room in self.map:
      self.map[room].buildRoom()

    self.player = Player()

    px.init(width=self.SCREENWIDTH, height=self.SCREENHEIGHT, title='Generic Dungeon Game', fps=144)
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

  def drawMapRoom(self, scale, centre, room) -> None: #Draws a room on the map
    room = self.map[room]
    
    #Find location and choose colour
    locX = room.location[0]*scale + centre[0] - (scale*0.4)
    locY = self.SCREENHEIGHT - (room.location[1]*scale + centre[1] + (scale*0.4))

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

    if room.location == self.currentRoom:
      px.circ(locX + scale*0.4, locY + scale*0.4, scale*0.15, px.COLOR_LIGHT_BLUE)

  def drawMap(self) -> None: # We have 280:280px to work with to draw the map
    px.rect(0,self.SCREENHEIGHT*2/9,self.SCREENHEIGHT*7/9,self.SCREENHEIGHT*7/9,px.COLOR_NAVY)

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

    scale = self.SCREENHEIGHT*7/9/(max((rightMost-leftMost), (upMost-bottomMost)) + 1)
    centre = [0.0, 0.0]
    
    centre[0] = self.SCREENHEIGHT*7/9*(  (-leftMost + 0.5)/(rightMost - leftMost + 1)  )
    centre[1] = self.SCREENHEIGHT*7/9*(  (-bottomMost + 0.5)/(upMost - bottomMost + 1)  )
    
    for room in self.map:
      self.drawMapRoom(scale, centre, room)

  def devTools(self) -> None: #To test room generation and drawings and stuff
    if False: #False for devTools, True for normal
      return

    if px.btn(px.KEY_SPACE):
      if px.btnp(px.KEY_UP):
        if str([self.currentRoom[0], self.currentRoom[1] + 1]) in self.map:
          self.currentRoom = [self.currentRoom[0], self.currentRoom[1] + 1]
      if px.btnp(px.KEY_DOWN):
        if str([self.currentRoom[0], self.currentRoom[1] - 1]) in self.map:
          self.currentRoom = [self.currentRoom[0], self.currentRoom[1] - 1]
      if px.btnp(px.KEY_LEFT):
        if str([self.currentRoom[0] - 1, self.currentRoom[1]]) in self.map:
          self.currentRoom = [self.currentRoom[0] - 1, self.currentRoom[1]]
      if px.btnp(px.KEY_RIGHT):
        if str([self.currentRoom[0] + 1, self.currentRoom[1]]) in self.map:
          self.currentRoom = [self.currentRoom[0] + 1, self.currentRoom[1]]
    
  def update(self) -> None:
    self.devTools()
    self.map[str(self.currentRoom)].update()

    self.player.update(self.map[str(self.currentRoom)])

    for axis in range(2):
      if self.player.location[axis] > 144:
        self.currentRoom[axis] += 1
        self.player.location[axis] -= 144
      elif self.player.location[axis] < 0:
        self.currentRoom[axis] -= 1
        self.player.location[axis] += 144

  def getShift(self) -> list[float]: #Gets the room shift
    shift = [0.0, 0.0]
    for axis in range(2):
      if self.player.location[axis] > 16*8 - 8:
        shift[axis] += (self.player.location[axis] - 16*8 + 8)*self.SCREENHEIGHT/48
      elif self.player.location[axis] < 24:
        shift[axis] += (self.player.location[axis] - 24)*self.SCREENHEIGHT/48
    return shift

  def draw(self) -> None:
    px.cls(px.COLOR_BLACK)

    shift = self.getShift()

    if shift != [0.0, 0.0]:
      try:
        if shift[0] > 0:
          self.map[str([self.currentRoom[0] + 1, self.currentRoom[1]])].draw(self.SCREENHEIGHT, [shift[0] - self.SCREENHEIGHT, shift[1]])
        elif shift[0] < 0:
          self.map[str([self.currentRoom[0] - 1, self.currentRoom[1]])].draw(self.SCREENHEIGHT, [shift[0] + self.SCREENHEIGHT, shift[1]])
      except: #If there is no room there it will break and reset shift
        shift[0] = 0.0

      try:
        if shift[1] > 0:
          self.map[str([self.currentRoom[0], self.currentRoom[1] + 1])].draw(self.SCREENHEIGHT, [shift[0], shift[1] - self.SCREENHEIGHT])
        elif shift[1] < 0:
          self.map[str([self.currentRoom[0], self.currentRoom[1] - 1])].draw(self.SCREENHEIGHT, [shift[0], shift[1] + self.SCREENHEIGHT])
      except: #Read the other one
        shift[1] = 0.0

    #Main map room placed afterwards so if shift defaults to 0 the map is not shifted
    self.map[str(self.currentRoom)].draw(self.SCREENHEIGHT, shift)
    self.player.draw(self.SCREENHEIGHT, shift)

    self.drawMap()
    px.rect(0, 0, self.SCREENWIDTH*7/16, self.SCREENHEIGHT*2/9, px.COLOR_BLACK)