import sys

def Log2(n):
  if n != int(n):
    raise Exception("Not an int: %g" % n)
  if n == 1:
    return 0
  else:
    return Log2(n / 2.0)+1
assert Log2(1) == 0
assert Log2(2) == 1
assert Log2(4) == 2
assert Log2(64) == 6

NUMERIC = [int, long, float]
def scalar(x):
  return type(x) in NUMERIC

def add(x, y):
  if scalar(x) and scalar(y):
    return x + y
  else:
    return tuple([xe + ye for xe, ye in zip(x, y)])

def sub(x, y):
  if scalar(x) and scalar(y):
    return x - y
  else:
    return tuple([xe - ye for xe, ye in zip(x, y)])

def neg(x):
  if scalar(x):
    return -x
  else:
    return tuple([-e for e in x])

def conj(x):
  #print "conj <<", x
  if scalar(x):
    z = x
  elif len(x) == 2:
    a, b = x
    z = (a, -b)
  else:
    a, b = split(x)
    z = conj(a) + neg(b)  # List add.
  #print "conj >>", z
  return z

def split(x):
  h = len(x) / 2
  return tuple(x[:h]), tuple(x[h:])

# Mathemetician's multiply:
#   multiplier is on the left (x).
# Backwards of what we show the users.
MUL_CACHE = {}
def mul(x, y):
  if scalar(x) and scalar(y):
    return x * y

  cache_key = (x, y)
  cached = MUL_CACHE.get(cache_key)
  if cached:
    return cached

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
    z = tuple([left, right])
  else:
    z = tuple(left + right)  # List add.
  MUL_CACHE[cache_key] = z
  return z

assert add(3, 4) == 7
assert add([10, 11], [20, 22]) == (30, 33)
assert sub([10, 11], [20, 22]) == (-10, -11)
assert conj(4) == 4
assert conj([55, 66]) == (55, -66)

def TestQuaternions():
  Q0, Q1 = (0, 0, 0, 0), (1, 0, 0, 0)
  Qi, Qj, Qk = (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)

  assert neg(Q0) == (0, 0, 0, 0)
  assert neg(Q1) == (-1, 0, 0, 0)

  # Test multQiplyQing by 0.
  assert mul(Q0, Qi) == Q0
  assert mul(Q0, Qj) == Q0
  assert mul(Q0, Qk) == Q0
  assert mul(Qi, Q0) == Q0
  assert mul(Qj, Q0) == Q0
  assert mul(Qk, Q0) == Q0

  # Test multQiplyQing by 1.
  assert mul(Q1, Qi) == Qi
  assert mul(Q1, Qj) == Qj
  assert mul(Q1, Qk) == Qk
  assert mul(Qi, Q1) == Qi
  assert mul(Qj, Q1) == Qj
  assert mul(Qk, Q1) == Qk

  # Test rocQk-paper-scQissors wQith Qi, Qj, Qk.
  if 0:
    assert mul(Qi, Qj) == Qk
    assert mul(Qj, Qk) == Qi
    assert mul(Qk, Qi) == Qj
    assert mul(Qj, Qi) == neg(Qk) == (0, 0, 0, -1)
    assert mul(Qk, Qj) == neg(Qi) == (0, -1, 0, 0)
    assert mul(Qi, Qk) == neg(Qj) == (0, 0, -1, 0)
TestQuaternions()

def BasisVec(n, i):
  vec = n * [0] 
  vec[i] = 1
  return tuple(vec)

def DecodeUnitVector(vec):
  assert 1 == sum([e != 0 for e in vec])
  assert 1 == sum([e in [1, -1] for e in vec])
  if vec[0]==1:
    return "1"
  if vec[0]==-1:
    return "-1"

  sign = sum(vec)
  assert sign==1 or sign==-1
  i = abs(sum([x*y for x,y in zip(vec, range(len(vec)))]))
  assert 0 <= i < len(vec)

  s = ''
  c = ord('a')
  while i > 0:
    if i & 1:
      s += chr(c)
    i >>= 1
    c += 1

  return "%s%s" % (('-' if sign<0 else ''), s)

def TestOctonions():
  # Build the octonions.
  K = [BasisVec(8, i) for i in range(8)]
  K0 = tuple(8 * [0])
  K1 = K[0]
  Kminus1 = tuple(-e for e in K1)

  for i in range(8):
    #print "Octonion Basis #%d: %s" % (i, K[i])
    assert K[i] == mul(K1, K[i])  # test mult by 1
    assert K[i] == mul(K[i], K1)  # test mult by 1
    assert K0 == mul(K[i], K0)    # test mult by 0
    assert K0 == mul(K0, K[i])    # test mult by 0
    assert neg(K[i]) == mul(Kminus1, K[i])  # test mult by -1
    assert neg(K[i]) == mul(K[i], Kminus1)  # test mult by -1

  def CheckOctonions():
    for i in range(8):
      #print
      for j in range(8):
        prod = mul(K[i], K[j])
        #print "Octonion #%d x #%d = %s" % (i, j, prod)
        # Check that units are closed under mul:
        #   -- Exactly 1 member of prod is nonzero.
        assert 1 == sum([e != 0 for e in prod])
        #   -- Exactly 1 member of prod is 1 or -1.
        assert 1 == sum([e in [1, -1] for e in prod])

        if i == j:  # If a basis is multiplied by itself,
          if i == 0:
            # -- Real basis squares to be 1.
            assert (1, 0, 0, 0, 0, 0, 0, 0) == prod
          if i > 1:
            # -- Imaginary bases square to be -1.
            assert (-1, 0, 0, 0, 0, 0, 0, 0) == prod
        elif i>0 and j>0:
          # If not multiplied by itself, and neither is 1, check anti-commutativity.
          backwards_prod = mul(K[j], K[i])  # Multiplied backwards.
          assert neg(prod) == backwards_prod, (i, j, K[i], K[j], prod, backwards_prod)
  CheckOctonions()
TestOctonions()

def TestNions(n):
  # Build the basis vectors N.
  N = [BasisVec(n, i) for i in range(n)]
  Zero = tuple(n * [0])
  One = N[0]
  MinusOne = neg(One)

  for i in range(n):
    #print "%dNion Basis #%d: %s" % (n, i, N[i])
    assert N[i] == mul(One, N[i])  # test mult by 1
    assert N[i] == mul(N[i], One)  # test mult by 1
    assert Zero == mul(N[i], Zero)    # test mult by 0
    assert Zero == mul(Zero, N[i])    # test mult by 0
    assert neg(N[i]) == mul(MinusOne, N[i])  # test mult by -1
    assert neg(N[i]) == mul(N[i], MinusOne)  # test mult by -1

  def CheckNions():
    for i in range(n):
      #print
      for j in range(n):
        prod = mul(N[i], N[j])
        backwards_prod = mul(N[j], N[i])  # Multiplied backwards.
        #print "%dNion #%d x #%d = %s" % (n, i, j, prod)

        # Check that units are closed under mul:
        #   -- Exactly 1 member of prod is nonzero.
        assert 1 == sum([e != 0 for e in prod])
        #   -- Exactly 1 member of prod is 1 or -1.
        assert 1 == sum([e in [1, -1] for e in prod])

        # Check type of associativity.
        for k in range(n):
          left = mul(prod, N[k])
          right = mul(N[i], mul(N[j], N[k]))
          if n < 8:
            # Must be associative.
            assert left==right, (i, j, k, left, right)
          else:
            # Must be plus-or-minus associative.
            assert left == neg(right) or left==right, (i, j, k, left, right)
            #if left == (right):
              #print 'ASSOC: %s, %s, %s' % (i, j, k)
            #if left == neg(right):
              #print 'ANTI: %s, %s, %s' % (i, j, k)

          # Check alternative property.
          if i==j or j==k or k==i:
            assert left==right, (i, j, k, left, right, 'Alternative?')
            

        if i == j:  # If a basis is multiplied by itself,
          if i == 0:
            # -- Real basis squares to be 1.
            assert One == prod
          if i > 1:
            # -- Imaginary bases square to be -1.
            assert MinusOne == prod
        elif i>0 and j>0:
          # If not multiplied by itself, and neither is 1, check anti-commutativity.
          assert neg(prod) == backwards_prod, (i, j, N[i], N[j], prod, backwards_prod)

                    
  CheckNions()

TestNions(2)
TestNions(4)
TestNions(8)
TestNions(16)
TestNions(32)
#TestNions(64)
#TestNions(128)

def Brief(vec):
  return ''.join(['1' if e==1 else '-' if e==-1 else '.' if e==0 else '?' for e in vec])

def UnitNames(alphabet):
  def Inner(s):
    if len(s) == 1:
      yield ''
      yield s
    else:
      for e in Inner(s[1:]):
        yield e
        yield s[0]+e
  return list((e if e else '1') for e in Inner(alphabet))
  return sorted((e if e else '1') for e in Inner(alphabet))

def AssignNames(D, T, N, alphabet):
  n = len(N)
  def LeftToRight(s):
    x = N[0]
    #print 'LeftToRight(%s):' % s
    for c in s:
      if c == '1':
        pass
      elif c == '-':
        x = neg(x)
      else:
        f = D[c]
        x = mul(f, x)
        #print 'LeftToRight: %s -> f = %s -> x = %s' % (c, f, x)
    #print 'LeftToRight(%9s) = %s' % (s, Brief(x))
    return x

  b = 1
  i = 0
  while b < n:
    c = alphabet[i]
    vec = BasisVec(n, b)
    D[c] = vec
    T[vec] = c
    b <<= 1
    i += 1

  for s in UnitNames(alphabet):
    vec = LeftToRight(s)
    D[s] = vec
    T[vec] = s
    D['-' + s] = neg(vec)
    T[neg(vec)] = '-' + s

  return LeftToRight

def Alphabet(n):
  ALFA = 'abcxyzpqrstuv'
  ALFA = 'abcdefghijklmnopqrstuvwxyz'
  s = ''
  b = 1
  i = 0
  while b < n:
    s += ALFA[i]
    b <<= 1
    i += 1
  return s

#def PrintAbsoluteTable(n, ht):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  print >>ht, '<html><body><table border=1>'
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#    print >>ht, '<tr>'
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      prod = mul(b, a)  # Proper multiplication.
#      tprod = T[prod]
#      if tprod.startswith('-'):
#        print >>ht, '<td bgcolor="grey">', tprod
#      else:
#        print >>ht, '<td>', tprod
#  print >>ht, '</table><br>'
#  
#
#def Calculate(n, *v):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  m = N[0]  # The One Element.
#  for e in v:
#    m = mul(D[e], m)
#    print '  %s' % T[m]
#  #print '%s . %s = %s' % (a, b, T[m])
#  pass
#
#
#
#def SingleLetterMoves(n):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  print '============= Single Letter Moves: n=', n
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#
#    print
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      if j == 0 or len(tb) != 1: continue
#
#      m = mul(b, a)
#      tm = T[m]
#      print 'From Cell', ta, ' Times ',tb, 'Moves To', tm
#
#def DoubleLetterMoves(n):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  print '============= Single Letter Moves: n=', n
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#
#    print
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      if len(tb) != 2: continue
#
#      m = mul(b, a)
#      tm = T[m]
#      print ta, '.', tb, '=', tm
#
#def SingleLetterAssociativeCheck(n):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  print '============= SingleLetterAssociativeCheck: n=', n
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#
#    print
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      if j == 0 or len(tb) != 1: continue
#
#      m = mul(b, a)
#      tm = T[m]
#      #print ta, tb, tm
#
#      # Conjecture: count moves until multiplier is in place, then anihilate.
#      jumps = sum([(e > tb) for e in ta])
#      if jumps:
#        tp = ta[:-jumps] + tb.upper() + ta[-jumps:]
#      else:
#        tp = ta + tb.upper()
#      print ta, tb, jumps, tp, '......', tm
#
#      anihilate = 0
#      after = tp
#      for k in range(len(tp)-1):
#        if tp[k].lower() == tp[k+1].lower():
#          after = "" + tp[:k] + tp[k+2:]
#          anihilate += 1
#          break
#      strikes = anihilate + jumps
#      print ta, tb, jumps, tp, '......', anihilate, after, strikes, '...', tm
#
#      # Test our conjecture:  odd strikes implies
#      assert (0 != ((strikes) & 1)) == tm.startswith('-'), (anihilate, jumps, tm)
#
#          
#def MultiLetterMultiply(n):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#
#    print
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      if j == 0: continue
#
#      m = mul(b, a)
#      tm = T[m]
#      print '%8s %8s %8s' % (ta, tb, tm)
#
#
#if 0:
#  Calculate(32, *sys.argv[1:])
#  sys.exit(0)
#  DoubleLetterMoves(32)
#  sys.exit(0)
#  SingleLetterMoves(32)
#  # sys.exit(0)
#  MultiLetterMultiply(32)
#  # sys.exit(0)
#
#
## for n in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:  #  But not 128!
## for n in [2, 4, 8, 16, 32, 64, 128]:
#for n in [2, 4, 8, 16, 32, 64]:
#  SingleLetterAssociativeCheck(n)
## sys.exit(0)
#
#def AssociativeCheck(n, l1=2, l2=2, l3=2):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#
#  print '============= AssociativeCheck: n=', n
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#    if len(ta) != l1: continue
#
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      if len(tb) != l2: continue
#
#      for k in range(n):
#        c = N[k]
#        tc = T[c]
#        if len(tc) != l3: continue
#
#        # (a * b) * c
#        left = mul(c, mul(b, a))
#        # a * (b * c)
#        right = mul(mul(c, b), a)
#
#        if left == right:
#          print 'okay: (%s * %s) * %s == %s * (%s * %s) == %s' % (ta, tb, tc, ta, tb, tc, T[left])
#        elif left == neg(right):
#          print 'NEG : (%s * %s) * %s == neg( %s * (%s * %s)) == %s  ... %s * %s = %s ... %s * %s = %s' % (ta, tb, tc, ta, tb, tc, T[left],
#                    ta, tb, T[mul(b, a)],
#                    tb, tc, T[mul(c, b)],
#                    )
#        else:
#          raise Exception( 'DIFF: %s = (%s * %s) * %s != %s * (%s * %s) = %s' % (T[left], ta, tb, tc, ta, tb, tc, T[right]) )
#
#AssociativeCheck(32, 2, 1, 1)
#sys.exit(0)
#
#
#def PrintTable(n, ht=None, only=None, candy=None):
#  alfa = Alphabet(n)
#  N = [BasisVec(n, i) for i in range(n)]
#  D, T = {}, {}
#  left2right = AssignNames(D, T, N, alfa)
#  candyTmp = {}
#
#  print '============================='
#  print '====   Table n = %d' % n
#  if ht: print >>ht, '<html><body><table border=1>'
#  Right = dict([(i, 0) for i in range(n)])
#  Wrong = dict([(i, 0) for i in range(n)])
#  # Pink for wrong, lightgreen for right.
#  for i in range(n):
#    a = N[i]
#    ta = T[a]
#    if ht: print >>ht, '<tr> <!-- %s -->' % repr((i, a, T[a]))
#    print
#    for j in range(n):
#      b = N[j]
#      tb = T[b]
#      if only:
#        #print (n, i, j, tb, only), tb in only
#        if j!=0 and tb not in only:
#          continue
#      prod = mul(b, a)  # Proper multiplication.
#      jam = N[0]        # Jamming multiplication.
#      for c in T[a] + T[b]:
#        if c == '-':
#          jam = neg(jam)
#        else:
#          jam = mul(D[c], jam)
#      print '%6s  * %6s  = %6s  [ %s ]  %s' % (T[a], T[b], T[prod], T[jam], prod == jam)
#      assert prod == jam or prod == neg(jam)
#      Right[j] += int(prod == jam)
#      Wrong[j] += int(prod != jam)
#
#      if ht: print >>ht, '<td bgcolor="%s"> %s <!-- %s -->' % (
#          'lightgreen' if prod==jam else 'pink',
#          T[prod],
#          repr((j, b, T[b])))
#
#      if candy:
#        for k, v in candy.items():
#          print k, v, tb, prod, jam, candyTmp
#          if tb in v and prod != jam:
#            candyTmp[k] = candyTmp.get(k, {})
#            candyTmp[k][ta] = candyTmp[k].get(ta, [])
#            candyTmp[k][ta].append(tb)
#
#  if ht: print >>ht, '<tr>'
#  # The right/wrong count.
#  for j in range(n):
#    b = N[j]
#    tb = T[b]
#    if only:
#      if j!=0 and tb not in only:
#        continue
#    if ht: print >>ht, '<th %s>%d,%d' % (
#        ' bgcolor="gray" ' if Right[j]==16 else '',
#        Right[j],
#        Wrong[j])
#  if ht: print >>ht, '<tr>'
#  # Repeat the column header as a footer.
#  for j in range(n):
#    b = N[j]
#    tb = T[b]
#    if only:
#      if j!=0 and tb not in only:
#        continue
#    if ht: print >>ht, '<th>%s' % T[N[j]]
#  if ht: print >>ht, '</table><br>'
#
#  if candy:
#    print 'candyTmp=', candyTmp
#    for k, v in candyTmp.items():
#      print k
#      print v
#
#    for label, count in [(k, len(v)) for k, v in candy.items()]:
#      allWrong = []
#      for k, v in candyTmp[label].items():
#        if len(v) == count: allWrong.append(k)
#      print label, len(allWrong), sorted(allWrong)
#
#      uniques = dict([(k, []) for k in candy[label]])
#      for k, v in candyTmp[label].items():
#        if k not in allWrong:
#          for v9 in v:
#            uniques[v9].append(k)
#
#      print label, '======', uniques
#pass
#
#PrintTable(16)
#
#CANDY = dict(cane=['axy', 'bxy', 'cxy'],
#             pop=['acx', 'bcx'],
#             taffy=['acy', 'bcy'])
#
#ht = open('1.html', 'w')
#PrintAbsoluteTable(32, ht=ht)
##PrintTable(32, ht=ht)
#PrintTable(32, ht=ht,
#           only=['axy', 'bxy', 'cxy',  'acx', 'bcx',  'acy', 'bcy'],
#           candy=CANDY)
#ht.close()
#
#
#print "OKAY"
#sys.exit(0)
##PrintTable(64)
#pass
#  #################################################################
##
##  print
##  for j in range(n):  # The move.
##    b = N[j]
##    print
##    nsame, ndiff = 0, 0
##    diffOrig, sameOrig = [], []
##    diffDest, sameDest = [], []
##    for i in range(n):  # The start cell.
##      a = N[i]
##      prod = mul(b, a)
##      end = T[prod]
##      end = end[1:] if end.startswith('-') else end
##      print '%6s  * %6s  = %6s' % (T[a], T[b], T[prod])
##      #print '%6s  * %6s  = %6s' % (a, b, prod)
##
##      # Now try the move step by step.
##      prod2 = a
##      steps = T[b]
##      for c in steps:
##        m = left2right(c)
##        prod2 = mul(m, prod2)
##
##      if prod2 == prod:
##        print 'CARD %6s * %6s = %6s: Same.' % (T[a], steps, T[prod])
##        nsame += 1
##        sameOrig.append(T[a])
##        sameDest.append(end)
##      elif prod2 == neg(prod):
##        print 'CARD %6s * %6s = %6s: NEGATED.' % (T[a], steps, T[prod])
##        ndiff += 1
##        diffOrig.append(T[a])
##        diffDest.append(end)
##      else:
##        raise Exception('What %s Versus %s' % (prod, prod2))
##    print '%d_ORIG Same %d Diff %d  [ %s ] %s' % (len(T[b]), nsame, ndiff, T[b], sorted(sameOrig))
##    print '%d_DEST Same %d Diff %d  [ %s ] %s' % (len(T[b]), nsame, ndiff, T[b], sorted(sameDest))
##
##  print
##  powers = []
##  p = 1
##  while p < n:
##    powers.append(p)
##    p <<= 1
##  print powers
##  for i in range(n):
##    a = N[i]
##    print
##    for j in powers:
##      b = N[j]
##      prod = mul(b, a)
##      print '%6s  * %6s  = %6s' % (T[a], T[b], T[prod])
##      #print '%6s  * %6s  = %6s' % (a, b, prod)
##  print '============================='
#
##################################################################
##################################################################
##################################################################
#
#def ReverseString(s):
#  v = [c for c in s]
#  v.reverse()
#  return ''.join(v)
#
##bad	#################################################################
##bad	
##bad	def cons(a, b):
##bad	  assert type(b) is list, b
##bad	  return [a] + b
##bad	def head(a):
##bad	  assert type(a) is list, a
##bad	  return a[0]
##bad	def tail(a):
##bad	  assert type(a) is list
##bad	  return a[1:]
##bad	def split(a):
##bad	  assert type(a) is list, a
##bad	  assert a, a
##bad	  return head(a), tail(a)
##bad	def null(a):
##bad	  return type(a) is list and not a
##bad	def atom(a):
##bad	  return type(a) is not list
##bad	  
##bad	# Expr will mult math style, multipler on left.
##bad	# abcde means [e [d [c [b [a []]]]]]
##bad	# -abcde means [e [d [c [b [a [- []]]]]]]
##bad	def strToExpr(s):
##bad	  x = 1
##bad	  for c in s:
##bad	    x = [c, x]
##bad	  return x
##bad	def multExprs(b, a):
##bad	  return [b, [a, 1]]
##bad	# Simplify means turn [[A B] C] into [- [A [B C]]]]
##bad	def simplifyExprs(x):
##bad	  if not atom(x) and len(x):
##bad	    left, c = split(x)
##bad	    left = simplifyExprs(left)
##bad	    c = simplifyExprs(c)
##bad	    if not atom(left) and len(left):
##bad	      a, b = split(left)
##bad	      a = simplifyExprs(a)
##bad	      b = simplifyExprs(b)
##bad	      return ['-', a, b, c]
##bad	    return cons(left, c)
##bad	  return x
##bad	
##bad	a1 = strToExpr('abcd')
##bad	a2 = strToExpr('-abcd')
##bad	assert a1 = ['a', 'b', 'c', 'd']
##bad	assert a2 = ['-', 'a', 'b', 'c', 'd']
##bad	assert a1 == simplifyExprs(a1) 
##bad	assert a2 == simplifyExprs(a2) 
##bad	  
##bad	
##bad	#################################################################
#
#if 0:
#  def LettersToCons(s):
#    z = None
#    flip = 0
#    for c in ReverseString(s):
#      if c == '-':
#        flip += 1
#      elif c == '1':
#        pass
#      else:
#        z = (c, z)
#    return z, flip
#
#  def ConsMultiply((a, f1), (b, f2)):
#    return (a, (b, None)), int(f1)+int(f2)
#
#  def Canonical(a):
#    print '<<<', repr(a)
#    if type(a) is tuple:
#      l, r = a
#      assert l is not None
#      l, f0 = Canonical(l)
#      assert l is not None
#      r, f1 = Canonical(r)
#      if type(l) is tuple:
#        p, q = l
#        assert p is not None
#        p, f2 = Canonical(p)
#        assert p is not None
#        q, f3 = Canonical(q)
#
#        if q is None:
#          pass
#          z = (p, (q, r)), 1+f0+f1+f2+f3
#        else:
#          pass
#          z = (p, (q, r)), 1+f0+f1+f2+f3
#      else:
#        z = (l, r), f0+f1
#    else:
#      z = a, 0
#
#    z1, z2 = z
#    print '>>>', repr(z1), '[%d]' % z2
#    return z
#
#  if 0:
#    print LettersToCons('-fruitcake')
#    z, f = ConsMultiply(LettersToCons('-abc'), LettersToCons('-xy'))
#    print z, f
#
#    z, f = Canonical(z)
#    print z, f
#    while f:
#      z, f = Canonical(z)
#      print z, f
#
#    def LetterPredict(s, t):
#      pass
#    
#
#
#  #PrintTable(4)
#  #PrintTable(8)
#  #PrintTable(16)
#  PrintTable(32)
#
#
#  ## Generate n-ions: first the 0, then the n bases.
#  #def GenerateNions(n):
#  #  return n * [0], [BasisVec(n, i) for i in range(n)]
#  #
#  #def TestNions(n):
#  #  Zero, V = GenerateNions(n)
#  #  One = V[0]
#  #  MinusOne = neg(One)
#  #
#  #  for i in range(n):
#  #    print "%d-ions %d: %s" % (n, i, V[i])
#  #    assert V[i] == mul(One, V[i])
#  #    assert V[i] == mul(V[i], One)
#  #    assert Zero == mul(V[i], Zero)
#  #    assert Zero == mul(Zero, V[i])
#  #
#  #  for i in range(n):
#  #    print
#  #    for j in range(n):
#  #      print "Octonion %d x %d = %s" % (i, j, mul(V[i], V[j]))
#  #      assert 1 == sum([e != 0 for e in mul(V[i], V[j])])
#  #      assert 1 == sum([abs(e) == 1 for e in mul(V[i], V[j])])
#  #      if i > 0 and i == j:
#  #        assert MinusOne == mul(V[i], V[j])
#  #
#  ##TestNions(2)
#  ##TestNions(4)
#  ##TestNions(8)
#  ##TestNions(16)
#  ##TestNions(32)
#  ##TestNions(64)
#  #
#  #def Chr(b):
#  #  return chr(97+b)
#  #
#  #def MustBeAUnit(vec):
#  #  assert 1 == sum([x != 0 for x in vec])
#  #  assert 1 == sum([x in [-1, 1] for x in vec])
#  #
#  #def Name1(vec):
#  #  # This function only works if only 1 basis is nonzero.
#  #  MustBeAUnit(vec)
#  #
#  #  s = str(sum(vec))
#  #  n = len(vec)
#  #  logn = int(0.5 + Log2(n))
#  #  pos = -1
#  #  for i in range(n):
#  #    if vec[i]:
#  #      pos = i
#  #      break
#  #  assert pos >= 0
#  #    
#  #  for b in range(logn):
#  #    if pos & (1<<b):
#  #      s += Chr(b)
#  #  return s 
#  #
#  #def GameHints(n):
#  #  Zero, V = GenerateNions(n)
#  #  One = V[0]
#  #  MinusOne = neg(One)
#  #  logn = int(0.5 + Log2(n))
#  #  print "logn: %f -> %d" % (Log2(n), logn)
#  #
#  #  byName = {}
#  #  for i in range(n):
#  #    byName[Name1(V[i])] = V[i]
#  #
#  #  for name, a in sorted(byName.items()):
#  #    print
#  #    print "[ %s = %s ]" % (name, a)
#  #    for b in range(logn):
#  #      c = Chr(b)
#  #      bvec = BasisVec(n, 1<<b)
#  #      z = mul(a, bvec)
#  #      assert Name1(bvec) == "1"+c, (bvec, Name1(bvec), c)
#  #      print "  %s : %s => %s   %s" % (name, c, Name1(z), z)
#  #
#  #def GameWalk(game, n):
#  #  Zero, V = GenerateNions(n)
#  #  One = V[0]
#  #  MinusOne = neg(One)
#  #  logn = int(0.5 + Log2(n))
#  #  print "logn: %f -> %d" % (Log2(n), logn)
#  #
#  #  Goal = MinusOne
#  #  Choices = V
#  #  if game == 2:
#  #    Goal = V[n-1]
#  #    Choices = [V[1<<i] for i in range(logn)]
#  #
#  #  a = One
#  #  for i in range(10000):
#  #    r = random.randrange(len(Choices))
#  #    m = Choices[r]
#  #    a = mul(a, m)
#  #    print "%4d: [%2d] %-8s = %s" % (i, r, Name1(a), " ".join(["%2d" % e for e in a]))
#  #    if a == Goal: break
#  #  if a != Goal: raise Exception("Never Finished.")
#  #  return i
#  #
#  #def LetterMul(s, a):
#  #  n = len(a)
#  #  #print 'LetterMul <<<', s, a
#  #  for c in s:
#  #    b = ord(c) - ord("a")
#  #    a = mul(a, BasisVec(n, 1<<b))
#  #    #print 'LetterMul ===', c, b, BasisVec(n, 1<<b), a
#  #  #print 'LetterMul >>>', s, a
#  #  return a
#  #
#  #assert [0, 1, 0, 0] == LetterMul('a', [1, 0, 0, 0])
#  #assert [0, 0, 1, 0] == LetterMul('b', [1, 0, 0, 0])
#  #assert [-1, 0, 0, 0] == LetterMul('a', [0, 1, 0, 0])
#  #assert [0, 0, 0, 1] == LetterMul('b', [0, 1, 0, 0])
#  #assert [0, 0, 0, -1] == LetterMul('a', [0, 0, 1, 0])
#  #
#  #class Universe(object):
#  #  
#  #  def __init__(self, n):
#  #    self.byName = {}
#  #    self.byVec = {}
#  #    one = BasisVec(n, 0)
#  #    logn = int(0.5 + Log2(n))
#  #
#  #    def Inner(i, s):
#  #      #print "INNER(%d, %s)" % (i, s)
#  #      if i == logn:
#  #        vec = LetterMul(s, one)
#  #        if s=="": s = '1'
#  #        s = s.replace('d', 'x')
#  #        s = s.replace('e', 'y')
#  #        self.byName[s] = vec
#  #        self.byVec[tuple(vec)] = s
#  #      else:
#  #        Inner(i+1, s)
#  #        Inner(i+1, s + Chr(i))
#  #
#  #    Inner(0, "")
#  #
#  #  def NameOfVec(self, vec):
#  #    t = tuple(vec)
#  #    s = self.byVec.get(t)
#  #    if s:
#  #      return s
#  #    t = tuple([-x for x in vec])
#  #    s = self.byVec.get(t)
#  #    if s:
#  #      return '-%s' % s
#  #    raise Exception("Cannot find vec: %s" % vec)
#  #
#  #  def VecOfName(self, s):
#  #    if s != "1" and s != "-1":
#  #      s = s.replace('1', '')
#  #    #print "LOOK FOR", s
#  #    vec = self.byName.get(s)
#  #    if vec:
#  #      return vec
#  #    if s.startswith('-'):
#  #      s = s[1:]
#  #    else:
#  #      s = '-%s' % s
#  #    #print "  OR LOOK FOR", s
#  #    vec = self.byName.get(s)
#  #    if vec:
#  #      return [-x for x in vec]
#  #    raise Exception("Cannot find name: %s" % s)
#  #
#  #  def Mul(self, s, t):
#  #    vec = mul(self.VecOfName(s), self.VecOfName(t))
#  #    return self.NameOfVec(vec)
#  #
#  #  def Dump(self):
#  #    for k, v in sorted(self.byName.items()):
#  #      print "%10s : %s" % (k, v)
#  #
#  #def NewStrToVec(n, s):
#  #  pos = 0
#  #  sign = 1
#  #  z = n * [0]
#  #  for c in s:
#  #    if c == '-':
#  #      sign = -sign
#  #    elif c == '1':
#  #      pass
#  #    elif 'a' <= c and c <= 'z':
#  #      pos += 1 << (ord(c) - ord('a'))
#  #    else:
#  #      raise Exception('Weird char "%s" in str "%s"' % (c, s))
#  #  z[pos] = sign
#  #  return z
#  #
#  #
#  #def NewMulStr(n, xs, ys):
#  #  cc = [c for c in xs if c not in '-1'] + [c for c in ys if c not in '-1']
#  #  cc_negative = ('-' in xs) ^ ('-' in ys)
#  #  print xc, yc
#  #  x, y = NewStrToVec(n, p), NewStrToVec(n, q)
#  #  print x, y
#  #
#  #  flips = 0
#  #  # Ripple Sort, counting flips
#  #  for i in range(n-1):
#  #    for j in range(n-1):
#  #      if xc[i] > xc[j]:
#  #        xc[j], xc[i] = xc[i], xc[j]
#  #        flips += 1
#  #  print 
#  #
#  #def NewPredictMul(p, q):
#  #  raise 1
#  #
#  #GameHints(32)
#  #pass

def mu(a, b):  # Left-To-Right Multiply
  return mul(b, a)

def AntiCommutativeCheck(n):
  alfa = Alphabet(n)
  N = [BasisVec(n, i) for i in range(n)]
  D, T = {}, {}
  left2right = AssignNames(D, T, N, alfa)

  for i in range(n):
    x = N[i]
    tx = T[x]

    for j in range(n):
      y = N[j]
      ty = T[y]

      m1 = mul(x, y)
      m2 = mul(y, x)

      if i==0 or j==0 or i==j:
        assert m1 == m2
      else:
        assert m1 == neg(m2)

def MoufagClanCheck(n):
  alfa = Alphabet(n)
  N = [BasisVec(n, i) for i in range(n)]
  D, T = {}, {}
  left2right = AssignNames(D, T, N, alfa)

  for i in range(n):
    x = N[i]
    tx = T[x]

    for j in range(n):
      y = N[j]
      ty = T[y]

      # Alternate?
      # 0.  x(yx) = (xy)x
      l0 = mu(x, mu(y, x))
      r0 = mu(mu(x, y), x)
      m0 = (l0 == r0)
      assert m0

      for k in range(n):
        z = N[k]
        tz = T[z]

        # Moufang Laws -- Conway & Smith section 7.4
        # z(xy)z = (zx)(yz)  -- Bi-Moufang
        # z(x(zy)) = (z(xz))y  -- Left-Moufant
        # ((xz)y)z = x(z(yz))  -- Right-Moufant

        # Wikipedia "Moufang Loop"
        # 1. z(x(zy)) = ((zx)z)y  -- Left
        # 2. x(z(yz)) = ((xz)y)z  -- Right
        # 3. (zx)(yz) = (z(xy))z  -- Bi (left first)
        # 4. (zx)(yz) = z((xy)z)  -- Bi (right first)

        # 1. z(x(zy)) = ((zx)z)y
        l1 = mu(z, mu(x, mu(z, y)))
        r1 = mu(mu(mu(z, x), z), y)
        m1 = (l1 == r1)

        l2 = mu(x, mu(z, mu(y, z)))
        r2 = mu(mu(mu(x, z), y), z)
        m2 = (l2 == r2)

        l3 = mu(mu(z, x), mu(y, z))
        r3 = mu(mu(z, mu(x, y)), z)
        m3 = (l3 == r3)

        l4 = mu(mu(z, x), mu(y, z))
        r4 = mu(z, mu(mu(x, y), z))
        m4 = (l4 == r4)

        assert m3 == m4
        print m1, m2, m3



def MulOneTerm(n, term, ns=0):
  alfa = Alphabet(n)
  N = [BasisVec(n, i) for i in range(n)]
  D, T = {}, {}
  left2right = AssignNames(D, T, N, alfa)

  m = N[0]  # The 'one' element.
  for i in range(ns):
    m = neg(m)
  for c in term:
    if c == '-':
      m = neg(m)
    elif c == '1':
      m = m
    else:
      m = mul(D[c], m)
  return T[m]


def StrikeSort(term, ns=0):
  assert type(term) == str
  prev = ''
  accum = ''
  rest = term
  for i in range(len(term)):
    c = term[i]
    assert type(c) == str
    assert len(c) == 1

    if c == '-':
      zz, strikes = StrikeSort(accum + term[i+1:])
      #print '** [=-: StrikeSort(%s, %d) ==> %s, %d]' % (term, ns, zz, strikes+1+ns)
      return zz, strikes+1+ns

    if c == '1':
      zz, strikes = StrikeSort(accum + term[i+1:])
      #print '** [=1: StrikeSort(%s, %d) ==> %s, %d]' % (term, ns, zz, strikes+0+ns)
      return zz, strikes+0+ns

    if c == prev:
      # Doubled.
      zz, strikes = StrikeSort(accum[:-1] + term[i+1:])
      #print '** [eq: StrikeSort(%s, %d) ==> %s, %d]' % (term, ns, zz, strikes+1+ns)
      return zz, strikes+1+ns

    if c < prev:
      # Out of order.
      zz, strikes = StrikeSort(accum[:-1] + c + accum[-1] + term[i+1:])
      #print '** [lt: StrikeSort(%s, %d) ==> %s, %d]' % (term, ns, zz, strikes+1+ns)
      return zz, strikes+1+ns

    else:
      accum += c
      prev = c
  #print '** [OK: StrikeSort(%s, %d) ==> %s, %d]' % (term, ns, accum, ns)
  return accum, ns

def SimplifyJamming(t):
  z, strikes = StrikeSort(t)
  z = ('-%s' % z) if (strikes & 1) else z
  if z == '-':  z = '-1'
  if z == '':  z = '1'
  return z

def Signless(s):
  return s[1:] if s.startswith('-') else s

def NumRepeatedLetters(s, t):
  return sum(int(e in t) for e in s)

def TryJammingConjecture(n):
  alfa = Alphabet(n)
  N = [BasisVec(n, i) for i in range(n)]
  D, T = {}, {}
  left2right = AssignNames(D, T, N, alfa)

  for i in range(n):
    if i==0: continue
    a = N[i]
    ta = T[a]
    la = len(ta)

    print
    for j in range(n):
      if j==0: continue
      b = N[j]
      tb = T[b]
      lb = len(tb)
      #if tb != 'ac': continue
      if len(tb) != 2: continue

      m = mul(b, a)
      tm = T[m]
      tp = SimplifyJamming('%s%s' % (ta, tb))

      p1, p2, p3 = len(ta), len(tb), NumRepeatedLetters(ta, tb)
      parity = (p1 + p2 + p3) % 2
      print p1, p2, p3, '=', parity

      if tm == tp:
        ok = (parity == 0)
        print ok, 'JC=: %8s . %8s = %8s' % (ta, tb, tm)
      elif T[neg(m)] == tp:
        ok = (parity == 1)
        print ok, 'JC-: %8s . %8s = %8s' % (ta, tb, tm)
      else:
        assert False, (ta, tb, i, j, tm, tp)
        

def FullMultiplicationTable(n, trim=False, singleLetter=False):
  alfa = Alphabet(n)
  N = [BasisVec(n, i) for i in range(n)]
  D, T = {}, {}
  left2right = AssignNames(D, T, N, alfa)

  for i in range(n):
    if trim and i==0: continue
    a = N[i]
    ta = T[a]
    la = len(ta)
    if trim and la==1: continue

    if singleLetter: print
    for j in range(n):
      if trim and j==0: continue
      b = N[j]
      tb = T[b]
      lb = len(tb)
      if trim and lb==1: continue

      if trim and (tb == ta): continue
      if trim and (lb > la): continue
      if trim and (lb == la) and (tb > ta): continue

      if singleLetter and (lb!=1 or j==0): continue

      m = mul(b, a)
      tm = T[m]
      print '%8s . %8s = %8s' % (ta, tb, tm)

      if singleLetter:
        # Check the jamming rule for single-letter multipliers: just count the hops.
        sj = SimplifyJamming('%s%s' % (ta, tb))
        assert tm == sj

if __name__ == '__main__':
  cmd = sys.argv[1]
  args = sys.argv[2:]

  if cmd == 'StrikeSort':
    for arg in args:
      z, ns = StrikeSort(arg)
      print "** MulOneTerm(%s) = %s" % (arg, MulOneTerm(32, arg))
      print "** MulOneTerm(%s {%d}) = %s" % (z, ns, MulOneTerm(32, z, ns))
      print "****  %s: %s {%d}: %s" % (arg, z, ns, (z if (0 == (ns&1)) else '-%s' % z))

  elif cmd == 'J':
    TryJammingConjecture(32)
  elif cmd == 'M':
    MoufagClanCheck(int(args[0]))
  elif cmd == 'Mul':
    FullMultiplicationTable(int(args[0]))
  elif cmd == 'MulTrim':
    FullMultiplicationTable(int(args[0]), trim=True)
  elif cmd == 'MulSingle':
    FullMultiplicationTable(int(args[0]), singleLetter=True)
  elif cmd == 'AC':
    AntiCommutativeCheck(int(args[0]))
  else:
    raise Exception('Unknown command: %s' % (cmd))
