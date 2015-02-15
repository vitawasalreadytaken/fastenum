# Faster enums

This package contains two implementations of a faster Python 3.4 Enum type. `enum_simple` is a minor edit of the standard library Enum and is perfectly compatible with it. `fastenum` is a simplified implementation that is significantly faster but not compatible with the standard Enum.

### Installation & usage

```
pip install git+https://github.com/ze-phyr-us/fastenum
```

```python
import enum_simple, fastenum

class Season1(enum_simple.Enum):
	SPRING = 1
	SUMMER = 2
	AUTUMN = 3
	WINTER = 4

class Season2(fastenum.Enum):
	SPRING = 1
	SUMMER = 2
	AUTUMN = 3
	WINTER = 4

assert Season1.SPRING is Season1['SPRING']
assert Season2.SUMMER is Season2['SUMMER']
assert Season1.AUTUMN is Season1(3)
assert Season2.AUTUMN is Season2(3)
assert Season1.WINTER is not Season2.WINTER
```

### Performance benchmarks

```
$ python3 benchmark.py
Timing
+----------------+-------------+----------------+-------------+-------------------+-------------------+
| Implementation | Enum.MEMBER | Enum["MEMBER"] | Enum(value) | hash(Enum.MEMBER) | repr(Enum.MEMBER) |
+----------------+-------------+----------------+-------------+-------------------+-------------------+
|  enum_native   |    2.2729   |     0.8454     |    1.4207   |       0.5573      |       1.4576      |
|  enum_simple   |    1.4010   |     0.8282     |    1.4214   |       0.5498      |       1.3209      |
|    fastenum    |    0.0533   |     0.4105     |    0.7917   |       0.3996      |       0.3550      |
+----------------+-------------+----------------+-------------+-------------------+-------------------+

Speedup vs native implementation
+----------------+-------------+----------------+-------------+-------------------+-------------------+
| Implementation | Enum.MEMBER | Enum["MEMBER"] | Enum(value) | hash(Enum.MEMBER) | repr(Enum.MEMBER) |
+----------------+-------------+----------------+-------------+-------------------+-------------------+
|  enum_simple   |    38.4%    |      1.0%      |    -0.1%    |        1.1%       |        0.4%       |
|    fastenum    |    97.7%    |     51.4%      |    44.3%    |       28.3%       |       75.6%       |
+----------------+-------------+----------------+-------------+-------------------+-------------------+
```

### Tests

`enum_simple` passes the standard library Enum tests. `fastenum` passes a subset of the standard tests. Tests are included in the repo and can be run with:

```
python3 -m unittest
```


## enum_simple (35% faster member lookups)

Faster version of Python 3.4's native Enum implementation. It turns out that attribute lookups (any expressions like `MyEnum.SOME_MEMBER`) can be sped up by ~35% by removing two lines of code that don't even seem necessary. 

This is literally the only change I've made to the standard library implementation in `Lib/enum.py`:

```diff
-        if _is_dunder(name):
-            raise AttributeError(name)
+        # The `_is_dunder` check is not strictly necessary here
+        # and removing it speeds up attribute lookups.
+        # if _is_dunder(name):
+        #     raise AttributeError(name)
```


## fastenum (97% faster member lookups, 25--75% speedups on everything else)

`fastenum` is a very lean implementation that does not preserve some behavior of the native Enum. In particular, many runtime integrity checks are skipped to speed up attribute lookups. For example, it does not prevent you from overwriting member values after the enum class is created, or from subclassing existing enums. If you do something like that, things may break in unpredictable ways.

This means you need to be more careful with this class. On the other hand, if you use enums heavily in a performance-sensitive application, the drastic performance benefits may be interesting.
