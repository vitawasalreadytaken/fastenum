import collections



def _is_descriptor(obj):
	"""Returns True if obj is a descriptor, False otherwise."""
	return (hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__'))


class EnumMeta(type):

	@classmethod
	def __prepare__(metacls, cls, bases):
		return collections.OrderedDict()


	def __new__(metacls, cls, bases, classdict: collections.OrderedDict):
		enum_class = super().__new__(metacls, cls, bases, classdict)
		# name->value map
		enum_class._member_map_ = collections.OrderedDict()
		# Reverse value->name map for hashable values.
		enum_class._value2member_map_ = {}

		for name, value in classdict.items():
			if not name.startswith('_') and not _is_descriptor(value):
				member = enum_class.__new__(enum_class)
				member.name = name
				member.value = value
				# name and value are not expected to change, so we can cache __repr__ and __hash__.
				member._repr = '<%s.%s: %r>' % (enum_class.__name__, name, value)
				member._hash = hash(name)

				#args = value if isinstance(value, tuple) else (value,)
				member.__init__()
				setattr(enum_class, name, member)
				enum_class._member_map_[name] = member
				try:
					# This may fail if value is not hashable. We can't add the value
					# to the map, and by-value lookups for this value will be linear.
					enum_class._value2member_map_[value] = member
				except TypeError:
					pass

		return enum_class


	def __call__(cls, value) -> 'Enum':
		# For lookups like Color(Color.red)
		if isinstance(value, cls):
			return value
		# by-value search for a matching enum member
		# see if it's in the reverse mapping (for hashable values)
		try:
			return cls._value2member_map_[value]
		except (KeyError, TypeError):
			# not there, now do long search -- O(n) behavior
			for member in cls._member_map_.values():
				if member.value == value:
					return member
		raise ValueError("%s is not a valid %s" % (value, cls.__name__))


	def __getitem__(cls, name: str) -> 'Enum':
		return cls._member_map_[name]


	def __iter__(cls):
		return (v for v in cls._member_map_.values())


	def __reversed__(cls):
		return reversed([ v for v in cls ])


	def __len__(cls):
		return len(cls._member_map_)



class Enum(metaclass = EnumMeta):

	def __repr__(self) -> str:
		return self._repr # cache of `'<%s.%s: %r>' % (self.__class__.__name__, self.name, self.value)`

	def __str__(self) -> str:
		return '%s.%s' % (self.__class__.__name__, self.name)

	def __hash__(self):
		return self._hash # cache of `hash(self.name)`

	def __format__(self, format_spec):
		return str.__format__(str(self), format_spec)

	def __reduce_ex__(self, proto):
		return self.__class__, (self.value,)
