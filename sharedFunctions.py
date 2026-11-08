# Generic Dungeon Game - Shared Functions
# Created - 31/10/2026
# Owner - Xia34_
# Last updated - 08/11/2026

# Imports
from hashlib import sha3_256

#Functions
def hash(string) -> str: # The inbuilt python hash method is finicky
  return sha3_256(str(string).encode('utf-8')).hexdigest()
