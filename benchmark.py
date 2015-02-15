import timeit, prettytable

N = 1000 * 1000
SETUP = 'import {module} \nclass E({module}.Enum): MEMBER = 1 \n{extra}'


def time(module: str, op: str, extraSetup: str = '') -> float:
	return timeit.timeit(op, SETUP.format(module = module, extra = extraSetup), number = N)

def fmt(t: float) -> str:
	return '{:.4f}'.format(t)


tab = prettytable.PrettyTable(('Implementation', 'Enum.MEMBER', 'Enum["MEMBER"]', 'Enum(value)', 'hash(Enum.MEMBER)', 'repr(Enum.MEMBER)'))
for module in ('enum_native', 'enum', 'fastenum'):
	t_attr = time(module, 'E.MEMBER')
	t_item = time(module, 'E["MEMBER"]')
	t_val = time(module, 'E(1)')
	t_hash = time(module, 'hash(E_MEMBER)', 'E_MEMBER = E.MEMBER')
	t_repr = time(module, 'repr(E_MEMBER)', 'E_MEMBER = E.MEMBER')
	tab.add_row((module, fmt(t_attr), fmt(t_item), fmt(t_val), fmt(t_hash), fmt(t_repr)))

print(tab)
