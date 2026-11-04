# A length-density obstruction for restricted hexadecimal palindromes

4 November 2026. Status: complete proof draft, checked internally; not externally
reviewed. Priority/novelty is unverified. No claim of finiteness or nonexistence of
the unrestricted triple-base palindrome set is made.

## Statements

Let a *possible length* for a class mean a positive integer n for which at least
one member of that class has exactly n canonical hexadecimal digits and is also
a canonical decimal palindrome. Density here is density of **lengths**, not the
already sparse set of integer values.

**Theorem A.** The possible lengths for the union of the hexadecimal-palindrome
families with digits {0,1} and {0,3} have natural density zero:

    lim (1/X) #{n <= X : such a palindrome exists at length n} = 0.
    X -> infinity

Both families automatically have palindromic binary expansions, by the known
binary/hexadecimal digit classification. Thus almost every hexadecimal length is
impossible for a triple palindrome in these two families. This permits an infinite
set of exceptional lengths; it does not eliminate either family entirely.

**Theorem B.** The same conclusion holds for all six binary/hexadecimal families
combined, restricted to strings with **no adjacent nonzero hexadecimal digits**.

The latter restriction is imposed on the complete canonical hexadecimal string,
including its center and endpoints.

## General covering lemma

Put eta = log_10(16). Let C be any class of canonical hexadecimal palindromes.
Suppose that for each p there is a finite set V_p of p-digit hexadecimal strings
such that every member of C of length n >= 2p starts with a string in V_p. Write
H_p = |V_p|. The set V_p must be independent of n.

For any integers p,k >= 1 satisfying

    10^k <= 16^p,       k <= 4p,

there is a finite union E_(p,k) of closed arcs of the circle R/Z with total
Lebesgue measure at most

    measure(E_(p,k)) <= (26 / ln(10)) H_p / 2^k,

such that every possible length n >= 2p satisfies

    {(n-1) eta} in E_(p,k).

Bounds exceeding 1 are harmless. Curly braces denote fractional part. These are
fixed finite unions for each fixed p,k; their number of arcs need not be small.

### Proof of the lemma

Take a simultaneous hexadecimal/decimal palindrome N of hexadecimal length n.
Let v be the integer represented by its first p hex digits. Define rev_B,k to
reverse exactly k base-B digits, retaining zeros in the fixed-width word. Since
N is a hexadecimal palindrome,

    N = rev_16,p(v)  (mod 16^p).

Let d be its decimal length and P its first k decimal digits. Here d >= k:
n >= 2p implies N >= 16^(2p-1) >= 16^p >= 10^k. Decimal palindromicity gives

    N = rev_10,k(P)  (mod 10^k).

Consequently

    rev_10,k(P) = rev_16,p(v)  (mod 2^k).                 (1)

This uses k <= 4p. Reversal is a permutation of the 10^k fixed-width decimal
words. Each residue modulo 2^k occurs exactly 5^k times among those words.
Requiring a nonzero first digit can only reduce the count. Therefore each fixed
v admits at most 5^k possibilities for P.

For a fixed pair (v,P), the normalized significands lie in

    a = N / 16^(n-1) in [v / 16^(p-1), (v+1) / 16^(p-1)],
    b = N / 10^(d-1) in [P / 10^(k-1), (P+1) / 10^(k-1)].

Closing the right endpoints enlarges these necessary intervals and is safe.
Their logarithms range over intervals of lengths respectively

    log_10(1 + 1/v) <= 16^(1-p) / ln(10),
    log_10(1 + 1/P) <= 10^(1-k) / ln(10).

But

    log_10(b) - log_10(a) = (n-1) eta - (d-1).

Thus the fractional part {(n-1)eta} lies in the difference of those two logarithm
intervals, taken modulo 1. This image is a closed arc, or the entire circle if
the interval is long enough. Its measure is at most the interval length, hence
at most

    [16 * 16^(-p) + 10 * 10^(-k)] / ln(10)
        <= (26 / ln(10)) * 10^(-k).

There are at most H_p * 5^k admissible pairs. The measure of their union is no
greater than the sum of their measures. This proves the claimed bound. QED.

## From the cover to a statement about lengths

The number eta is irrational: a rational identity eta = a/b with positive
integers a,b would give 16^b = 10^a, contradicted by the prime factor 5.
Therefore {(n-1)eta} is equidistributed modulo 1. For completeness, for every
nonzero integer h, the associated exponential average is a geometric sum divided
by X; its denominator 1-exp(2*pi*i*h*eta) is nonzero, so the average tends to zero.
Weyl's criterion gives equidistribution. See the
[IISc lecture notes, Theorem 2 and Lemma 7](https://math.iisc.ac.in/~manju/TA/3-weylequidistribution.pdf).

For each **fixed** p,k, the finite union E_(p,k) has boundary of measure zero.
Equidistribution implies that its visit frequency equals its measure. The
finitely many lengths n < 2p do not affect density. Hence the upper natural
density of possible lengths is at most

    (26 / ln(10)) H_p / 2^k.                            (2)

We first take X -> infinity with p,k fixed, and only then vary p,k. There is no
claim of uniform equidistribution for shrinking targets.

In particular, if H_p <= C lambda^p with

    lambda < 2^(log_10(16)) = 2.3039668876...,

choose k = floor(p log_10(16)). Conditions of the covering lemma hold and (2)
is bounded by (52C / ln(10)) [lambda / 2^(log_10(16))]^p, which tends to zero.

### Proof of Theorem A with integer block sizes

For the two families combined, H_p = 2 * 2^(p-1) = 2^p. Choose p = 5r, k = 6r.
The integer inequality 16^5 = 1,048,576 > 10^6 ensures 10^k <= 16^p; also k <= 4p.
Equation (2) gives, for every r >= 1,

    upper_density(possible lengths) <= (26 / ln(10)) * 2^(-r).

Let r tend to infinity. The upper density is zero, so the natural density exists
and equals zero. QED.

### Proof of Theorem B with exact arithmetic witnesses

Fix a leading family digit. Enlarge its alphabet to four digits consisting of
zero and three nonzero choices. The number u_p of allowed p-digit prefixes with
that fixed nonzero first digit and no adjacent nonzero digits obeys

    u_1 = u_2 = 1,       u_p = u_(p-1) + 3 u_(p-2)  (p >= 3).

Indeed, append either a zero to any shorter prefix, or a zero followed by one of
three nonzero digits to a prefix two positions shorter. Its growth root is
(1+sqrt(13))/2 = 2.3027756377..., just below the covering threshold.

No numerical comparison of those two real constants is needed. Put L = 2303/1000.
The following three strict inequalities are integer checks:

    2303^2 > 2303*1000 + 3*1000^2,
    16^49 > 10^59,
    2303^49 < 1000^49 * 2^59.

The first gives L^2 > L+3. Induction on the recurrence yields u_p <= L^(p-1),
and hence H_p <= 6 L^p for the union of six families. Choose p = 49r, k = 59r.
The last two integer checks ensure the covering conditions and give

    upper_density(possible lengths)
        <= (156 / ln(10)) * (L^49 / 2^59)^r -> 0.

Again the natural density is zero. QED.

## Limits, provenance and checks

This is a complete elementary argument conditional only on the standard
irrational-rotation equidistribution theorem. It supplies neither a last possible
length nor a proof that even one exceptional length contains an answer. It does
not improve the unrestricted all-family finite exclusion bound.

The generic four-symbol families have H_p growing like 4^p, so this counting
argument does not prove density zero for them without an extra restriction.
Improving that entropy threshold is the main mathematical obstacle to extending
this result to the whole problem.

The known hexadecimal/binary classification is due to
[Rick Regan's structural analysis](https://www.exploringbinary.com/the-structure-of-binary-hexadecimal-palindromes/).
The prefix/suffix compatibility mechanism is closely related to
[Schacham's search method](https://ashdnazg.github.io/articles/22/Finding-Really-Big-Palindromes).
[Berczes and Ziegler](https://arxiv.org/abs/1403.0787) study simultaneous
palindromes and prove bounds for specified long zero-gap families; those results
are background rather than an ingredient of this proof. No priority claim is
made for the covering argument or its specializations.

`validate_length_density.py` checks the integer witnesses, reversal
multiplicities, prefix recurrence and necessary-cover inclusion on actual
hexadecimal/decimal palindromes, including positive controls from more general
alphabets. These finite checks are development checks, not the proof of the
asymptotic statements.


## Internal audit of the argument

- The reversal counts use all fixed-width words, including leading zeros, as a
  superset. No assumption that reversed P still has k canonical digits is used.
- The hexadecimal prefix v and its reversed suffix are independent of n once
  p is fixed. This is what makes the phase cover fixed as n varies.
- An arc crossing phase zero is interpreted on the circle, not discarded.
  Closing interval endpoints can add only valid necessary conditions.
- Counting arcs overcounts overlaps; it yields an upper bound, which is the
  direction required. No probabilistic independence is assumed.
- Equidistribution is used only for a fixed finite union. Letting the prefix
  size grow before taking the limit in the number of lengths would be unjustified.
- Density zero is not finiteness. The density result is compatible with no
  solutions, finitely many solutions, or infinitely many exceptionally spaced
  lengths. No claim that the actual solution set is nonempty is used.
- The mathematical proof does not trust the search's empty hit lists, GPU
  arithmetic, LLL tables, or any finite computation of decimal logarithms.
