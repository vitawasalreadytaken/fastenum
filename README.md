fastenum
========

Faster version of Python 3.4's Enum implementation. It turns out that attribute lookups (any expressions like `MyEnum.SOME_MEMBER`) can be sped up by ~35% by removing two lines of code that don't even seem necessary. 

This is literally the only change I've made to the standard library implementation in `Lib/enum.py`:

```diff
-        if _is_dunder(name):
-            raise AttributeError(name)
+        # The `_is_dunder` check is not strictly necessary here
+        # and removing it speeds up attribute lookups.
+        # if _is_dunder(name):
+        #     raise AttributeError(name)
```

You can compare performance with the included `test.py` script:

```
$ python3 test.py
native:  4.2420294570038095
fast:    2.7184620610205457 (64.08%)
```
