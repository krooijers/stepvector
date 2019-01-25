# StepVector

A data structure to efficiently store and query values, or sets of values, in a
1D space.

While abstract, the envisioned use are genomic ranges, where a score, or
feature or features, span a certain genomic locus.

The underlying data structure is fast and space-efficient thanks to the
[sortedcontainers](http://www.grantjenks.com/docs/sortedcontainers/introduction.html) package.  
Memory usage is $\mathcal{O}(n)$ where $n$ is the number of "break points"
(steps). Insertion and query speed is $\mathcal{O}(\log n)$.  

In practice this means that e.g. all exons of the human genome can be kept in
memory easily even on old machines, and fetching overlapping exons in a certain
interval is basically instant.  
Generally, speed is competitive with established packages, e.g. `python`'s
`HTseq` and `R`/`BioConductor`'s `GenomicRanges`.


## Caution

> You probably don't want to use this!
> Instead, you're probably better off with (py)bedtools or HTSeq
>
> This package is/was an impromptu solution to have an efficient data structure
> for (values and/or sets of features in) genomic ranges, written in a time
> where HTSeq was python2-only.
>
> Things "work", but I can't say it has really been battle-tested, so caveat
> emptor...

[bedtools](http://bedtools.readthedocs.io/en/latest/)  
[pybedtools](https://daler.github.io/pybedtools/)  
[HTSeq](https://htseq.readthedocs.io/)  


## Installation

```bash
pip install git+https://github.com/krooijers/stepvector
```


## Use

```python
>>> from stepvector import StepVector

# create a stepvector that will hold float values
>>> sv = StepVector(float)

# set the region [100, 200) to 1.0
>>> sv[100:200] = 1.0

# query the steps in [0, 300):
>>> list(sv[0:300])
[(0, 100, 0.0), (100, 200, 1.0), (200, 300, 0.0)]

# assign [50, 150) the value 2.0:
>>> sv[50:150] = 2.0

# query all steps in `sv`:
# note the absence of (implicit) zero values
>>> list(sv)
[(50, 150, 2.0), (150, 200, 1.0)]

# query the steps in [0, 300):
# note the presence of (implicit) zero values
# note that the default value is derived from calling `<<datatype>>()`, e.g. in this case `float()`
>>> list(sv[0:300])
[(0, 50, 0.0), (50, 150, 2.0), (150, 200, 1.0), (200, 300, 0.0)]


# bug ? or harmless ?
>>> sv[0] = 0.0
>>> list(sv)
[(0, 1, 0.0), (1, 50, 0.0), (50, 150, 2.0), (150, 200, 1.0)]

# integers of course also work
>>> sv = StepVector(int)
>>> sv[100:200] = 1
>>> list(sv)
[(100, 200, 1)]

# incrementing is still to be implemented:
>>> sv[150:200] += 1
Traceback (most recent call last):
  File "<ipython-input-6-d421dfb1b7dc>", line 1, in <module>
    sv[150:200] += 1
TypeError: unsupported operand type(s) for +=: 'StepVector' and 'int'

# instead, use `add_value()`:
>>> sv.add_value(150, 200, 1)
>>> list(sv)
[(100, 150, 1), (150, 200, 2)]

```

Another useful feature is to hold sets of items that span intervals:

```python
>>> sv = StepVector(set)

>>> sv[100:200] = {"A"}
>>>
>>> list(sv[0:300])
[(0, 100, set()), (100, 200, {'A'}), (200, 300, set())]

>>> sv.add_value(50, 150, {"B"})
>>> 
>>> list(sv)
[(50, 100, {'B'}), (100, 150, {'A', 'B'}), (150, 200, {'A'})]

>>> sv.add_value(150, 250, {"C"})
>>> 
>>> list(sv)
[(50, 100, {'B'}), (100, 150, {'A', 'B'}), (150, 200, {'A', 'C'}), (200, 250, {'C'})]

>>> list(sv[0:300])
[(0, 50, set()), (50, 100, {'B'}), (100, 150, {'A', 'B'}), (150, 200, {'A', 'C'}), (200, 250, {'C'}), (250, 300, set())]

```

Unlike HTSeq, `StepVector`s are abstract and apply to any linear 1D-space. If
you want to use them for genomic intervals -where you have chromosomes, and
strands that make up a genome- you need to implement it yourself. The
recommended way is to use `defaultdict`s for chromosomes and `dict`s for
strands. Unstranded features should be placed in a pseudo-strand `.` (HTSeq
does it this way).

For example:
```python
from collections import defaultdict

from stepvector import StepVector

# initialize mapping:
# for every chrom (TBD): for "+" and "-": a StepVector of sets
my_features = defaultdict(lambda: {"+": StepVector(set), "-": StepVector(set)})

bed = """
chr1 50 150 a . +
chr1 100 200 b . +
chr1 150 250 c . +
chr1 50 250 d . -
chr2 100 300 e . +
"""

bed_field_iter = (line.strip().split() for line in filter(None, bed.splitlines()))

for fields in bed_field_iter:
    chrom, start, end, name, score, strand = fields
    start, end = int(start), int(end)
    my_features[chrom][strand].add_value(start, end, {name})
```

Query:

```python
for stepstart, stepend, stepvalues in my_features['chr1']['+'][0:180]:
    print(stepstart, stepend, sorted(stepvalues))
```
```text
0 50 []
50 100 ['a']
100 150 ['a', 'b']
150 180 ['b', 'c']
```

List all:

```python
chroms = sorted(my_features.keys())
for chrom in chroms:
    for strand in ("+", "-"):
        for stepstart, stepend, stepvalues in my_features[chrom][strand]:
            print(chrom, strand, stepstart, stepend, sorted(stepvalues))
```
```text
chr1 + 50 100 ['a']
chr1 + 100 150 ['a', 'b']
chr1 + 150 200 ['b', 'c']
chr1 + 200 250 ['c']
chr1 - 50 250 ['d']
chr2 + 100 300 ['e']
```

## Feedback and Legal

No warranty whatsoever.

Feedback, bug reports and fixes (in the form of well-formatted pull requests)
are much appreciated.
