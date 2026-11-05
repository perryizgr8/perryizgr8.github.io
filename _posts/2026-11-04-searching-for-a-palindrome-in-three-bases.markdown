---
layout: post
title: "Searching for a palindrome in three number systems"
categories: projects maths
published: true
---
I asked Codex to find a number that reads the same forwards and backwards in decimal, binary, and hexadecimal. Each representation had to have at least two digits. Otherwise, numbers like 7 make the question rather boring.

It hasn't found one. The search has ruled out every possibility below `2^436`, using independently checked certificates. Along the way, it went from checking billions of numbers to rejecting whole branches, then to a proof draft about which lengths could contain an answer.

This post is about the things we learned while failing to find the number.

## The problem

A palindrome depends on how you write it. For example:

{% highlight text %}
585 in decimal
1001001001 in binary
249 in hexadecimal
{% endhighlight %}

The first two are palindromes. The third isn't. We want all three, without adding leading zeros to make them match.

[Rick Regan searched for these numbers in 2010](https://www.exploringbinary.com/in-search-of-decimal-binary-hexadecimal-palindromes/) and found no examples. His search covered all the relevant families through 32 hexadecimal digits, and two smaller families through 64. That gave us both a starting point and a useful baseline to reproduce.

I should also say how this work was done. Codex wrote the search programs, developed the pruning methods, and worked through the mathematical argument. I set the problem, suggested directions, and supplied the machine. This is an account of that collaboration, not a claim that I personally wrote all the code or independently verified a new theorem.

## Generate the right numbers

Regan's [analysis of binary/hexadecimal palindromes](https://www.exploringbinary.com/the-structure-of-binary-hexadecimal-palindromes/) gives a much better starting point than checking every integer. There are six possible first hexadecimal digits, and each permits a small alphabet for the remaining digits:

| First digit | Allowed interior digits |
| --- | --- |
| 1 | 0, 1 |
| 3 | 0, 3 |
| 5 or 7 | 0, 2, 5, 7 |
| 9 or F | 0, 6, 9, F |

Choose half the hexadecimal string from the appropriate alphabet, then mirror it. For odd lengths, don't copy the centre digit twice. This generates exactly the numbers that are palindromes in both binary and hexadecimal. The remaining question is whether any of them is a decimal palindrome.

The rule is neat because binary and hexadecimal are related: each hexadecimal digit represents four bits. Decimal doesn't line up with those four-bit blocks, which is where the trouble starts.

Even with this generator, there are 4,295,032,832 candidates at exactly 32 hexadecimal digits. The initial CPU and GPU implementations reproduced the complete search through that length and found nothing.

## More hardware, then less work

My machine has an RTX 3060 Ti. We got CUDA working through Docker and split the work into independent CPU and GPU jobs. That helped, but the number of candidates still grows exponentially. Eventually the proof files also became large enough that we moved completed results and live CPU output onto a spare HDD.

At some point I suggested using the fact that every even-length decimal palindrome is divisible by 11. That is a useful filter. It doesn't apply to odd decimal lengths, and being divisible by 11 certainly doesn't make a number a palindrome.

The bigger improvement came from [Eshed Schacham's binary/decimal palindrome search](https://ashdnazg.github.io/articles/22/Finding-Really-Big-Palindromes). Instead of generating every complete number, fix a prefix and ask whether *any* completion could work.

## The beginning tells us about the end

Fixing the first few hexadecimal digits also fixes the last few, because the hexadecimal string must be a palindrome.

The remaining completions lie between a smallest value `L` and a largest value `U`. If both bounds share a decimal prefix, every number in between shares it too. A decimal palindrome must end with the reverse of that prefix.

Now two different number systems are making demands on the same suffix.

Here is a small arithmetic example, separate from the actual palindrome tree. Suppose candidates lie between 1200 and 1299 and must be 1 modulo 16. Their decimal prefix is `12`, so a decimal palindrome would end in `21`:

{% highlight text %}
x = 1  (mod 16)
x = 21 (mod 100)
{% endhighlight %}

The simultaneous solutions are 321, 721, 1121, 1521, and so on. None lies in our interval. We can discard the entire branch.

The real search does this with powers of 16 and 10, using exact integer arithmetic and the Chinese remainder theorem. Sometimes the suffix requirements disagree immediately. Sometimes they agree, but the first simultaneous solution is already above `U`.

There is an important limitation here. An integer satisfying the congruences may still have illegal hexadecimal digits. An interval is a very loose description of the remaining middle of the number.

## Remember the missing digits

For the family beginning with 5, the middle digits must come from `0, 2, 5, 7`. There is a convenient way to write those choices:

{% highlight text %}
digit = 2*b + 5*c, where b and c are independently 0 or 1
{% endhighlight %}

Similarly, `0, 6, 9, F` can be written as `6*b + 9*c`. Once we include the mirrored place values, the unknown middle becomes a sum of fixed weights, each either selected or omitted:

{% highlight text %}
t = a_1*e_1 + ... + a_s*e_s, where every e_i is 0 or 1
{% endhighlight %}

The suffix calculation also tells us that `t` must equal a particular residue modulo some integer `M`. So the remaining problem is a modular subset sum, not an arbitrary integer in an interval.

This suggests a cheap certificate for rejecting a branch. Choose a multiplier `lambda` and signed coefficients `h_i` such that:

{% highlight text %}
h_i = lambda*a_i  (mod M)
{% endhighlight %}

Every legal choice of bits must then satisfy:

{% highlight text %}
sum(h_i*e_i) = lambda*t  (mod M)
{% endhighlight %}

But that sum is trapped between two explicit bounds: the sum of all negative `h_i`, and the sum of all positive `h_i`. If the required residue never occurs in that interval, no legal middle exists.

LLL lattice reduction helps find useful coefficients. It is doing the discovery work. Checking the resulting rejection only requires exact integer congruences and bounds. Both independent auditors check those again; they don't have to trust LLL's numerical calculations.

Lattice methods for integer knapsacks are established mathematics. Our work here was adapting them to this particular palindrome search, not inventing lattice reduction.

On one complete benchmark, covering the 80-digit hexadecimal family beginning with 5, the effect was:

| Method | Search nodes visited |
| --- | ---: |
| Previous CRT pruning, with checks of up to eight remaining integers | 16,180,545 |
| CRT plus modular lattice cuts | 2,539,417 |

That is about **6.4 times fewer nodes**, covering the same candidate set. The measured full GPU worker time, including the independent audit, went from about 37.24 seconds to 3.96 seconds. These were single runs with other workloads active, and reusable table discovery was excluded. The node counts are the stronger comparison; I wouldn't treat the timing ratio as a general speedup guarantee.

## How much have we actually ruled out?

The snapshot used for this post covers all six families at every hexadecimal length from 2 through 109. There were no matches. That excludes every qualifying integer below `2^436`.

Both scheduled batches have finished. The CPU batch stopped cleanly at its deadline, finishing around 11:35 IST on 4 November with no reported failures. The latest completed coverage is:

| Leading hexadecimal digit | Every length checked through |
| --- | ---: |
| 1 | 1000 |
| 3 | 1000 |
| 5 | 109 |
| 7 | 112 |
| 9 | 114 |
| F | 112 |

The GPU also completed the entire **113-digit family beginning with 5**. Its independent audit passed after a search visiting 2,448,728,317 nodes, again with no match. That result is beyond a gap: the 110-digit leading-5 family remains unfinished. Checking a later length does not fill an earlier one, so our complete all-family bound remains **109 hexadecimal digits**, or `2^436`.

The two smaller families, containing only `0/1` or `0/3`, were separately excluded through 1000 hexadecimal digits. That is not an all-family 1000-digit result. Unfinished branches are checkpointed for resumption; the completed batches are no longer searching.

Most of these candidates were never individually generated. The certificates partition the candidate space into checked leaves and rejected subtrees. A separate checker reconstructs each rejection and checks that the partition has no gaps or overlaps. A Python auditor is also available as a different implementation of the mathematics.

We also tested the pruning rules against deliberately reachable modular targets. Comparing two programs that both report an empty answer list is not enough to show that either one works.

The [evidence summary](https://github.com/perryizgr8/perryizgr8.github.io/blob/master/assets/palindrome-search/evidence-summary.json) records the fixed all-family snapshot, the latest family-specific status, and the benchmark. The large search certificates and full engine are not included with this post, so that summary alone is not a public reproduction of the complete exclusion bound. I am also not claiming a verified search record.

## What if there is no number?

After all this, I started feeling that we might never find it. Searching farther could mean finding an enormous first example, or spending forever looking for something that doesn't exist. An empty search doesn't distinguish those possibilities.

So I asked Codex to work towards a theorem instead.

The resulting argument is a **complete proof draft, internally checked but not externally reviewed**. Its novelty has not been established. Here is the main statement:

> Among the first `X` hexadecimal lengths, the proportion admitting a decimal palindrome from either the `0/1` or `0/3` hexadecimal-palindrome family tends to zero as `X` tends to infinity.

The density is about **lengths**. It is not merely saying that palindromic integers are rare among all integers, which we already knew.

It also doesn't say that the exceptional lengths stop. There could still be infinitely many of them, just as the squares form an infinite set of density zero.

## Why the density argument works

The starting point is the same prefix/suffix restriction we used in the search. Fix `p` hexadecimal prefix digits and consider a decimal prefix of `k` digits, with `10^k <= 16^p` and `k <= 4p`.

The reversed decimal prefix must match the hexadecimal suffix modulo `2^k`. Among all `10^k` fixed-width decimal words, exactly `5^k` have any specified residue modulo `2^k`. Reversal is a permutation of those words, including words with leading zeros. So each hexadecimal prefix permits at most `5^k` decimal prefixes.

Each compatible pair restricts the relative position of the two number systems to a short interval. As the hexadecimal length changes, that position moves according to the fractional part of:

{% highlight text %}
(n - 1) * log_10(16)
{% endhighlight %}

Since `log_10(16)` is irrational, these positions are equidistributed around the unit interval. This is the standard [irrational-rotation equidistribution theorem](https://math.iisc.ac.in/~manju/TA/3-weylequidistribution.pdf).

For the two smaller families together, there are only `2^p` hexadecimal prefixes. Taking `p = 5r` and `k = 6r` works because `16^5 > 10^6`. Counting all the permitted intervals bounds the upper density of possible lengths by:

{% highlight text %}
26 / ln(10) * 2^(-r)
{% endhighlight %}

That bound holds for every fixed positive integer `r`. Letting `r` grow forces the density to zero. The [full proof](https://github.com/perryizgr8/perryizgr8.github.io/blob/master/assets/palindrome-search/length-density-proof.md) spells out the interval bound and the order of the limits. There is no assumption that decimal and hexadecimal digits behave independently at random.

The same argument extends across all six families if adjacent nonzero hexadecimal digits are forbidden. The allowed prefixes then grow slowly enough for the bound to shrink. Interestingly, their growth rate is only just below the threshold needed by the proof.

Without that restriction, the larger families have four choices per independent prefix digit. This argument cannot handle that growth. Extending it to those unrestricted families is the main mathematical problem left by this approach.

## What we have, and what we don't

We have a much stronger search than the one we started with, a finite exclusion bound with checked certificates, and a proof draft about arbitrarily large lengths in restricted families. We still have no triple-base palindrome, no proof that none exists, and no confirmed claim of a new theorem.

For anyone who wants to inspect the mathematical part, I included the proof and a [standalone Python validation script](https://github.com/perryizgr8/perryizgr8.github.io/blob/master/assets/palindrome-search/validate_length_density.py). The script enumerates 131,055 general hexadecimal palindromes and checks the covering condition on actual positive decimal/hexadecimal examples. Those checks help catch implementation mistakes; the infinite-length conclusion comes from the proof, not the enumeration.

I would still like to see the number. But making the constraints explain something, even without finding a match, has been a satisfying outcome in its own right.
