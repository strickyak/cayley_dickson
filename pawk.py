import sys

pred = sys.argv[1]
expr = sys.argv[2]

for line in sys.stdin:
  line = line.rstrip()
  w = line.split()

  if eval(pred):
    print eval(expr)
