
w = []

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
