import timeit, prettytable

N = 100 * 1000
SETUP = 'import {module} \nclass E({module}.Enum): MEMBER = 1'


def time(module: str, op: str) -> float:
	return timeit.timeit(op, SETUP.format(module = module), number = N)

def fmt(t: float) -> str:
	return '{:.4f}'.format(t)


tab = prettytable.PrettyTable(('Implementation', 'Enum.MEMBER', 'Enum["MEMBER"]', 'Enum(value)'))
for module in ('enum_native', 'enum', 'fastenum'):
	t_attr = time(module, 'E.MEMBER')
	t_item = time(module, 'E["MEMBER"]')
	t_val = time(module, 'E(1)')
	tab.add_row((module, fmt(t_attr), fmt(t_item), fmt(t_val)))

print(tab)
