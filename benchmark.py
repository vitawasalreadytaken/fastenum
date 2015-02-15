import timeit, prettytable

N = 1000 * 1000
SETUP = 'import {module} \nclass E({module}.Enum): MEMBER = 1 \n{extra}'


def time(module: str, op: str, extraSetup: str = '') -> float:
	return timeit.timeit(op, SETUP.format(module = module, extra = extraSetup), number = N)

def fmt(t: float) -> str:
	return '{:.4f}'.format(t)


print('Timing')
times = {}
tab = prettytable.PrettyTable(('Implementation', 'Enum.MEMBER', 'Enum["MEMBER"]', 'Enum(value)', 'hash(Enum.MEMBER)', 'repr(Enum.MEMBER)'))
for module in ('enum_native', 'enum_simple', 'fastenum'):
	t = {
		'attr': time(module, 'E.MEMBER'),
		'item': time(module, 'E["MEMBER"]'),
		'val': time(module, 'E(1)'),
		'hash': time(module, 'hash(E_MEMBER)', 'E_MEMBER = E.MEMBER'),
		'repr': time(module, 'repr(E_MEMBER)', 'E_MEMBER = E.MEMBER'),
	}
	times[module] = t
	tab.add_row((module, fmt(t['attr']), fmt(t['item']), fmt(t['val']), fmt(t['hash']), fmt(t['repr'])))

print(tab)


print('\nSpeedup vs native implementation')
tab = prettytable.PrettyTable(('Implementation', 'Enum.MEMBER', 'Enum["MEMBER"]', 'Enum(value)', 'hash(Enum.MEMBER)', 'repr(Enum.MEMBER)'))
for module in ('enum_simple', 'fastenum'):
	tab.add_row([module] + [
		'{:.1f}%'.format(100 - 100 * times[module][k] / times['enum_native'][k])
		for k in ('attr', 'item', 'val', 'hash', 'repr')
	])

print(tab)
