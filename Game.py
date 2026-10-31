# Generic Dungeon Game - The whole game
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 31/10/2026

# Imports
import pyxel as px
from datetime import datetime

class Game(): #Main Game class. Initialising a Game object runs the game
  def __init__(self):
# constants
    self.SCREENWIDTH = 640
    self.SCREENHEIGHT = 360
    self.TIMECONSTANT = 1

# Initialise everything
    self.getSeed()
    self.expectedLength = 15 # int(input("Expected time (minutes): "))
    self.createMap()
    self.currentRoom = [0, 0]

    px.init(640, 360)
    px.run(self.update, self.draw)

  def getSeed(self):
    self.seed = hash(datetime.now()[:11]) # yyyy-mm-dd hh:mm:ss.ssssss

  def varHash(self, var):
    return hash([self.getSeed, var])

  def createMap(self):
# Find nearest integer room number
    numRooms = self.expectedLength*self.TIMECONSTANT
    self.map = {}
    self.map[[0, 1]] = Room(roomType="Boss")
    self.map([0, 0]) = Room(roomType="Node")


  def update(self):
    self.map(self.currentRoom).update()

  def draw(self):
    self.map[self.currentRoom].draw()

class Room(): #Room class
  def __init__(self, roomType="Normal"):
    if roomType == "Normal":
      pass
    elif roomType == "Node":
      self.North = "Boss Door"
    elif roomType == "Boss":
      self.North = "None"
      self.South = "Self locking door"
      self.East = "None"
      self.West = "None"

  tiles = [["" for i in range(9)] for j in range(9)]

  def update(self):
    pass

  def draw(self):
    for x in range(9):
      for y in range(9):
        pass