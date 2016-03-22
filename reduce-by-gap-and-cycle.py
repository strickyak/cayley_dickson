# Reduce by Gap & Cycle.
import sys

ALPHABET = 'abcdefxyz'

def TakeInventory(line):
  z = {}
  for c in line:
    if c in ALPHABET:
      z[c] = True
  return sorted(z.keys())

def Renaming(inventory):
  i = 0
  for c in ALPHABET:
    if c in inventory:
      yield c, ALPHABET[i]
      i += 1

def Reduce(line):
  #print 'line:\t', line
  inventory = TakeInventory(line)
  #print 'inv:\t', inventory
  renaming = dict(Renaming(inventory))
  #print 'renam:\t', sorted(renaming.items())
  z = []
  for c in line:
    if c in renaming:
      z.append(renaming[c])
    else:
      z.append(c)
  ret = ''.join(z)
  #print 'outp:\t', ret
  return ret

for line in sys.stdin:
  line = line.rstrip()
  print Reduce(line)
