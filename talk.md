Original title:

# Trans-Sedenion Meditation with the Moufang Clan

(Contains 0% real Moufang Loops.)

Actual topic:

## Three Discoveries in Multiplying Trigintaduonion Bases, and an Application.

by Henry Strickland, 2016, for 
[G4G12](http://gathering4gardner.org/)  

Main web page: http://wiki.yak.net/1093

## My Discoveries

* Annihilating-Leapfrog Identity
* Letter-Gap Symmetry
* Multiplying by Dissociate-Then-Fix


## My Application: a Hyper-Complex C*ndyl*and game.

Instead of taking whole number steps from START to FINISH,
our board positions are trigintaduonion numbers,
and we multiply (instead of add) steps to get from 1 to FINISH. 

* Multiplayer board game: "Cayley-Dickson Trans-Sedenion Hyper-Complex C*nadyl*and"
* (Solitaire game web page)[http://wiki.yak.net/1093/solitaire.html]

## Hyper-Complex Summary

```
 num         num     num
 real  imagimary   total
 dims       dims    dims    Name
 ----       ----    ----    -----------------
    1         0        1    Real Numbers
    1         1        2    Complex Numbers
    1         3        4    Quaternions
    1         7        8    Octonions
    1        15       16    Sedenions
    1        31       32    Trigintaduonions
    1    (2^n)-1     2^n    ...etc...
```

## How we will write the bases:
```
1 Real Number:
                 1
2 Complex Numbers:
                 1  a             ( We use "a" instead of "i". )
4 Quaternions:
                 1, a, b, ab     ( Instead of "i", "j", & "k". )
8 Octonions:
                 1, a, b, ab, c, ac, bc, abc
16 Sedenions:
                 1, a, b, ab, c, ac, bc, abc,
                 d, ad, bd, abd, cd, acd, bcd, abcd
32 Trigintaduonions:
                 1, a, b, ab, c, ac, bc, abc,
                 d, ad, bd, abd, cd, acd, bcd, abcd,
                 e, ae, be, abe, ce, ace, bce, abce,
                 de, ade, bde, abde, cde, acde, bcde, abcde
```


## Trigintaduonion Bases, I choose you!

From here on, we only use the Trigintaduonion Bases (and their negatives) for multiplication.

*But it would apply generally to any hyper-complex system.*

*Multiplication is defined by the usual Cayley-Dickson Construction*
*(see Wikipedia or "The Octonions" by John C. Baez [2001].)*

Canonically we write our imaginary bases with letters:

* in alphabetical order
* no duplicates

*Some are a single letter: they are like primary bases.*

*Some are multi-letter.  They are independant imaginary bases, but they are also the product of 2 or more single-letter bases.*

Our convention: Multiply Left-to-Right: "abcde" means "(((ab)c)d)e"

### Warnings:

* Not commutative ...... don't assume xy = yx. &nbsp; &nbsp; (But they are anti-commutative!  xy = -yx, unless x=y or x=&plusmn;1 or y=&plusmn;1.)
* Not associative ...... don't assume x(yz) = (xy)z. &nbsp; &nbsp; (But they are plus-or-minus associative! x(yz) = &plusmn;(xy)z.)
* Not Moufang ...... don't assume (zx)(yz) = z(xy)z.
* Not alternative ...... don't assume x(xy) = (xx)y.

### The good news:

The set of 32 bases and their 32 negatives is closed under multiplication.

Multiplying by 1 and -1 work as we want (on left or right).  Two -1's cancel.

Multiplying any basis (except 1) by itself gives -1 (that is, the letter bases are all imaginary).


# Annihilating-Leapfrog Identity

*As you discovered in the Solitaire Game.*

But it only works for a single-letter multiplier!

Examples:
```
        acx(b)  =  a (b) -c -x  =  --abcx  =  abcx
```
To alphabetize, the (b) jumps over x and then c, producing a minus each time.
```
        acx(c)  =  a  c(c) -x  =  a (-) -x  =  --ax  =  ax
```
To alphabetize, the \(c) jumps over x, producing a minus.
Then it annihilates with the other c, producing a second minus.

You end up with the product in canonical form: alphabetized and no duplicates.

*Jump the multiplier over letters from right to left, until it is in alphabetical order,*
*adding a minus sign every time you leap.*

*Then repeated letters annihilate and become a minus sign.*



# Letter-Gap Symmetry

*(Related to index-cycling & index-doubling, but different.)*

Suppose you already know
```
        abc(ac) = -b
```
but you now want to know what is
```
        bde(be) = ?
```
You can reassign letters (introduce or remove gaps) with lines
from old to new letters, but do not cross the lines!
```
        a b c d e      abc(ac) = -b
         \ \ \         ||| ||     |
          | \ \        ||| ||     |
          |  \ \       ||| ||     |
        a b c d e      bde(be) = -d
```
If you cross the lines, you might prove that "ab = ba" which is wrong!



# Multiplying by Dissociate-Then-Fix

Below is a Twist Table for multiplying trigintaduonion bases:
it's gray if the product is negative.

Below that is another Twist Table, for fixing "Dissociations":
it's gray if the dissociation is the negative of the product.

The second Twist Table looks simpler than the first, so we prefer to use it instead.

Dissociating is my name for removing parentheses.
Remember that multiplication is not associative, so this can change the result,
so we have to fix it later.

Say you want to multiply *bcd* by *de*.  Drop the parentheses,
and use the Annihilating Leapfrog technique to absorb these extra letters
and canonicalize the result:
```
        bce(de)
        bce d e   ; dissociate d & e
        -bcde e     ; leapfrog the d (producing a minus)
        -bcd(-)       ; annihilate the e (producing another minus)
        bcd           ; cancel the minuses
```
However this is not the final answer, because dissociating is not safe.

But we can look up the entry for "bcd" & "de" in the Dissociating Twist Table,
and we get -1.   So we multiply the entire result by it:
```
        (-1) bcd  =  -bcd
```
and that will be correct.

*The Advanced Card Deck for the Game uses this technique to multiply by*
*multi-letter bases, without the full complexity of the Multiplication Twist Table.*


