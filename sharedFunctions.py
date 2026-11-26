# Generic Dungeon Game - Shared Functions
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 26/11/2026

# Imports
from hashlib import sha3_256

#Functions
def hash(string) -> str: # The inbuilt python hash method is finicky
  return sha3_256(str(string).encode('utf-8')).hexdigest()

def posNeg(num) -> int: #returns if a number is positive or negative
  if not num:
    return 0
  if num > 0:
    return 1
  else:
    return -1

def length(vector) -> float: #Returns a float length from a vector e.g v -> |v|
  return (vector[0]**2 + vector[1]**2)**0.5