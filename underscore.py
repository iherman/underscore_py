#!/usr/bin/env python
# coding=utf-8
from types import *
import itertools
import random
import math
import bisect

__version__ = 0.2

class underscore(object):
	"""
	The example codes all rely on:

	```
	from underscore import underscore as _
	listOfPlays = [
		{
			"author" : "Shakespeare",
			"year"   : 1611,
			"title"  : "The tempest"
		},
		{
			"author" : "Shakespeare",
			"year"   : 1611,
			"title"  : "Cymbeline"
		},
		{
			"author" : "Shakespeare",
			"year"   : 1601,
			"title"  : "Romeo and Juliet"
		},
	]
	stooges = [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}]
	def createApplication():
		print("created")
	```

	"""
	@staticmethod
	def _exec1(f, context, a1):
		if isinstance(f, basestring):
			return a1[f]
		elif context is None:
			return f(a1)
		else:
			return f(context, a1)

	@staticmethod
	def _exec2(f, context, a1, a2):
		if context is None:
			return f(a1, a2)
		else:
			return f(context, a1, a2)

	@staticmethod
	def _exec3(f, context, a1, a2, a3):
		if context is None:
			return f(a1, a2, a3)
		else:
			return f(context, a1, a2, a3)

	@staticmethod
	def _exec4(f, context, a1, a2, a3, a4):
		if context is None:
			return f(a1, a2, a3, a4)
		else:
			return f(context, a1, a2, a3, a4)

	@staticmethod
	def _extends( obj, ext) :
		if isinstance(obj,DictType) and isinstance(ext, DictType) :
			for key in ext:
				if key not in obj or obj[key] != ext[key]:
					return False
			return True
		return False

	@staticmethod
	def _index_sorted(a, x):
		"""Locate the leftmost value exactly equal to x when the array is sorted"""
		i = bisect.bisect_left(a, x)
		return i if i != len(a) and a[i] == x else -1

	@staticmethod
	def identity(x):
		return x

	@staticmethod
	def each(list, iteratee, context = None):
		"""Iterates over a list of elements, yielding each in turn to an **iteratee** function. Each
		invocation of **iteratee** is called with three arguments: if **list** is of list type,
		then the arguments are ``(element, index, list)``, if it is of dictionary type, or
		the arguments are ``(value, key, list``). Returns **list** for chaining.

		```
		>>> def pr(element, index, list):
		>>>	    print element
		>>> _.each([1, 2, 3], pr)
		1
		2
		3
		>>> _.each({'one': 11, 'two': 22, 'three': 33}, pr)
		33
		22
		11
		```
		"""
		if iteratee is None:
			return list
		elif isinstance(list, ListType):
			for i in xrange(0, len(list)):
				underscore._exec3(iteratee, context, list[i], i, list)
		elif isinstance(list, DictType):
			for key in list:
				underscore._exec3(iteratee, context, list[key], key, list)
		return list

	@staticmethod
	def map(list, iteratee, context = None):
		"""Produces a new array of values by mapping each value in list through a transformation function (**iteratee**).
		The **iteratee** is passed three arguments: the ``value``, then the ``index`` (or ``key``) of the iteration, and finally a reference to the entire list.

		```
		>>> _.map([1, 2, 3], lambda num, *args: num * 3)
		[3, 6, 9]
		>>> _.map({'one': 1, 'two': 2, 'three': 3}, lambda num, key, *args: num * 4)
		[12, 8, 4]
		>>> _.map([[1, 2], [3, 4]], lambda a, *args: _.first(a));
		[1, 3]
		```
		"""
		if iteratee is None:
			return list
		elif isinstance(list, ListType):
			return map(lambda i: underscore._exec3(iteratee, context, list[i], i, list), xrange(0, len(list)))
		elif isinstance(list, DictType):
			return map(lambda key: underscore._exec3(iteratee, context, list[key], key, list), list.keys())
		else:
			return list

	@staticmethod
	def reduce(list, iteratee, memo = None, context = None):
		"""
		Reduce boils down a list of values into a single value. **Memo** is the initial state of the reduction, and each successive step of it should be returned by **iteratee**. The **iteratee** is passed four arguments: the ``memo``, then the ``value`` and ``index`` (or ``key``) of the iteration, and finally a reference to the entire list.

		If no memo is passed to the initial invocation of reduce, the iteratee is not invoked on the first element of the list. The first element is instead passed as the memo in the invocation of the iteratee on the next element in the list.

		```
		>>> _.reduce([1, 2, 3], lambda memo, num, *args: memo + num, 0)
		6
		```
		"""
		if isinstance(list, ListType):
			return reduce(lambda m,i: underscore._exec4(iteratee, context, m, list[i], i, list), xrange(0, len(list)), memo)
		elif isinstance(list, DictType):
			return reduce(lambda m,i: underscore._exec4(iteratee, context, m, list[key], key, list), xrange(0, len(list)), memo)

	@staticmethod
	def find(list, predicate, context = None):
		"""
		Looks through each value in the **list**, returning the first one that passes a truth test (**predicate**), or ``None`` if no value passes the test. The function returns as soon as it finds an acceptable element, and doesn't traverse the entire list.

		```
		>>> _.find([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0)
		2
		```
		"""
		for x in list:
			if underscore._exec1(predicate, context, x):
				return x
		return None


	@staticmethod
	def filter(list, predicate, context = None):
		"""
		Looks through each value in the **list**, returning an array of all the values that pass a truth test (**predicate**).

		```
		>>> _.filter([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0)
		[2, 4, 6]
		```
		"""
		return [ x for x in list if underscore._exec1(predicate, context, x)]

	@staticmethod
	def where(list, properties):
		"""
		Looks through each value in the **list**, returning an array of all the values that contain all of the key-value pairs listed in **properties**.
		```
		>>> _.where(listOfPlays, {'author': "Shakespeare", 'year': 1611})
		[{'title': 'The tempest', 'year': 1611, 'author': 'Shakespeare'},
		 {'title': 'Cymbeline', 'year': 1611, 'author': 'Shakespeare'}]
		```
		"""
		return [ x for x in list if underscore._extends(x, properties) ]

	@staticmethod
	def findWhere(list, properties):
		"""
		Looks through the **list** and returns the *first* value that matches all of the key-value pairs listed in **properties**.

		```
		>>> _.findWhere(listOfPlays, {'author': "Shakespeare", 'year': 1611})
		{'title': 'The tempest', 'year': 1611, 'author': 'Shakespeare'}
		```
		"""
		for x in list:
			if underscore._extends(x, properties):
				return x
		return None

	@staticmethod
	def reject(list, predicate, context = None):
		"""
		Returns the values in **list** without the elements that the truth test (**predicate**) passes. The opposite of filter.

		```
		>>> _.reject([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0)
		[1, 3, 5]
		```
		"""
		return [ x for x in list if not underscore._exec1(predicate, context, x)]

	@staticmethod
	def every(list, predicate = None, context = None):
		"""
		Returns true if all of the values in the **list** pass the **predicate** truth test.

		```
		>>> _.every([True, 1, None, 'yes'], _.identity)
		False
		```
		"""
		if predicate is None: predicate = underscore.identity
		for x in list:
			if not underscore._exec1(predicate, context, x):
				return False
		return True

	@staticmethod
	def some(list, predicate = None, context = None):
		"""
		Returns true if any of the values in the **list** pass the predicate truth test. Short-circuits and stops traversing the list if a true element is found.

		```
		>>> _.some([None, 0, True, False])
		True
		```
		"""
		if predicate is None: predicate = underscore.identity
		for x in list:
			if underscore._exec1(predicate, context, x):
				return True
		return False

	@staticmethod
	def contains(list, value):
		"""
		Returns true if the value is present in the list.
		"""
		return value in list

	@staticmethod
	def pluck(list, propertyName):
		"""
		A convenient version of what is perhaps the most common use-case for **map**: extracting a list of property values from an array of dictionaries.

		```
		>>> _.pluck(stooges, 'name');
		['moe', 'larry', 'curly']
		```
		"""
		return [l[propertyName] for l in list]

	@staticmethod
	def max(list, iteratee = None, context = None):
		"""
		Returns the maximum value in **list**. If an **iteratee** function is provided, it will be used on each value to generate the criterion by which the value is ranked. `float("inf")` is returned if list is empty, so a guard may be required.

		```
		>>> _.max(stooges, lambda stooge: stooge['age'])
		{'age': 60, 'name': 'curly'}
		```
		"""
		if list is None or len(list) == 0:
			return float("inf")
		if iteratee is None :
			return max(list)
		else:
			return max(list, key=lambda x: underscore._exec1(iteratee, context, x))

	@staticmethod
	def min(list, iteratee = None, context = None):
		"""
		Returns the min value in **list**. If an **iteratee** function is provided, it will be used on each value to generate the criterion by which the value is ranked. `float("-inf")` is returned if list is empty, so an guard may be required.

		```
		>>> _.max(stooges, lambda stooge: stooge['age'])
		{'age': 40, 'name': 'moe'}
		```
		"""
		if list is None or len(list) == 0:
			return float("-inf")
		if iteratee is None :
			return min(list)
		else:
			return min(list, key=lambda x: underscore._exec1(iteratee, context, x))

	@staticmethod
	def sortBy(list, iteratee = None, context = None):
		"""
		Returns a sorted copy of **list**, ranked in ascending order by the results of running each value through **iteratee**. **iteratee** may also be the string name of the property.

		```
		>>> _.sortBy([1, 2, 3, 4, 5, 6], lambda num: math.sin(num))
		[5, 4, 6, 3, 1, 2]
		>>> _.sortBy(stooges, 'name')
		[{'age': 60, 'name': 'curly'}, {'age': 50, 'name': 'larry'}, {'age': 40, 'name': 'moe'}]
		```

		"""
		if iteratee is None:
			return sorted(list)
		elif isinstance(iteratee, basestring):
			return sorted(list, key=lambda x: x[iteratee])
		else:
			return sorted(list, key=lambda x: underscore._exec1(iteratee, context, x))

	@staticmethod
	def _group(list, iteratee, context):
		if isinstance(iteratee, basestring):
			return itertools.groupby(list, lambda x: x[iteratee])
		else:
			return itertools.groupby(list, lambda x: underscore._exec1(iteratee, context, x))

	@staticmethod
	def groupBy(list, iteratee, context = None):
		"""
		Splits a collection into sets, grouped by the result of running each value through **iteratee**. If **iteratee** is a string instead of a function, groups by the property named by iteratee on each of the values.

		```
		>>> _.groupBy([1.3, 2.1, 2.4], lambda num: math.floor(num))
		{1.0: [1.3], 2.0: [2.1, 2.4]}
		>>> st2= [{'name': 'joe', 'age': 40}, {'name': 'tom', 'age': 50}, {'name': 'bill', 'age': 50}]
		>>> _.groupBy(st2, 'age')
		{40: [{'age': 40, 'name': 'joe'}], 50: [{'age': 50, 'name': 'tom'}, {'age': 50, 'name': 'bill'}]}
		```
		"""
		retval = {}
		for group in underscore._group(list, iteratee, context):
			retval[group[0]] = [x for x in group[1]]
		return retval

	@staticmethod
	def indexBy(list, iteratee, context = None):
		"""
		Given a **list**, and an **iteratee** function that returns a key for each element in the list (or a property name), returns an object with an index of each item. Just like **groupBy**, but for when you know your keys are unique.

		```
		>>> _.indexBy(stooges, 'age')
		{40: {'age': 40, 'name': 'moe'}, 50: {'age': 50, 'name': 'larry'}, 60: {'age': 60, 'name': 'curly'}}
		```
		"""
		retval = {}
		for group in underscore._group(list, iteratee, context):
			retval[group[0]] = group[1].next()
		return retval

	@staticmethod
	def countBy(list, iteratee, context = None):
		"""
		Sorts a **list** into groups and returns a count for the number of objects in each group. Similar to **groupBy**, but instead of returning a list of values, returns a count for the number of values in that group.

		```
		>>> _.countBy([1, 2, 3, 4, 5], lambda num: 'even' if num % 2 == 0 else 'odd')
		{'even': 1, 'odd': 1}
		```
		"""
		retval = {}
		for group in underscore._group(list, iteratee, context):
			retval[group[0]] = len([x for x in group[1]])
		return retval

	@staticmethod
	def shuffle(list):
		"""
		Returns a shuffled copy of the **list**.

		```
		>>> _.shuffle([1, 2, 3, 4, 5, 6])
		[6, 4, 5, 2, 1, 3]
		```
		"""
		indeces = [ i for i in xrange(0, len(list)) ]
		random.shuffle(indeces);
		return [ list[i] for i in indeces ]

	@staticmethod
	def sample(list, n = None):
		"""
		Produce a random sample from the **list**. Pass a number to return **n** random elements from the list. Otherwise a single random item will be returned.
		```
		>>> _.sample([1, 2, 3, 4, 5, 6])
		1
		>>> _.sample([1, 2, 3, 4, 5, 6], 3)
		[4, 1, 5]
		```
		"""
		return random.sample(list, 1)[0] if n is None else random.sample(list, n)

	@staticmethod
	def toArray(lst):
		"""
		Creates a real Array from the **lst** (anything that can be iterated over). Useful for transmuting the arguments object. An alias to the built-in **list** function.
		```
		>>> _.toArray(xrange(0,4))
		[0, 1, 2, 3]
		```
		"""
		return list(lst)

	@staticmethod
	def size(list):
		"""
		Return the number of values in the **list**. An alias to the built-in **len** function.
		```
		>>> _.size({'one': 1, 'two': 2, 'three': 3})
		3
		```
		"""
		return len(list)

	@staticmethod
	def partition(list, predicate, context = None):
		"""
		Split array into two arrays: one whose elements all satisfy predicate and one whose elements all do not satisfy predicate. If **list** is actually a tuple, then a tuple is returned, otherwise an array, each containing the two generated arrays in the 'yes' and 'no' order.
		```
		>>> _.partition([0, 1, 2, 3, 4, 5], lambda num: num % 2 != 0)
		[[1, 3, 5], [0, 2, 4]]
		```
		"""
		yes = []
		no  = []
		for x in list:
			if underscore._exec1(predicate, context, x) is True:
				yes.append(x)
			else:
				no.append(x)
		return (yes, no) if type(list) is TupleType else [yes,no]

	###############################################################################
	#                                Array Functions                              #
	###############################################################################

	@staticmethod
	def first(array, n = None):
		"""Returns the first element of an array. Passing n will return the first n elements of the array.
		```
		>>> _.first([5, 4, 3, 2, 1])
		5
		>>> _.first([5, 4, 3, 2, 1],3)
		[5, 4, 3]
		```
		"""
		return array[0] if n is None else array[0:n]

	@staticmethod
	def initial(array, n = 1):
		"""Returns everything but the last entry of the array. Especially useful on the arguments object. Pass n to exclude the last n elements from the result.

		```
		>>> _.initial([5, 4, 3, 2, 1])
		[5, 4, 3, 2]
		>>> _.initial([5, 4, 3, 2, 1],3)
		[5, 4]
		```
		"""
		return array[:-n]

	@staticmethod
	def last(array, n = None):
		"""Returns the last element of an array. Passing n will return the last n elements of the array.
		```
		>>> _.last([5, 4, 3, 2, 1])
		1
		>>> _.last([5, 4, 3, 2, 1],3)
		[3, 2, 1]
		```
		"""
		return array[-1] if n is None else array[-n:]

	@staticmethod
	def rest(array, n = 1):
		"""Returns the rest of the elements in an array. Pass an index to return the values of the array from that index onward.
		>>> _.rest([5, 4, 3, 2, 1])
		[4, 3, 2, 1]
		>>> _.rest([5, 4, 3, 2, 1],3)
		[2, 1]
		```
		"""
		return array[n:]

	@staticmethod
	def compact(array):
		"""
		Returns a copy of the array with all falsy values removed. ``False``, ``None``, 0, "", and ``NaN`` for floats are all falsy.
		```
		>>> _.compact([0, 1, False, 2, '', 3])
		[1, 2, 3]
		```
		"""
		falsy = lambda x: x is None or x is False or x == "" or x == 0 or (type(x) is FloatType and math.isnan(x))
		return [x for x in array if falsy(x) is not True]

	@staticmethod
	def flatten(array, shallow = False):
		"""Flattens a nested array (the nesting can be to any depth). If you pass shallow, the array will only be flattened a single level.

		```
		>>> _.flatten([1, [2], [3, [[4]]]])
		[1, 2, 3, 4]
		>>> _.flatten([1, [2], [3, [[4]]]], True)
		[1, 2, 3, [[4]]]
		```
		"""
		retval = []
		for x in array :
			if type(x) is ListType:
				retval +=  x if shallow else underscore.flatten(x)
			else:
				retval.append(x)
		return retval

	@staticmethod
	def without(array, *values):
		"""Returns a copy of the array with all instances of the values removed.
		```
		>>> _.without([1, 2, 1, 0, 3, 1, 4], 0, 1)
		[2, 3, 4]
		```
		"""
		return [x for x in array if x not in values]

	@staticmethod
	def union(*arrays):
		"""
		Computes the union of the passed-in arrays: the list of unique items, in order, that are present in one or more of the arrays.

		```
		>>> _.union([1, 2, 3], [101, 2, 1, 10], [2, 1])
		[1, 2, 3, 101, 10]
		```
		"""
		if len(arrays) == 0:
			return []
		elif len(arrays) == 1:
			return [x for x in arrays[0]]
		else :
			retval = []
			for a in arrays:
				for x in a:
					if x not in retval:
						retval.append(x)
			return retval

	@staticmethod
	def intersection(*arrays):
		"""
		Computes the list of values that are the intersection of all the arrays. Each value in the result is present in each of the arrays.

		```
		>>> _.intersection([1, 2, 3], [101, 2, 1, 10], [2, 1])
		[1, 2]
		```
		"""
		if len(arrays) == 0:
			return []
		elif len(arrays) == 1:
			return [x for x in arrays[0]]
		else :
			curr = arrays[0]
			retval = []
			for b in arrays[1:]:
				for x in curr:
					if x in b and x not in retval:
						retval.append(x)
			return retval

	@staticmethod
	def difference(array, *others):
		"""
		Similar to **without**, but returns the values from array that are not present in the other arrays.
		```
		>>> _.difference([1, 2, 3, 4, 5], [5, 2, 10])
		[1, 3, 4]
		```
		"""
		if len(others) == 0:
			return [x for x in array]
		else :
			retval = []
			for x in array:
				tobeadded = True
				for a in others:
					if x in a:
						tobeadded = False
						break
				if tobeadded: retval.append(x)
			return retval

	@staticmethod
	def uniq(array, iteratee = None, context = None, isSorted = False):
		"""
		Produces a duplicate-free version of the array, based on the "in" operator of Python's list. If you want to compute unique items after a transformation, pass an iteratee function. If you know in advance that the array is sorted, passing ``True`` for **isSorted** will run a much faster algorithm.
		```
		>>> _.uniq([1, 2, 1, 3, 1, 4])
		[1, 2, 3, 4]
		```
		"""
		if len(array) == 0:
			return []
		else:
			to_compare = (lambda x: x) if iteratee is None else (lambda x: underscore._exec1(iteratee, context, x))
			retval      = [array[0]]
			comparisons = [to_compare(array[0])]
			if isSorted:
				for x in array[1:]:
					y = to_compare(x)
					if underscore._index_sorted(comparisons, y) == -1:
						retval.append(x)
						comparisons.append(y)
			else:
				for x in array[1:]:
					y = to_compare(x)
					if y not in comparisons:
						retval.append(x)
						comparisons.append(y)
			return retval

	@staticmethod
	def zip(*arrays):
		"""
		Merges together the values of each of the arrays with the values at the corresponding position. Useful when you have separate data sources that are coordinated through matching array indexes. If the arguments are tuples, a tuple is returned, otherwise an array.
		```
		>>> _.zip(['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False])
		[['moe', 30, True], ['larry', 40, False], ['curly', 50, False]]
		>>> _.zip(('moe', 'larry', 'curly'), (30, 40, 50), (True, False, False))
		[('moe', 30, True), ('larry', 40, False), ('curly', 50, False)]
		```
		"""
		zipped = zip(*arrays)
		if type(arrays[0]) is TupleType :
			return zipped
		else:
			return map(lambda x: list(x), zipped)

	@staticmethod
	def object(list, values = None):
		"""
		Converts arrays into dictionaries. Pass either a single list of [key, value] pairs, or a list of keys, and a list of values. If duplicate keys exist, the last value wins.

		```
		>>> _.object(['moe', 'larry', 'curly'], [30, 40, 50])
		{'larry': 40, 'curly': 50, 'moe': 30}
		>>> _.object([['moe', 30], ['larry', 40], ['curly', 50]])
		{'larry': 40, 'curly': 50, 'moe': 30}
		>>>
		```
		"""
		if values is None:
			return {x[0]:x[1] for x in list}
		else:
			return {list[i]:values[i] for i in xrange(0,min(len(list),len(values)))}

	@staticmethod
	def indexOf(array, value, isSorted = False):
		"""
		Returns the index at which value can be found in the array, or -1 if value is not present in the array. If you're working with a large array, and you know that the array is already sorted, pass `True` for isSorted to use a faster binary search... or, pass a number as the third argument in order to look for the first matching value in the array after the given index.

		```
		>>> _.indexOf([1, 2, 3, 1, 2, 3], 2)
		1
		```

		"""
		# I could have relied on findIndex, but this is way simpler. Actually, I could have
		# also used the built-in facility, but the lastIndexOf cannot be done that way, so
		# I kept this for the sake of symmetry, but also to use bisect for large arrays
		if type(isSorted) is BooleanType and isSorted:
			return underscore._index_sorted(array, value)
		else:
			start = 0 if (type(isSorted) is BooleanType and isSorted is False) or type(isSorted) is not IntType else isSorted
			for i in xrange(start, len(array)):
				if array[i] == value :
					return i
			return -1

	@staticmethod
	def lastIndexOf(array, value, fromIndex = None):
		"""
		Returns the index of the last occurrence of value in the array, or -1 if value is not present. Pass fromIndex to start your search at a given index.

		```
		>>> _.lastIndexOf([1, 2, 3, 1, 2, 3], 2)
		4
		```
		"""
		start = len(array) if fromIndex is None else fromIndex
		for i in xrange(start-1, -1, -1):
			if array[i] == value :
				return i
		return -1

	@staticmethod
	def sortedIndex(array, value, iteratee = None, context = None):
		"""
		Determine the index at which the value should be inserted into the list in order to maintain the list's sorted order. If an iteratee function is provided, it will be used to compute the sort ranking of each value, including the value you pass. The iteratee may also be the string name of the key to sort by.

		```
		>>> _.sortedIndex([10, 20, 30, 40, 50], 35)
		3
		>>> stooges2 = [{'name': 'moe', 'age': 40}, {'name': 'curly', 'age': 60}]
		>>> _.sortedIndex(stooges2, {'name': 'larry', 'age': 50}, 'age')
		1
		```
		"""
		# The version with a real iteratee is inefficient for larger arrays.
		# Ideally, the bisect module should be rewritten to use the iteratee directly. T.B.D.
		if iteratee is None:
			a = array
			v = value
		else :
			a = [ underscore._exec1(iteratee, context, x) for x in array ]
			v = underscore._exec1(iteratee, context, value)
		return bisect.bisect_left(a, v)

	@staticmethod
	def findIndex(array, predicate, context = None):
		"""
		Similar to _.indexOf, returns the first index where the predicate truth test passes; otherwise returns -1.

		```
		>>> def isPrime(n):
		...
		...
		>>> _.findIndex([4, 6, 8, 12], isPrime)
		-1
		>>> _.findIndex([4, 6, 7, 12], isPrime)
		2
		"""
		for i in xrange(0, len(array)):
			if underscore._exec1(predicate, context, array[i]):
				return i
		return -1

	@staticmethod
	def findLastIndex(array, predicate, context = None):
		"""
		Like _.findIndex but iterates the array in reverse, returning the index closest to the end where the predicate truth test passes.
		```
		>>> _.findLastIndex([4,6,5,7,12],isPrime)
		3
		```
		"""
		for i in xrange(len(array)-1,-1,-1):
			if underscore._exec1(predicate, context, array[i]):
				return i
		return -1

	@staticmethod
	def range(*args):
		"""
		A function to create flexibly-numbered lists of integers, handy for each and map loops. start, if omitted, defaults to 0; step defaults to 1. Returns a list of integers from start (inclusive) to stop (exclusive), incremented (or decremented) by step, exclusive. Note that ranges that stop before they start are considered to be zero-length instead of negative — if you'd like a negative range, use a negative step.

		This is just an alias to the built-in **range** function.

		```
		>>> _.range(10)
		[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		>>> _.range(3,10)
		[3, 4, 5, 6, 7, 8, 9]
		>>> _.range(3,10,2)
		[3, 5, 7, 9]
		>>>
		```

		"""
		return range(*args)

	###############################################################################
	#                             Function Functions                              #
	###############################################################################


	@staticmethod
	def partial(func, *args, **keywords):
		"""
		Partially apply a function by filling in any number of its arguments and keywords. You may pass `None` in your list of arguments to specify an argument that should not be pre-filled, but left open to supply at call-time.

		```
		>>> substract = lambda a,b: b-a
		>>> sub5 = _.partial(substract, 5)
		>>> sub5(20)
		15
		>>> subFrom20 = _.partial(substract, None, 20)
		>>> subFrom20(5)
		15
		```
		"""
		def combine(a,b):
			retval = ()
			for i in xrange(0,len(a)):
				if a[i] is None:
					retval += tuple([b[0]])
					b = b[1:]
				else:
					retval += tuple([a[i]])
			return retval + b
		def newfunc(*fargs,**fkeywords):
			newkeywords = keywords.copy()
			newkeywords.update(fkeywords)
			return func(*(combine(args,fargs)), **newkeywords)
		return newfunc

	@staticmethod
	def once(func):
		"""
		Creates a version of the function, as a callable object, that can only be called one time. Repeated calls to the modified function will have no effect, returning the value from the original call.

		```
		>>> initialize = _.once(createApplication)
		>>> initialize()
		created
		>>> initialize()
		>>>
		```
		"""
		return underscore.before(1, func)

	@staticmethod
	def after(count, func):
		"""
		Creates a version of the function, as a callable object, that will only be run after first being called count times. Useful for grouping asynchronous responses, where you want to be sure that all the async calls have finished, before proceeding.
		```
		>>> delayInit = _.after(2,createApplication)
		>>> delayInit()
		>>> delayInit()
		>>> delayInit()
		created
		>>>
		```
		"""
		class _after(object):
			def __init__(self, count, func):
				self.count  = count
				self.called = 0
				self.func   = func
			def __call__(self, *args, **keywords):
				if self.called == self.count:
					return self.func(*args, **keywords)
				else:
					self.called += 1
		return _after(count, func)

	@staticmethod
	def before(count, func):
		"""
		Creates a version of the function, as a callable object, that can be called no more than count times. The result of the last function call is memoized and returned when count has been reached.

		```
		>>> createOnly3 = _.before(3,createApplication)
		>>> createOnly3()
		created
		>>> createOnly3()
		created
		>>> createOnly3()
		created
		>>> createOnly3()
		>>>
		```
		"""
		class _before(object):
			def __init__(self, count, func):
				self.count  = count
				self.called = 0
				self.retval = None
				self.func   = func
			def __call__(self, *args, **keywords):
				if self.called < self.count:
					self.retval = self.func(*args, **keywords)
					self.called += 1
					return self.retval
				else:
					return self.retval
		return _before(count, func)

	@staticmethod
	def wrap(function, wrapper):
		"""
		Wraps the first function inside of the wrapper function, passing it as the first argument. This allows the wrapper to execute code before and after the function runs, adjust the arguments, and execute it conditionally.
		The generated functions can have arguments and keywords, which will be forwarded to the wrapper.

		```
		>>> func = lambda x: "Hello: " +x
		>>> def wra(f, *args, **keywords):
		...     print(args)
		...     print(keywords)
		...     print("before, " + f("name") + ", after")
		...
		>>> wrapper = _.wrap(func,wra)
		>>> wrapper(1,2,3,a=1)
		(1, 2, 3)
		{'a': 1}
		before, Hello: name, after
		```
		"""
		def ff(*args, **keywords):
			return(wrapper(function, *args, **keywords))
		return ff

	@staticmethod
	def negate(predicate, *args, **keywords):
		"""Returns a new negated version of the predicate function (invoked with the arguments).

		```
		>>> tst = lambda x,y: x and y
		>>> _.negate(tst,False,True)
		True
		>>> _.negate(tst,True,True)
		False
		```
		"""
		return not predicate(*args, **keywords) if hasattr(predicate, '__call__') else not predicate

	@staticmethod
	def compose(*functions):
		"""
		Returns the composition of a list of functions, where each function consumes the return value of the function that follows. In math terms, composing the functions f(), g(), and h() produces f(g(h())). The composition function can be invoked with arguments, which will be used for the arguments of the innermost function (h() in this example).

		```
		>>> greet    = lambda name: "hi: " + name
		>>> exclaim  = lambda statement: statement.upper() + "!"
		>>> welcome  = _.compose(greet, exclaim)
		>>> welcome('moe')
		'hi: MOE!'
		>>>
		```
		"""
		def ff(*args,**keywords):
			nextarg = functions[-1](*args,**keywords)
			for i in xrange(len(functions)-2,-1,-1):
				nextarg = functions[i](nextarg)
			return nextarg
		return ff

	# Aliases to the core method names
	forEach = each
	collect = map
	inject  = reduce
	detect  = find
	select  = filter
	any     = some
	include = contains
	unique  = uniq


if __name__ == '__main__':
	greet    = lambda name: "hi: " + name
	exclaim  = lambda statement: statement.upper() + "!"
	welcome  = underscore.compose(greet, exclaim)
	print welcome('moe')
