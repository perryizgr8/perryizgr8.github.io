#!/usr/bin/env python3
"""Independent finite development checks for docs/length-density-theorem.md."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
def reverse_fixed(n,base,width):
    out=0
    for _ in range(width):
        n,digit=divmod(n,base);out=base*out+digit
    if n:raise ValueError('input wider than specified word')
    return out

def cover_check(nvalue,hex_length,p):
    # This uses exact ratios and powers, independently of the proof's circle logs.
    h=format(nvalue,'x');dec=str(nvalue)
    k=0
    while 10**(k+1)<=16**p:k+=1
    assert k>=1 and k<=4*p and len(dec)>=k
    v=int(h[:p],16);prefix=int(dec[:k]);residue=reverse_fixed(v,16,p)
    assert reverse_fixed(prefix,10,k)%(2**k)==residue%(2**k)
    s=len(str(16**(hex_length-1)))-1
    theta=Fraction(16**(hex_length-1),10**s)
    exponent=(len(dec)-1)-s-k+1
    power=Fraction(10**exponent) if exponent>=0 else Fraction(1,10**(-exponent))
    a=Fraction(v,16**(p-1));b=Fraction(v+1,16**(p-1))
    # This is the unwrapped version of the particular arc containing the phase.
    lo=prefix*power/b;hi=(prefix+1)*power/a
    assert lo<=theta<=hi,(nvalue,p,k,lo,theta,hi)
    return k

def main():
    assert 2303**2>2303*1000+3*1000**2
    assert 16**49>10**59
    assert 2303**49<1000**49*2**59
    reversal_words=0
    for k in range(1,5):
        counts=Counter(reverse_fixed(n,10,k)%(2**k) for n in range(10**k))
        assert len(counts)==2**k and set(counts.values())=={5**k}
        reversal_words+=10**k
    previous2=previous=1;prefix_counts={1:1,2:1}
    for p in range(3,9):
        recurrence=previous+3*previous2
        actual=sum(1 for tail in product(range(4),repeat=p-1)
                   if all(not (a and b) for a,b in zip((1,*tail),(1,*tail)[1:])))
        assert actual==recurrence
        assert recurrence*1000**(p-1)<=2303**(p-1)
        prefix_counts[p]=actual;previous2,previous=previous,recurrence
    scanned=hits=cover_cases=0;examples=[]
    for n in range(2,9):
        half=(n+1)//2
        for prefix in range(16**(half-1),16**half):
            left=format(prefix,'x')
            text=left+ (left[:-1] if n%2 else left)[::-1]
            value=int(text,16);scanned+=1
            dec=str(value)
            if dec!=dec[::-1]:continue
            hits+=1
            if len(examples)<12:examples.append({'decimal':dec,'hex':text})
            for p in range(1,n//2+1):
                cover_check(value,n,p);cover_cases+=1
    assert hits>0 and cover_cases>0
    report={'integer_witnesses_verified':True,'reversal_words_checked':reversal_words,
            'nonadjacent_prefix_counts':prefix_counts,'generic_hex_palindromes_enumerated':scanned,
            'positive_decimal_hex_palindromes':hits,'positive_cover_inclusions':cover_cases,
            'positive_examples':examples,'note':'finite development checks; the density conclusions follow from the written proof'}
    path=ROOT/'length-density-validation.json';path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
