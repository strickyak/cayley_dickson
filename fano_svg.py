import cayley_dickson as CD
U = CD.Universe(32)

Red='#fbb'
Green='#bfb'
Blue='#bbf'

AntiRed='#8ee'
AntiGreen='#e8e'
AntiBlue='#ee8'

def Rect((x, y), (w, h), fill='white', width=3):
  print '<rect x="%f" y="%f" width="%f00" height="%f50" fill="%s" stroke="black" stroke-width="%f" />' % (
      x, y, w, h, fill, width)

def Circle((cx, cy), rad, color='white', width=1, peek=''):
  if peek == 'abcxy':
    width = 5
  if color is None:
    color = 0, 0, 0
  print '<circle cx="%f" cy="%f" r="%f" stroke="black" fill="%s" stroke-width="%d" ></circle>' % (
      cx, cy, rad, color, width)
  
def Text((x, y), s, i=0):
  if type(s) is list or type(s) is tuple:
    i = 0
    for e in s:
      Text((x, y), e, i)
      y += 15
      i += 1
  elif i == 0:
    print '<text x="%f" y="%f" fill="black" font-weight="bold" font-size="18" font-family="Arial, Helvetica, sans-serif" font="Open Sans">%s</text> ' % (
        x, y, s)
  else:
    print '<text x="%f" y="%f" fill="black" font-size="14" font-family="Arial, Helvetica, sans-serif" font="Open Sans">%s</text> ' % (
        x, y, s)

def Lines(vec, c='black', fill='none', width=2, extra=''):
  x, y = vec.pop(0)
  s = 'M %f %f ' % (x, y)
  for x, y in vec:
    s += 'L %f %f ' % (x, y)
  print '<path d="%s" fill="%s" stroke="%s" stroke-width="%d" %s></path>' % (s, fill, c, width, extra)

def Cubic(vec, c='black'):
  x, y = vec.pop(0)
  s = 'M %f %f C ' % (x, y)
  for x, y in vec:
    s += ' %f %f ' % (x, y)
  print '<path d="%s" fill="none" stroke="%s" stroke-width="2"></path>' % (s, c)

def Mid((ax, ay), (bx, by)):
  return (ax+bx)/2, (ay+by)/2
def Mid3((ax, ay), (bx, by), (cx, cy)):
  return (ax+bx+cx)/3, (ay+by+cy)/3

def Fano(a, b, c, texts=[]):
  rad = 52
  def T((x, y)):
    return x-24, y-35
  ab, bc, ca = Mid(a, b), Mid(b, c), Mid(c, a)
  abc = Mid3(a, b, c)

  Lines([a, b, c, a])
  Lines([a, bc], 'red')
  Lines([b, ca], 'blue')
  Lines([c, ab], 'green')

  Cubic([ab, a, ca, ca], 'purple')
  Cubic([ca, c, bc, bc], 'purple')
  Cubic([bc, b, ab, ab], 'purple')

  Circle(a, rad, AntiRed, peek=texts[0][0])
  Circle(b, rad, AntiBlue, peek=texts[1][0])
  Circle(c, rad, AntiGreen, peek=texts[2][0])
  Text(T(a), texts.pop(0))
  Text(T(b), texts.pop(0))
  Text(T(c), texts.pop(0))

  Circle(bc, rad, Red)
  Circle(ab, rad, Green)
  Circle(ca, rad, Blue)
  Text(T(ab), texts.pop(0))
  Text(T(bc), texts.pop(0))
  Text(T(ca), texts.pop(0))

  Circle(abc, rad, '#aaa')
  Text(T(abc), texts.pop(0))
  x, y = Mid(abc, c)
  w, h = 70, 100
  peek = texts[0][0]
  if peek == '1':
    width = 5
  else:
    width = 2
  Rect((x-w/2, y-h/2), (w, h), width=width)
  Text((x-w/2+5, y-h/2+15), texts.pop(0))

print '<html><body>'

print '<h3>Cayley-Dickson Trans-Sedenion Hyper-Complex Candyland</h3>'

print '<svg height="1010" width="1010">'
#Lines([(0, 1000), (1000, 1000), (1000, 0), (0, 0), (0, 1000)], fill='#eee', width=1, extra='stroke-dasharray="4"')

SPOTS = 'ac:bc:abc:ab:a:b:c:1'.split(':')
def Texts(suffix):
  return [
    ('%s' % U.Mul(s, '1'),
     '%s&#10140;%s' % ('a', U.Mul(s, 'a')),
     '%s&#10140;%s' % ('b', U.Mul(s, 'b')),
     '%s&#10140;%s' % ('c', U.Mul(s, 'c')),
     '%s&#10140;%s' % ('x', U.Mul(s, 'x')),
     '%s&#10140;%s' % ('y', U.Mul(s, 'y')),
    ) for s in ['%s%s' % (s, suffix) for s in SPOTS]
  ]

Fano((145, 55), (865, 55), (505, 425), texts=Texts(''))
Fano((955, 145), (955, 865), (585, 505), texts=Texts('x'))
Fano((865, 955), (145, 955), (505, 585), texts=Texts('y'))
Fano((55, 865), (55, 145), (425, 505), texts=Texts('xy'))

print '''</svg>

<p> Players use coins for their tokens, initially Heads Up (the "+" orientation)
    in the bold square marked "1" on the first line.
<p> The deck is a mixture of 5 types of cards, those marked "a", "b", "c", "x", and "y".
<p> Shuffle the deck and deal 2 cards face down to each player.
<p> Place the rest of the deck face-down for drawing.
<p> Players take turns drawing 1 card, picking a card from the hand to execute, and discarding it.
<p> To execute a card, multiply your position on the board by the value on the card,
    using Trigintaduonions (32-dimensional trans-sedenions) in the Cayley-Dickson construction,
    and move your token to the product.  Each location is named by the label on the first line, and lists the
    result of multiplying by "a", "b", "c", "x", or "y" on the remaining lines.
<p> Positive and negative numbers share the same positions on the board,
    so use the coin token with Heads Up to indicate positive and Tails Up to indicate negative.
<p> So every time a player moves, if the multiplication result is listed as negative,
    they should flip the coin over.
<p> If a player moves to the same place with the same sign as another player,
    the other player gets sent back to "+1", the start state.
<p> The goal is to move to the bold cirle labeled "abcxy" with positive orientation.
    The first player to do so wins.

<p> <i>You do not need to understand this, to play the game:
    This game is designed to give you intuition about the Cayley-Dickson constrution of hyper-complex numbers.
    It uses a 32-dimensional space of bases, formed from primitive complex bases we name "a", "b", "c", "x", and "y",
    and the real basis "1". We only use unit vectors with one non-zero basis, so combinations of the characters
    "-1abcxy" can name all the numbers.  Once you get used to multiplying these numbers,
    the only tricky thing is the negative sign.
    </i>
</body></html>
'''
