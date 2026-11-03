# Generic Dungeon Game - The whole game
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 03/11/2026

# Imports
from hashlib import sha3_256
from datetime import datetime
import random as rng
from math import e
import pyxel as px

#Functions
def hash(string): # The inbuilt python hash method is finicky
  return sha3_256(str(string).encode('utf-8')).hexdigest()

#Classes
class Game(): #Main Game class. Initialising a Game object runs the game
  def __init__(self):
# constants
    self.SCREENWIDTH = 2560#640
    self.SCREENHEIGHT = 1440#360
    self.TIMECONSTANT = 2.75

    self.expectedLength = 15 # int(input('How long will the game be? (minutes): '))

# Initialise everything
    self.seed = hash(str(datetime.now())[:10]) # yyyy-mm-dd hh:mm:ss.ssssss
    self.totalRooms = int(self.TIMECONSTANT*self.expectedLength)
    self.map = {}
    self.toAdd = []
    
    self.createMap()
    self.currentRoom = [0, 0]

    px.init(self.SCREENWIDTH, self.SCREENHEIGHT)
    px.load('Assets.pyxres')
    px.run(self.update, self.draw)

  def makeRoom(self, loc, roomType='Normal'): #Makes a room and checks if more rooms are due to be added
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

  def createMap(self): #Used at start
    self.makeRoom([0, 0], roomType='Node')
    self.makeRoom([0, 1], roomType='Boss')
    self.toAdd.remove([0, 1])
    self.map['[0, 0]'].roomFound = True
    self.map['[0, 1]'].roomFound = True

    while len(self.toAdd):
      self.makeRoom(self.toAdd[0])
      self.toAdd = self.toAdd[1:]

  def drawMapRoom(self, scale, centre, room): #Draws a room on the map
    room = self.map[room]
    
    #Find location and choose colour
    loc = [
      room.location[0]*scale + centre[0] - (scale*0.4),
      room.location[1]*scale + centre[1] + (scale*0.4)
    ]

    colour = px.COLOR_GRAY # px.COLOR_NAVY
    # if self.player.hasMap:
    #   colour = px.COLOR_GRAY
    if room.roomType == 'Node':
      colour = px.COLOR_DARK_BLUE
    elif room.roomType == 'Boss':
      colour = px.COLOR_RED
    elif room.roomFound == True:
      colour = px.COLOR_GREEN

    px.rect(loc[0], self.SCREENHEIGHT-loc[1], scale*0.8, scale*0.8, colour) #Make the box
    
    if room.North in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(loc[0]+scale*0.3, self.SCREENHEIGHT-loc[1]-scale*0.125, scale*0.2, scale*0.325, colour)
    elif room.North == 'Seamless':
      px.rect(loc[0], self.SCREENHEIGHT-loc[1]-scale*0.125, scale*0.8, scale*0.325, colour)

    if room.South in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(loc[0]+scale*0.3, self.SCREENHEIGHT-loc[1]+scale*0.7, scale*0.2, scale*0.225, colour)
    elif room.South == 'Seamless':
      px.rect(loc[0], self.SCREENHEIGHT-loc[1]+scale*0.7, scale*0.8, scale*0.225, colour)

    if room.East in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(loc[0]+scale*0.7, self.SCREENHEIGHT-loc[1]+scale*0.3, scale*0.225, scale*0.2, colour)
    elif room.East == 'Seamless':
      px.rect(loc[0]+scale*0.7, self.SCREENHEIGHT-loc[1], scale*0.225, scale*0.8, colour)

    if room.West in ['Arch', 'Boss Door', 'Self Locking Door']:
      px.rect(loc[0]-scale*0.125, self.SCREENHEIGHT-loc[1]+scale*0.3, scale*0.225, scale*0.2, colour)
    elif room.West == 'Seamless':
      px.rect(loc[0]-scale*0.125, self.SCREENHEIGHT-loc[1], scale*0.225, scale*0.8, colour)

  def drawMap(self): # We have 280:280px to work with to draw the map
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
    centre = [0, 0]
    
    centre[0] = self.SCREENHEIGHT*7/9*(  (-leftMost + 0.5)/(rightMost - leftMost + 1)  )
    centre[1] = self.SCREENHEIGHT*7/9*(  (-bottomMost + 0.5)/(upMost - bottomMost + 1)  )
    
    for room in self.map:
      self.drawMapRoom(scale, centre, room)
    
  def update(self):
    self.map[str(self.currentRoom)].update()

  def draw(self):
    self.map[str(self.currentRoom)].draw()

    self.drawMap()

class Room(): #Room class
  def __init__(self, location, totalRooms, map, toAdd, roomType='Normal'):
    self.location = location
    self.hash = hash(str(location) + str(datetime.now())[:10])
    
    self.makeConnections(location, totalRooms, map, toAdd, roomType)
    self.roomType = roomType
    self.roomFound = False

    self.buildRoom()

  def choiceConnection(self, totalRooms, roomsAdded, direction=''): #Chooses what type of connection to put
    rng.seed(hash(self.hash + direction + 'Change'))
    if totalRooms > roomsAdded:
      probability = 1-e**((-1)*(totalRooms - roomsAdded)*2/totalRooms)
      if rng.binomialvariate(p=probability):
        if rng.binomialvariate(p=0.8):
          return 'Arch'
        return 'Seamless'
    return 'None'
  
  def makeConnections(self, location, totalRooms, map, toAdd, roomType): #Chooses what connections the room will have and returns rooms to make
    if location == [9, -6]:
      pass
    
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
      if rng.binomialvariate(p=0.8):
        self.South = 'Arch'
      else:
        self.South = 'None'
      rng.seed(hash(str(self.hash) + 'West'))
      if rng.binomialvariate(p=0.8):
        self.West = 'Arch'
      else:
        self.West = 'None'
      rng.seed(hash(str(self.hash) + 'East'))
      if rng.binomialvariate(p=0.8):
        self.East = 'Arch'
      else:
        self.East = 'None'
    
    elif roomType == 'Boss':
      self.North = 'None'
      self.South = 'Self Locking Door'
      self.East = 'None'
      self.West = 'None'

  def buildRoom(self): #Builds the room
    self.tiles = [['Tile' for i in range(9)] for j in range(9)]
    for i in range(1, 8): #Make walls
      self.tiles[0][i] = 'Wall Left'
      self.tiles[8][i] = 'Wall Right'
      self.tiles[i][0] = 'Wall Top'
      self.tiles[i][8] = 'Wall Bottom'
    self.tiles[0][0] = 'Corner Inner'
    self.tiles[8][8] = 'Corner Inner'
    self.tiles[0][8] = 'Corner Inner'
    self.tiles[8][0] = 'Corner Inner'

    #Connections
    if self.North == 'Arch':
      self.tiles[4][0] = 'Arch'
    elif self.North == 'Seamless':
      for i in range(1, 8):
        self.tiles[0][i] = 'Tile'
      self.tiles[0][0] = 'Wall Left'
      self.tiles[0][8] = 'Wall Right'

    if self.South == 'Arch':
      self.tiles[4][8] = 'Arch'
    elif self.South == 'Seamless':
      for i in range(1, 8):
        self.tiles[8][i] = 'Tile'
      self.tiles[8][0] = 'Wall Left'
      self.tiles[8][8] = 'Wall Right'

    if self.West == 'Arch':
      self.tiles[0][4] = 'Arch'
    elif self.West == 'Seamless':
      for i in range(1, 8):
        self.tiles[i][0] = 'Tile'
      
      if self.tiles[0][0] == 'Wall Left':
        self.tiles[0][0] = 'Corner Outer'
      else:
          self.tiles[0][0] = 'Wall Top'
      if self.tiles[8][0] == 'Wall Left':
        self.tiles[8][0] = 'Corner Outer'
      else:
        self.tiles[8][0] = 'Wall Bottom'

    if self.East == 'Arch':
      self.tiles[8][4] = 'Arch'
    elif self.West == 'Seamless':
      for i in range(1, 8):
        self.tiles[i][8] = 'Tile'
      if self.tiles[0][8] == 'Wall Right':
        self.tiles[0][8] = 'Corner Outer'
      else:
        self.tiles[0][8] = 'Wall Top'
      if self.tiles[8][8] == 'Wall Right':
        self.tiles[8][8] = 'Corner Outer'
      else:
        self.tiles[8][8] = 'Wall Bottom'

  def drawTile(self, x, y, SCREENHEIGHT, SCREENWIDTH):
    locX = SCREENHEIGHT*7/9+SCREENHEIGHT/18+x*SCREENHEIGHT/9
    locY = y*SCREENHEIGHT/9+SCREENHEIGHT/18
    img = 0
    w=16
    h=16
    scale=SCREENHEIGHT/9/16
    if self.tiles[x][y] == 'Tile':
      px.blt(x=locX, y=locY, img=img, u=16, v=0, w=w, h=h, colkey=px.COLOR_BLACK, scale=scale)
    elif self.tiles[x][y] == 'Corner Inner':
      if x == y == 0:
        px.blt(x=locX, y=locY, img=img, u=0, v=16, w=-w, h=h, colkey=px.COLOR_BLACK, scale=scale)
      elif x == 0 and y == 8:
        px.blt(x=locX, y=locY, img=img, u=0, v=16, w=-w, h=-h, colkey=px.COLOR_BLACK, scale=scale)
      elif x == 8 and y == 0:
        px.blt(x=locX, y=locY, img=img, u=0, v=16, w=w, h=h, colkey=px.COLOR_BLACK, scale=scale)
      elif x == y == 8:
        px.blt(x=locX, y=locY, img=img, u=0, v=16, w=w, h=-h, colkey=px.COLOR_BLACK, scale=scale)
    elif self.tiles[x][y] == 'Wall Top':
      px.blt(x=locX, y=locY, img=img, u=48, v=0, w=w, h=h, colkey=px.COLOR_BLACK, scale=scale)
    elif self.tiles[x][y] == 'Wall Bottom':
      px.blt(x=locX, y=locY, img=img, u=48, v=0, w=w, h=-h, colkey=px.COLOR_BLACK, scale=scale)
    elif self.tiles[x][y] == 'Wall Left':
      px.blt(x=locX, y=locY, img=img, u=48, v=0, w=w, h=h, colkey=px.COLOR_BLACK, scale=scale, rotate=270)
    elif self.tiles[x][y] == 'Wall Right':
      px.blt(x=locX, y=locY, img=img, u=48, v=0, w=w, h=h, colkey=px.COLOR_BLACK, scale=scale, rotate=90)

  def update(self):
    pass

  def draw(self):
    for x in range(9):
      for y in range(9):
        self.drawTile(x, y, 1440, 2560)
