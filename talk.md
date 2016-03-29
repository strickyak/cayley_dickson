
# Trans-Sedenion Medtation with the Moufang Clan

### or

## Three Discoveries in Multiplying Trigintaduonion Bases

by Henry Strickland, 2016.

* Annihilating-Leapfrog Identity
* Letter-Gap Symmetry
* Multiplying by Dissociate-Then-Fix

## My Application: a C*ndyl*and game.

Instead of taking whole number steps from START to FINISH,
our board positions are trigintaduonion numbers,
and we multiply (instead of add) steps to get from 1 to FINISH. 

* Multiplayer board game: "Cayley-Dickson Trans-Sedenion Hyper-Complex C*nadyl*and"
* Solitare web page.

## Hyper-Complex Summary

<table>
<tr><td> real<br>dimensions <td> imaginary<br>dimensions <td> total<br>dimensions <td> Name
<tr><td>         1 <td>              0 <td>          1 <td> Real Numbers
<tr><td>         1 <td>              1 <td>          2 <td> Complex Numbers
<tr><td>         1 <td>              3 <td>          4 <td> Quaternions
<tr><td>         1 <td>              7 <td>          8 <td> Octonions
<tr><td>         1 <td>             15 <td>         16 <td> Sedenions
<tr><td>         1 <td>             31 <td>         32 <td> Trigintaduonions
</table>

## How we will write the bases:

### 1 Real Number
1
### 2 Complex Numbers
1, a
### 4 Quaternions
1, a, b, ab
### 8 Octonions
1, a, b, ab, c, ac, bc, abc
### 16 Sedenions
1, a, b, ab, c, ac, bc, abc, d, ad, bd, abd, cd, acd, bcd, abcd
### 32 Trigintaduonions
1, a, b, ab, c, ac, bc, abc, d, ad, bd, abd, cd, acd, bcd, abcd,
e, ae, be, abe, ce, ace, bce, abce, de, ade, bde, abde, cde, acde, bcde, abcde

## From here on, we use the Trigintaduonion Bases (and their negatives) for multiplication.

*But it would apply generally to any hyper-complex system.*

*Multiplication is defined by the usual Cayley-Dickson Construction*
*(see Wikipedia or "The Octonions" by John C. Baez [2001].)*

Our convention: Associate Left-to-Right: "abcde" means "(((ab)c)d)e"

Canonically we write our imaginary bases with letters:

* in alphabetical order
* no duplicates

### Warnings:

* Not commutative ...... don't assume xy = yx
* Not associative ...... don't assume x(yz) = (xy)z
* Not Moufang ...... don't assume (zx)(yz) = z(xy)z
* Not alternative ...... don't assume x(xy) = (xx)y

### The good news:

The set of 32 bases and their 32 negatives is closed under multiplication.

Multiplying by 1 and -1 work as we want (on left or right).

Also multiplying any basis (except 1) by itself gives -1 (that is, the letter bases are all imaginary).

Multiplying 1 or -1 by itself gives 1.  (They are real.)


# Annihilating-Leapfrog Identity

But it only works for a single-letter multiplier!

Examples:
```
        acx(b)  =  a (b) -c -x  =  --abcx  =  abcx

        acx(c)  =  a  c(c) -x  =  a (-) -x  =  --ax  =  ax
```

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

Here's a Twist Table for multiplying trigintaduonion bases:

LINK

Here's another Twist Table, for fixing "Dissociations":

LINK

Dissociating is my name for removing parentheses.
Remember we are not associative, so this can change the result,
so we have to fix it later.

Say you want to multiply *bcd* by *de*.  Drop the parentheses,
and use the Annihilating Leapfrog technique to absorb these extra letters
and canonicalize the result:
```
        bce(de)
        bce (d) (e)   ; dissociate d & e
        -bcde (e)     ; leapfrog the d (producing a minus)
        -bcd(-)       ; annihilate the e (producing another minus)
        bcd           ; cancel the minuses
```
However this is not the final answer, because dissociating is not safe.

But we can look up the entry for "bcd" & "de" in the Dissociating Twist Table,
and we get -1.   So we multiply the entire result by it:
```
        -bcd
```
and that will be correct.




