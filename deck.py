w = []

for a in ["a", ""]:
  for b in ["b", ""]:
    for c in ["c", ""]:
      for x in ["x", ""]:
        for y in ["y", ""]:
          z = a+b+c+x+y
          z = z if z else "-1"
          if len(z) in [1, 2, 3]:
            w.append(z)

for a in ["a", ""]:
  for b in ["b", ""]:
    for c in ["c", ""]:
      for x in ["x", ""]:
        for y in ["y", ""]:
          z = a+b+c+x+y
          z = z if z else "-1"
          if len(z) in [2,]:
            w.append(z)

w.reverse()

for x in range(8):
    print ""
    print "%8s%12s%12s%12s" % (w.pop(), w.pop(), w.pop(), w.pop())
    print ""
    print ""

if False:
  for a in ["a", ""]:
    for b in ["b", ""]:
      for c in ["c", ""]:
        for x in ["x", ""]:
          for y in ["y", ""]:
            z = a+b+c+x+y
            w.append(z if z else "-1")

  for x in range(8):
      print ""
      print ""
      print ""
      print "%10s%20s%20s%20s" % (w.pop(), w.pop(), w.pop(), w.pop())
      print ""
      print ""
      print ""
      print ""
