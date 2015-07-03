# cayley-dickson.py
import math, random

rye_rye = False
if rye_rye:
  NUMS = [int, float]
else:
  NUMS = [int, long, float]

def scalar(x):
  return type(x) in NUMS

def add(x, y):
  if scalar(x) and scalar(y):
    return x + y
  else:
    return [xe + ye for xe, ye in zip(x, y)]

def sub(x, y):
  if scalar(x) and scalar(y):
    return x - y
  else:
    return [xe - ye for xe, ye in zip(x, y)]

def neg(x):
  if scalar(x):
    return -x
  else:
    return [-e for e in x]

def conj(x):
  #print "conj <<", x
  if scalar(x):
    z = x
  elif len(x) == 2:
    a, b = x
    z = [a, -b]
  else:
    a, b = split(x)
    z = conj(a) + neg(b)  # List add.
  #print "conj >>", z
  return z

def split(x):
  h = len(x) / 2
  return x[:h], x[h:]

# To get this to work with quaternions
# with my assignments of i, j, k,
# I had to swap x and y here.
def mul(y, x):
  if scalar(x) and scalar(y):
    return x * y
  if scalar(x):
    return [x*e for e in y]
  if scalar(y):
    return [y*e for e in x]

  lx, ly = len(x), len(y)
  assert lx == ly, (lx, ly)
  h = lx/2
  if h == 1:
    # Components are scalars.
    a, b, c, d = x[0], x[1], y[0], y[1]
  else:
    # Components are complex.
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]

  #print "mul <<<<<<", a, b, c, d
  t1 = mul(a, c)
  t2 = mul(d, conj(b))
  left = sub(t1, t2)
  t3 = mul(conj(a), d)
  t4 = mul(c, b)
  right = add(t3, t4)
  #print "mul >>>>>>", t1, t2, t3, t4, ">>>>>>", left, right
  if scalar(left):
    return [left, right]
  else:
    return left + right  # List add.

assert add(3, 4) == 7
assert add([10, 11], [20, 22]) == [30, 33]
assert sub([10, 11], [20, 22]) == [-10, -11]
assert conj(4) == 4
assert conj([55, 66]) == [55, -66]

# Quaternions.
z, u = [0, 0, 0, 0], [1, 0, 0, 0]
i, j, k = [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

assert neg(u) == [-1, 0, 0, 0]

# Test multiplying by 0.
assert mul(z, i) == z
assert mul(z, j) == z
assert mul(z, k) == z
assert mul(i, z) == z
assert mul(j, z) == z
assert mul(k, z) == z

# Test multiplying by 1.
assert mul(u, i) == i
assert mul(u, j) == j
assert mul(u, k) == k
assert mul(i, u) == i
assert mul(j, u) == j
assert mul(k, u) == k

# Test rock-paper-scissors with i, j, k.
#assert mul(i, j) == k
#assert mul(j, k) == i
#assert mul(k, i) == j
#assert mul(j, i) == neg(k)
#assert mul(k, j) == neg(i)
#assert mul(i, k) == neg(j)

def Basis(n, i):
  vec = n * [0] 
  vec[i] = 1
  return vec

# Build the octonions.
K = [Basis(8, i) for i in range(8)]
K0 = 8 * [0]

for i in range(8):
  #print "Octonion %d: %s" % (i, K[i])
  assert K[i] == mul(K[0], K[i])
  assert K[i] == mul(K[i], K[0])
  assert K0 == mul(K[i], K0)

for i in range(8):
  #print
  for j in range(8):
    #print "Octonion %d x %d = %s" % (i, j, mul(K[i], K[j]))
    assert 1 == sum([e != 0 for e in mul(K[i], K[j])])
    assert 1 == sum([abs(e) == 1 for e in mul(K[i], K[j])])
    if i > 0 and i == j:
      assert [-1, 0, 0, 0, 0, 0, 0, 0] == mul(K[i], K[j])

# Generate n-ions: first the 0, then the n bases.
def GenerateNions(n):
  return n * [0], [Basis(n, i) for i in range(n)]

def TestNions(n):
  Zero, V = GenerateNions(n)
  One = V[0]
  MinusOne = neg(One)

  for i in range(n):
    print "%d-ions %d: %s" % (n, i, V[i])
    assert V[i] == mul(One, V[i])
    assert V[i] == mul(V[i], One)
    assert Zero == mul(V[i], Zero)

  for i in range(n):
    print
    for j in range(n):
      print "Octonion %d x %d = %s" % (i, j, mul(V[i], V[j]))
      assert 1 == sum([e != 0 for e in mul(V[i], V[j])])
      assert 1 == sum([abs(e) == 1 for e in mul(V[i], V[j])])
      if i > 0 and i == j:
        assert MinusOne == mul(V[i], V[j])

#TestNions(2)
#TestNions(4)
#TestNions(8)
#TestNions(16)
#TestNions(32)
#TestNions(64)

def Chr(b):
  return chr(97+b)

def Name(vec):
  s = str(sum(vec))
  n = len(vec)
  logn = int(0.5 + math.log(n, 2))
  pos = -1
  for i in range(n):
    if vec[i]:
      pos = i
      break
  assert pos >= 0
    
  for b in range(logn):
    if pos & (1<<b):
      s += Chr(b)
  return s 

def GameHints(n):
  Zero, V = GenerateNions(n)
  One = V[0]
  MinusOne = neg(One)
  logn = int(0.5 + math.log(n, 2))
  print "logn: %f -> %d" % (math.log(n, 2), logn)

  byName = {}
  for i in range(n):
    byName[Name(V[i])] = V[i]

  for name, a in sorted(byName.items()):
    print
    print "[ %s = %s ]" % (name, a)
    for b in range(logn):
      c = Chr(b)
      bvec = Basis(n, 1<<b)
      z = mul(a, bvec)
      assert Name(bvec) == "1"+c, (bvec, Name(bvec), c)
      print "  %s : %s => %s   %s" % (name, c, Name(z), z)

def GameWalk(game, n):
  Zero, V = GenerateNions(n)
  One = V[0]
  MinusOne = neg(One)
  logn = int(0.5 + math.log(n, 2))
  print "logn: %f -> %d" % (math.log(n, 2), logn)

  Goal = MinusOne
  Choices = V
  if game == 2:
    Goal = V[n-1]
    Choices = [V[1<<i] for i in range(logn)]

  a = One
  for i in range(10000):
    r = random.randrange(len(Choices))
    m = Choices[r]
    a = mul(a, m)
    print "%4d: [%2d] %-8s = %s" % (i, r, Name(a), " ".join(["%2d" % e for e in a]))
    if a == Goal: break
  if a != Goal: raise Exception("Never Finished.")
  return i

#GameHints(32)

def LetterMul(s, a):
  n = len(a)
  #print 'LetterMul <<<', s, a
  for c in s:
    b = ord(c) - ord("a")
    a = mul(a, Basis(n, 1<<b))
    #print 'LetterMul ===', c, b, Basis(n, 1<<b), a
  #print 'LetterMul >>>', s, a
  return a

class Universe(object):
  
  def __init__(self, n):
    self.byName = {}
    self.byVec = {}
    one = Basis(n, 0)
    logn = int(0.5 + math.log(n, 2))

    def Inner(i, s):
      #print "INNER(%d, %s)" % (i, s)
      if i == logn:
        vec = LetterMul(s, one)
        if s=="": s = '1'
        s = s.replace('d', 'x')
        s = s.replace('e', 'y')
        self.byName[s] = vec
        self.byVec[tuple(vec)] = s
      else:
        Inner(i+1, s)
        Inner(i+1, s + Chr(i))

    Inner(0, "")

  def NameOfVec(self, vec):
    t = tuple(vec)
    s = self.byVec.get(t)
    if s:
      return s
    t = tuple([-x for x in vec])
    s = self.byVec.get(t)
    if s:
      return '-%s' % s
    raise Exception("Cannot find vec: %s" % vec)

  def VecOfName(self, s):
    if s != "1" and s != "-1":
      s = s.replace('1', '')
    #print "LOOK FOR", s
    vec = self.byName.get(s)
    if vec:
      return vec
    if s.startswith('-'):
      s = s[1:]
    else:
      s = '-%s' % s
    #print "  OR LOOK FOR", s
    vec = self.byName.get(s)
    if vec:
      return [-x for x in vec]
    raise Exception("Cannot find name: %s" % s)

  def Mul(self, s, t):
    vec = mul(self.VecOfName(s), self.VecOfName(t))
    return self.NameOfVec(vec)

  def Dump(self):
    for k, v in sorted(self.byName.items()):
      print "%10s : %s" % (k, v)

pass
