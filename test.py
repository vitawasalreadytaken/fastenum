import timeit

N = 2000000

t1 = timeit.timeit('E.ENUM_MEMBER', 'import enum_native \nclass E(enum_native.Enum): ENUM_MEMBER = 1', number = N)
print('native: ', t1)
t2 = timeit.timeit('E.ENUM_MEMBER', 'import enum \nclass E(enum.Enum): ENUM_MEMBER = 1', number = N)
print('fast:   ', t2, '({:.2f}%)'.format(100 * t2 / t1))
