#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import sys

# Tricks to handle Python3
PY3 = sys.version_info.major > 2
if PY3:
    basestring = str


from types import *
import itertools
import random
import math
import bisect
from functools import reduce
from collections import Iterable

__version__ = 2.0

# noinspection PyCallByClass,PyShadowingBuiltins,PyPep8,PyPep8,PyPep8
class underscore(object):
	"""
    Methods usually have a usage example to make the description clearer. Conceptually, the following Python code precedes all examples::

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
        stooges = [{'name': 'moe',   'age': 40},
                   {'name': 'larry', 'age': 50},
                   {'name': 'curly', 'age': 60}]
        def createApplication():
            print("created")

    These structures are used in some of the examples and are listed here to avoid repeating their definition separately.

    A further simplification of the examples is the usage of the ``*args`` idioms. Many “iteratee” arguments represent a function with 3-4 arguments, per definition of the underscore method, but the example uses only the first few. Instead of::

        lambda name, index, list: ...

    the abbreviation::

        lambda name, *args: ...

    is sometimes used.
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
	def _extends(obj, ext):
		if isinstance(obj, dict) and isinstance(ext, dict):
			for key in ext:
				if key not in obj or obj[key] != ext[key]:
					return False
			return True
		return False

	@staticmethod
	def each(lst, iteratee, context = None):
		"""
        **Aliases**:
            :py:meth:`each`, :py:meth:`forEach`

        Iterates over a **lst** of elements, yielding each in turn to an **iteratee** function.
        Each invocation of **iteratee** is called with three arguments: if **lst** is of list type,
        then the arguments are ``(element, index, list)``; if it is of dictionary type
        the arguments are ``(value, key, list``). Returns **lst** for possible chaining.

        The method also works for an arbitrary iterator; however, in that case the **iteratee** is invoked
        with ``None`` for the second and third
        argument. In that case the return value of the method is also ``None``; i.e., no chaining is possible.

        Example:
            >>> def pr(element, index, list):
            ...	    print(element)
            >>> _.each([1, 2, 3], pr)
            1
            2
            3
            >>> _.each({'one': 11, 'two': 22, 'three': 33}, pr)
            33
            22
           11
        """
		if iteratee is None:
			return lst
		elif isinstance(lst, list):
			for i in range(0, len(lst)):
				underscore._exec3(iteratee, context, lst[i], i, lst)
			return lst
		elif isinstance(lst, dict):
			for key in lst:
				underscore._exec3(iteratee, context, lst[key], key, lst)
			return lst
		else:
			for value in lst:
				underscore._exec3(iteratee, context, value, None, None)
			return None

	@staticmethod
	def map(lst, iteratee = None, context = None):
		"""
        **Aliases**:
            :py:meth:`map`, :py:meth:`collect`

        Produces a *new* array of values by mapping each value in **lst** through a transformation
        function (**iteratee**). Similarly to :py:meth:`each`, the **iteratee** is passed three arguments:
        the ``value``, then the ``index`` (or ``key``) of the iteration, and finally a reference to the entire list.

        The method also works for an arbitrary iterator; however, in that case the **iteratee** is invoked
        with ``None`` for the second and third argument.

        Example:
            >>> _.map([1, 2, 3], lambda num, index, list: num * 3)
            [3, 6, 9]
            >>> _.map({'one': 1, 'two': 2, 'three': 3}, lambda val, key, *args: val * 4)
            [12, 8, 4]
            >>> _.map([[1, 2], [3, 4]], lambda a, *args: _.first(a))
            [1, 3]
        """
		if iteratee is None:
			return lst
		elif isinstance(lst, list):
			return [underscore._exec3(iteratee, context, lst[i], i, lst) for i in range(0, len(lst))]
		elif isinstance(lst, dict):
			return [underscore._exec3(iteratee, context, lst[key], key, lst) for key in lst]
		else:
			return [underscore._exec3(iteratee, context, value, None, None) for value in lst]

	@staticmethod
	def reduce(lst, iteratee, memo = None, context = None):
		"""
        **Aliases**:
            :py:meth:`reduce`, :py:meth:`inject`

        Reduce boils down a **lst** of values into a single value that is returned. **memo** is the initial state
        of the reduction, and each successive step of it should be returned by **iteratee**. The **iteratee** is
        passed four arguments: ``memo`` (ie, the current state of reduction), then the ``value`` and ``index``
        (or ``key``) of the iteration, and finally a reference to the entire list.

        If no memo is passed to the initial invocation of reduce, **iteratee** is not invoked on the first element
        of the list. The first element is instead passed as the ``memo`` in the invocation of the **iteratee** on
        the next element in the list. In the case of a dictionary this means the first element of the keys, which is n
        ot deterministic (unless an ordered dictionary is used)

        Example:
            >>> _.reduce([1, 2, 3], lambda memo, num, *args: memo + num, 1)
            7
            >>> _.reduce([1, 2, 3], lambda memo, num, *args: memo + num)
            6
            >>> _.reduce({'one':1,'two':2,'three':3,'four':4},lambda memo, value, *args: memo*value, 2)
            48
            >>> _.reduce({'one':1,'two':2,'three':3,'four':4},lambda memo, value, *args: memo*value)
            24
        """
		if isinstance(lst, list):
			if memo is None:
				if len(lst) == 0:
					raise IndexError("empty list with no initial value")
				else :
					return reduce(lambda m, i: underscore._exec4(iteratee, context, m, lst[i], i, lst), range(1, len(lst)), lst[0])
			else:
				return reduce(lambda m, i: underscore._exec4(iteratee, context, m, lst[i], i, lst), range(0, len(lst)), memo)
		elif isinstance(lst, dict):
			if memo is None:
				if len(lst) == 0:
					raise IndexError("empty dict with no initial value")
				else:
					keys = list(lst.keys()) if PY3 else lst.keys()
					return reduce(lambda m, key : underscore._exec4(iteratee, context, m, lst[key], key, lst), keys[1:], lst[keys[0]])
			else:
				return reduce(lambda m, key: underscore._exec4(iteratee, context, m, lst[key], key, lst), iter(lst), memo)
		else:
			return TypeError("should be a list or a dict")

	@staticmethod
	def find(lst, predicate, context = None):
		"""
        **Aliases**:
            :py:meth:`find`, :py:meth:`detect`

        Looks through each value in the **lst**, returning the first one that passes a truth test (**predicate**),
        or ``None`` if no value passes the test. The function returns as soon as it finds an acceptable
        element, and doesn't traverse the entire list.

        Example:
            >>> _.find([1, 2, 3, 4, 5, 6], lambda num: num % 2 == 0)
            2
        """
		if isinstance(lst, Iterable):
			for x in lst:
				if underscore._exec1(predicate, context, x):
					return x
			return None
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def filter(lst, predicate, context = None):
		"""
        **Aliases**:
            :py:meth:`filter`, :py:meth:`select`

        Looks through each value in the **lst**, returning an array of all the values that pass a
        truth test (**predicate**).

        Example:
            >>> _.filter([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0)
            [2, 4, 6]
        """
		if isinstance(lst, Iterable):
			return [x for x in lst if underscore._exec1(predicate, context, x)]
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def where(lst, properties):
		"""
        Looks through each value in the **lst**, returning an array of all the values that contain all of
        the key-value pairs listed in **properties**.

        Example:
            >>> _.where(listOfPlays, {'author': "Shakespeare", 'year': 1611})
            [{'title': 'The tempest', 'year': 1611, 'author': 'Shakespeare'}, {'title': 'Cymbeline', 'year': 1611, 'author': 'Shakespeare'}]
        """
		if isinstance(lst, Iterable):
			return [x for x in lst if underscore._extends(x, properties)]
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def findWhere(lst, properties):
		"""
        Looks through the **lst** and returns the *first* value that matches all of the key-value pairs
        listed in **properties**.

        Example:
            >>> _.findWhere(listOfPlays, {'author': "Shakespeare", 'year': 1611})
            {'title': 'The tempest', 'year': 1611, 'author': 'Shakespeare'}
        """
		if isinstance(lst, Iterable):
			for x in lst:
				if underscore._extends(x, properties):
					return x
			return None
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def reject(lst, predicate, context = None):
		"""
        Returns the values in **lst** without the elements that the truth test (**predicate**) passes. The opposite of :py:meth:`filter`.

        Example:
            >>> _.reject([1, 2, 3, 4, 5, 6], lambda num: num % 2 == 0)
            [1, 3, 5]
        """
		if isinstance(lst, Iterable):
			return [x for x in lst if not underscore._exec1(predicate, context, x)]
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def every(lst, predicate = lambda x: x, context = None):
		"""
        Returns true if all of the values in the **lst** pass the **predicate** truth test. The default predicate is the identity.

        Example:
            >>> _.every([True, 1, None, 'yes'], _.identity)
            False
        """
		if isinstance(lst, Iterable):
			for x in lst:
				if not underscore._exec1(predicate, context, x):
					return False
			return True
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def some(lst, predicate = lambda x: x, context = None):
		"""
        **Aliases**:
            :py:meth:`some`, :py:meth:`any`

        Returns ``True`` if any of the values in the **lst** pass the predicate truth test.
        Short-circuits and stops traversing the list if a true element is found.
        The default predicate is the identity.

        Example:
            >>> _.some([None, 0, True, False])
            True
        """
		if isinstance(lst, Iterable):
			for x in lst:
				if underscore._exec1(predicate, context, x):
					return True
			return False
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def contains(lst, value):
		"""
        **Aliases**:
            :py:meth:`contains`, :py:meth:`include`

        Returns ``True`` if the value is present in the list.
        """
		return value in lst

	@staticmethod
	def pluck(lst, propertyName):
		"""
        A convenient version of what is perhaps the most common use-case for :py:meth:`map`:
        extracting a list of property values from an array of dictionaries.

        Example:
            >>> _.pluck(stooges, 'name')
            ['moe', 'larry', 'curly']
        """
		return [l[propertyName] for l in lst]

	@staticmethod
	def max(lst, iteratee = None, context = None):
		"""
        Returns the maximum value in **lst**. If an **iteratee** function is provided,
        it will be used on each value to generate the criterion by which the value is ranked.
        ``float("inf")`` is returned if list is empty.

        Example:
           >>>> _.max([1,2,3,4])"
            4
            >>>> _.max([1,2,3,4], lambda x: -x)
            1
            >>>> _.max([])
            inf
            >>>> .max(stooges, lambda stooge: stooge['age'])
           {'name': 'moe', 'age': 40}
         """
		if isinstance(lst, Iterable):
			if lst is None or len(lst) == 0:
				return float("inf")
			if iteratee is None:
				return max(lst)
			else:
				return max(lst, key=lambda x: underscore._exec1(iteratee, context, x))
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def min(lst, iteratee = None, context = None):
		"""
        Returns the min value in **lst**. If an **iteratee** function is provided,
        it will be used on each value to generate the criterion by which the value
        is ranked. ``float("-inf")`` is returned if list is empty, so an guard may be required.

        Example:
            >>>> _.min([1,2,3,4])"
            1
            >>>> _.min([1,2,3,4], lambda x: -x)
            4
            >>>> _.min([])
            -inf
            >>>> .min(stooges, lambda stooge: stooge['age'])
           {'name': 'curly', 'age': 60}
        """
		if isinstance(lst, Iterable):
			if lst is None or len(lst) == 0:
				return float("-inf")
			if iteratee is None:
				return min(lst)
			else:
				return min(lst, key=lambda x: underscore._exec1(iteratee, context, x))
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def sortBy(lst, iteratee = None, context = None):
		"""
        Returns a sorted copy of **lst**, ranked in ascending order by the results of running each
        value through **iteratee**. **iteratee** may also be the string name of the property.

        Example:
            >>> _.sortBy([1, 2, 3, 4, 5, 6], lambda num: math.sin(num))
            [5, 4, 6, 3, 1, 2]
            >>> _.sortBy(stooges, 'name')
            [{'age': 60, 'name': 'curly'}, {'age': 50, 'name': 'larry'}, {'age': 40, 'name': 'moe'}]
        """
		if iteratee is None:
			return sorted(lst)
		elif isinstance(iteratee, basestring):
			return sorted(lst, key=lambda x: x[iteratee])
		else:
			return sorted(lst, key=lambda x: underscore._exec1(iteratee, context, x))

	@staticmethod
	def _group(lst, iteratee, context):
		if isinstance(iteratee, basestring):
			func = lambda x: x[iteratee]
		else:
			func = lambda x: underscore._exec1(iteratee, context, x)

		retval = {}
		for x in lst:
			key = func(x)
			if key in retval:
				retval[key].append(x)
			else:
				retval[key] = [x]
		return retval


	@staticmethod
	def groupBy(lst, iteratee, context = None):
		"""
        Splits a **lst** into sets, grouped by the result of running each value through **iteratee**.
        If **iteratee** is a string instead of a function, groups by the property named by
        iteratee on each of the values.

        Example:
            >>> _.groupBy([1.3, 2.1, 2.4], lambda num: math.floor(num))
            {1.0: [1.3], 2.0: [2.1, 2.4]}
            >>> st2 = [{'name': 'joe', 'age': 40}, {'name': 'tom', 'age': 50}, {'name': 'bill', 'age': 50}]
            >>> _.groupBy(st2, 'age')
            {40: [{'age': 40, 'name': 'joe'}], 50: [{'age': 50, 'name': 'tom'}, {'age': 50, 'name': 'bill'}]}
        """
		if isinstance(lst, Iterable):
			return underscore._group(lst, iteratee, context)
		else:
			raise TypeError("lst must be iterable")

	@staticmethod
	def indexBy(lst, iteratee, context = None):
		"""
        Given a **lst**, and an **iteratee** function that returns a key for each element in the
        list (or a property name), returns an object with an index of each item. Just
        like :py:meth:`groupBy`, but when you know your keys are unique.

        Example:
            >>> _.indexBy(stooges, 'age')
            {40: {'age': 40, 'name': 'moe'}, 50: {'age': 50, 'name': 'larry'}, 60: {'age': 60, 'name': 'curly'}}
        """
		if isinstance(lst, Iterable):
			grouped = underscore._group(lst, iteratee, context)
			return {g:grouped[g][0]  for g in grouped}
		else:
			raise TypeError("lst must be iterable")

	@staticmethod
	def countBy(lst, iteratee, context = None):
		"""
        Sorts a **lst** into groups and returns a count for the number of objects in each group.
        Similar to :py:meth:`groupBy`, but instead of returning a list of values, returns a count for the
        number of values in that group.

        Example:
            >>> _.countBy([1, 2, 3, 4, 5], lambda num: 'even' if num % 2 == 0 else 'odd')
            {'even': 2, 'odd': 3}
        """
		if isinstance(lst, Iterable):
			grouped = underscore._group(lst, iteratee, context)
			return {g: len(grouped[g]) for g in grouped}
		else:
			raise TypeError("lst must be iterable")


	@staticmethod
	def shuffle(lst):
		"""
        Returns a (randomly) shuffled copy of the **lst**.

        Example:
            >>> _.shuffle([1, 2, 3, 4, 5, 6])
            [6, 4, 5, 2, 1, 3]
        """
		indeces = list(range(0, len(lst)))
		random.shuffle(indeces)
		return [lst[i] for i in indeces]

	@staticmethod
	def sample(lst, n = None):
		"""
        Produce a random sample from the **lst**. Pass a number to return **n** random elements from the list. Otherwise a single random item will be returned.

        Example:
            >>> _.sample([1, 2, 3, 4, 5, 6])
            1
            >>> _.sample([1, 2, 3, 4, 5, 6], 3)
            [4, 1, 5]
        """
		return random.sample(lst, 1)[0] if n is None else random.sample(lst, n)

	@staticmethod
	def toArray(lst):
		"""
        Creates a real array from the **lst** (anything that can be iterated over).
		Useful for transmuting the arguments object. An alias to the built-in **list** function.

        Example:
            >>> _.toArray(range(0,4))
            [0, 1, 2, 3]
        """
		if isinstance(lst, Iterable):
			return list(lst)
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def size(lst):
		"""
        Return the number of values in the **lst**. An alias to the built-in *len* function.

        Example:
            >>> _.size({'one': 1, 'two': 2, 'three': 3})
            3
        """
		if isinstance(lst, Iterable):
			return len(lst)
		else:
			raise TypeError("argument must be Iterable")

	@staticmethod
	def partition(lst, predicate, context = None):
		"""
        Split **lst** into two arrays: one with elements that satisfy predicate and one with elements that do not satisfy **predicate**. If **lst** is actually a tuple, then a tuple is returned, otherwise an array, each containing the two generated arrays in the 'yes' and 'no' order.

        Example:
            >>> _.partition([0, 1, 2, 3, 4, 5], lambda num: num % 2 != 0)
            [[1, 3, 5], [0, 2, 4]]
			>>> _.partition((0, 1, 2, 3, 4, 5), lambda num: num % 2 != 0)
            ((1, 3, 5), (0, 2, 4))
        """
		yes = []
		no  = []
		if isinstance(lst, Iterable):
			for x in lst:
				if underscore._exec1(predicate, context, x) is True:
					yes.append(x)
				else:
					no.append(x)
			return (tuple(yes), tuple(no)) if type(lst) is tuple else [yes, no]
		else:
			raise TypeError("argument must be Iterable")


	###############################################################################
	#                                Array Functions                              #
	###############################################################################

	@staticmethod
	def first(array, n = None):
		"""Returns the first element of an **array**. Passing **n** will return the first n elements of the array.

        Example:
            >>> _.first([5, 4, 3, 2, 1])
            5
            >>> _.first([5, 4, 3, 2, 1],3)
            [5, 4, 3]
        """
		if isinstance(array, list):
			return array[0] if n is None else array[0:n]
		else:
			raise TypeError("argument must be a list")

	@staticmethod
	def initial(array, n = 1):
		"""Returns everything but the last entry of the **array**. Especially useful on the arguments object.
		Pass **n** to exclude the last n elements from the result.

        Example:
            >>> _.initial([5, 4, 3, 2, 1])
            [5, 4, 3, 2]
            >>> _.initial([5, 4, 3, 2, 1],3)
            [5, 4]
        """
		if isinstance(array, list):
			return array[:-n]
		else:
			raise TypeError("argument must be a list")

	@staticmethod
	def last(array, n = None):
		"""Returns the last element of **array**. Passing **n** will return the last n elements of the array.

        Example:
            >>> _.last([5, 4, 3, 2, 1])
            1
            >>> _.last([5, 4, 3, 2, 1],3)
            [3, 2, 1]
        """
		if isinstance(array, list):
			return array[-1] if n is None else array[-n:]
		else:
			raise TypeError("argument must be a list")

	@staticmethod
	def rest(array, n = 1):
		"""Returns the rest of the elements in an **array**. Pass an index to return
		the values of the array from that index onward.

        Example:
            >>> _.rest([5, 4, 3, 2, 1])
            [4, 3, 2, 1]
            >>> _.rest([5, 4, 3, 2, 1],3)
            [2, 1]
        """
		if isinstance(array, list):
			return array[n:]
		else:
			raise TypeError("argument must be a list")

	# noinspection PyShadowingNames
	@staticmethod
	def compact(array):
		"""
        Returns a copy of the **array** with all falsy values removed. ``False``, ``None``, 0, "" (empty string), and ``NaN`` for floats are all falsy.

        Example:
            >>> _.compact([0, 1, False, 2, '', 3, None, 4, float('nan'), 5])
            [1, 2, 3, 4, 5]
        """
		if isinstance(array, list):
			falsy = lambda x: x is None or x is False or x == "" or x == 0 or (type(x) is float and math.isnan(x))
			return [x for x in array if falsy(x) is not True]
		else:
			raise TypeError("argument must be a list")

	@staticmethod
	def flatten(array, shallow = False):
		"""Flattens a nested **array** (the nesting can be to any depth). If you pass **shallow** with value ``True``, the array is only be flattened a single level.

        Example:
            >>> _.flatten([1, [2], [3, [[4]]]])
            [1, 2, 3, 4]
            >>> _.flatten([1, [2], [3, [[4]]]], True)
            [1, 2, 3, [[4]]]
        """
		if isinstance(array, list):
			retval = []
			for x in array:
				if type(x) is list:
					retval +=  x if shallow else underscore.flatten(x)
				else:
					retval.append(x)
			return retval
		else:
			raise TypeError("argument must be a list")

	@staticmethod
	def without(array, *values):
		"""Returns a copy of the **array** with all instances in  ***values** removed.

        Example:
            >>> _.without([1, 2, 1, 0, 3, 1, 4], 0, 1)
            [2, 3, 4]
        """
		if isinstance(array, list):
			return [x for x in array if x not in values]
		else:
			raise TypeError("argument must be a list")

	@staticmethod
	def union(*arrays):
		"""
        Returns the union of the passed-in **arrays**: a list of unique items, in order,
		that are present in one or more of the **arrays**.

        Example:
            >>> _.union([1, 2, 3], [101, 2, 1, 10], [2, 1])
            [1, 2, 3, 101, 10]
        """
		if len(arrays) == 0:
			return []

		check = [True if isinstance(x, list) else False for x in arrays]
		if False in [True if isinstance(x, list) else False for x in arrays]:
			raise TypeError("all arguments must be arrays")
		else:
			if len(arrays) == 1:
				return [x for x in arrays[0]]
			else:
				retval = []
				for a in arrays:
					for x in a:
						if x not in retval:
							retval.append(x)
				return retval

	@staticmethod
	def intersection(*arrays):
		"""
        Returns the list of values that are the intersection of all the **arrays**.
		Each value in the result is present in each of the **arrays**.

        Example:
            >>> _.intersection([1, 2, 3], [101, 2, 1, 10], [2, 1])
            [1, 2]
        """
		if len(arrays) == 0:
			return []

		if False in [True if isinstance(x, list) else False for x in arrays]:
			raise TypeError("all arguments must be arrays")
		else:
			if len(arrays) == 1:
				return [x for x in arrays[0]]
			else:
				curr = arrays[0]
				retval = []
				for x in curr:
					to_be_added = True
					for Z in arrays[1:]:
						if x not in Z:
							to_be_added = False
							break
					if to_be_added: retval.append(x)
				return retval

	@staticmethod
	def difference(array, *others):
		"""
        Similar to :py:meth:`without`, but returns the values from **array** that are not present in the other arrays.

        Example:
            >>> _.difference([1, 2, 3, 4, 5], [5, 2, 10])
            [1, 3, 4]
        """
		if not isinstance(array, list):
			raise TypeError("argument must be an array")
		if len(others) == 0:
			return [x for x in array]

		if False in [True if isinstance(x, list) else False for x in others]:
			raise TypeError("all arguments must be arrays")
		else:
			retval = []
			for x in array:
				to_be_added = True
				for A in others:
					if x in A:
						to_be_added = False
						break
				if to_be_added: retval.append(x)
			return retval

	# noinspection PyShadowingNames,PyShadowingNames
	@staticmethod
	def uniq(array, iteratee = None, context = None):
		"""
        **Aliases**:
            :py:meth:`uniq`, :py:meth:`unique`

        Returns a duplicate-free version of the **array**, based on the **in** operator of Python's list. If you want to compute unique items after a transformation, pass an **iteratee** function (the retained element in the array will be the first one found).

        Example:
            >>> _.uniq([1, 2, 1, 3, 1, 4, 2])
            [1, 2, 3, 4]
			>>> _.uniq([1, 1, 1, 2, 3, 4, 4, 5], isSorted = True)
			[1, 2, 3, 4, 5]
			>>> _.uniq([1.5, 1.7, 2.0, 2.5, 2.5, 3.0, 4.0], iteratee = math.floor)
			[1.5, 2.0, 3.0, 4.0]
        """
		if not isinstance(array, list):
			raise TypeError("argument must be an array")

		if len(array) == 0:
			return []
		else:
			to_compare = (lambda x: x) if iteratee is None else (lambda x: underscore._exec1(iteratee, context, x))
			retval      = [array[0]]
			comparisons = [to_compare(array[0])]
			for x in array[1:]:
				y = to_compare(x)
				if y not in comparisons:
					retval.append(x)
					comparisons.append(y)
			return retval

	@staticmethod
	def zip(*arrays):
		"""
        Merges together the values of each of the **arrays** with the values at the
		corresponding position. Useful when you have separate data sources that
		are coordinated through matching array indexes. If the arguments are tuples,
		a tuple is returned in each position, otherwise an array.

        Example:
            >>> _.zip(['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False])
            [['moe', 30, True], ['larry', 40, False], ['curly', 50, False]]
            >>> _.zip(('moe', 'larry', 'curly'), (30, 40, 50), (True, False, False))
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)]
        """
		if False in [True if isinstance(x, list) or isinstance(x, tuple) else False for x in arrays]:
			raise TypeError("all arguments must be arrays")
		else:
			if PY3:
				zipped = list(zip(*arrays))
			else:
				zipped = zip(*arrays)
			return zipped if isinstance(arrays[0], tuple) else [list(x) for x in zipped]

	@staticmethod
	def object(array, values = None):
		"""
        Converts arrays into a dictionary and return it. Pass either a single list of ``[key, value]`` (or ``(key, value)``) pairs, or a list of keys, and a list of values. If duplicate keys exist, the last value wins.

		The first option is an alias to a possible ``dict`` constructor in Python.

        Example:
            >>> _.object([['moe', 30], ['larry', 40], ['curly', 50]])
            {'larry': 40, 'curly': 50, 'moe': 30}
            >>> _.object([('moe', 30), ('larry', 40), ('curly', 50)])
			{'larry': 40, 'curly': 50, 'moe': 30}
            >>> _.object(['moe', 'larry', 'curly'], [30, 40, 50])
            {'larry': 40, 'curly': 50, 'moe': 30}
        """
		if not isinstance(array, list):
			raise TypeError("all arguments must be arrays")
		if values is None:
			return dict(array)
		else:
			return {array[i]: values[i] for i in range(0, min(len(array), len(values)))}

	@staticmethod
	def indexOf(array, value, startIndex = 0, endIndex = None):
		"""
        Returns the index at which **value** can be found in the **array**, or -1 if value is not present in the **array**. The values of **startIndex** and **endIndex** may be used to refer to an interval where the search should be made.

        Example:
            >>> _.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2)
            1
			>>> _.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2, 3, 6)
			4
			_.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 10)
			-1
        """
		# I could have relied on findIndex, but this is way simpler. Actually, I could have
		# also used the built-in facility, but the lastIndexOf cannot be done that way, so
		# I kept this for the sake of symmetry, but also to use bisect for large arrays
		if not isinstance(array, list):
			raise TypeError("arguments must be a list")
		else:
			if endIndex is None:
				endIndex = len(array)
			try:
				return array.index(value, startIndex, endIndex)
			except ValueError:
				return -1

	@staticmethod
	def lastIndexOf(array, value, startIndex = 0, endIndex = None):
		"""
        Returns the index of the last occurrence of value in the **array**, or -1 if value is not present. The values of **startIndex** and **endIndex** may be used to refer to an interval where the search should be made.

        Example:
            >>> _.lastIndexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2)
            7
			>>> _.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2, 3, 6)
			4
        """
		if not isinstance(array, list):
			raise TypeError("arguments must be a list")
		start = len(array) if endIndex is None else endIndex
		end   = startIndex
		for i in range(start-1, end-1, -1):
			if array[i] == value:
				return i
		return -1

	@staticmethod
	def sortedIndex(array, value, iteratee = None, context = None):
		"""
        Determine the index at which the **value** should be inserted into the **array** in order to maintain the list's sorted order. If an **iteratee** function is provided, it will be used to compute the sort ranking of each value, including the value you pass. The **iteratee** may also be the string, providing the name of the key to sort by.

        Example:
            >>> _.sortedIndex([10, 20, 30, 40, 50], 35)
            3
			>>> _.sortedIndex([10, 20, 30, 40, 50], 55)
            5
            >>> stooges2 = [{'name': 'moe', 'age': 40}, {'name': 'curly', 'age': 60}]
            >>> _.sortedIndex(stooges2, {'name': 'larry', 'age': 50}, 'age')
            1
        """
		# The version with a real iteratee is inefficient for larger arrays.
		# Ideally, the bisect module should be rewritten to use the iteratee directly. T.B.D.
		if not isinstance(array, list):
			raise TypeError("arguments must be a list")
		if iteratee is None:
			a = array
			v = value
		else:
			a = [underscore._exec1(iteratee, context, x) for x in array]
			v = underscore._exec1(iteratee, context, value)
		return bisect.bisect_left(a, v)

	@staticmethod
	def findIndex(array, predicate, context = None, startIndex = 0, endIndex = None ):
		"""
        Similar to :py:meth:`indexOf`, returns the first index where the predicate truth test passes; otherwise returns -1. The values of **startIndex** and **endIndex** may be used to refer to an interval where the search should be made.

        Example:
            >>> def isPrime(n):
            ...     (— definition of the function)
            ...
            >>> _.findIndex([4, 6, 8, 12], isPrime)
            -1
            >>> _.findIndex([4, 6, 7, 12], isPrime)
            2
			>>> _.findIndex([4, 6, 3, 12, 14, 16], isPrime, startIndex=3)
			-1
			>>> _.findIndex([4, 6, 3, 12, 14, 16], isPrime, startIndex=1, endIndex=5)
			2
        """

		if not isinstance(array, list):
			raise TypeError("arguments must be a list")
		else:
			if endIndex is None:
				endIndex = len(array)

		for i in range(startIndex, endIndex):
			if underscore._exec1(predicate, context, array[i]):
				return i
		return -1

	@staticmethod
	def findLastIndex(array, predicate, context = None, startIndex = 0, endIndex = None):
		"""
        Like :py:meth:`findIndex` but iterates the array in reverse, returning the index closest to the end where the predicate truth test passes. The values of **startIndex** and **endIndex** may be used to refer to an interval where the search should be made.

        Example:
            >>> _.findLastIndex([4, 6, 5, 7, 12],isPrime)
            3
			>>> _.findLastIndex([2, 6, 7, 12, 13, 16], isPrime, startIndex = 1, endIndex = 3)
			2
        """
		if not isinstance(array, list):
			raise TypeError("arguments must be a list")
		else:
			if endIndex is None:
				endIndex = len(array)

		for i in range(endIndex - 1, startIndex - 1, -1):
			if underscore._exec1(predicate, context, array[i]):
				return i
		return -1

	@staticmethod
	def range(*args):
		"""
        A function to create flexibly-numbered lists of integers, handy for each and map loops. The combination of the arguments can be:

        * **end**: return a list of integers between 0 and **end**, with **end** non inclusive
        * **start**, **end**: like before but starting at **start** instead of 0
        * **start**, **end**, **step**: like before, but stepping with **step** instead of 1. **step** can also be negative

        This is just an alias to Python2's built-in **range** function. In Python3, the result of the same built-in is turned into a list before return.

        Example:
            >>> _.range(10)
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> _.range(3, 10)
            [3, 4, 5, 6, 7, 8, 9]
            >>> _.range(3, 10, 2)
            [3, 5, 7, 9]
        """
		return list(range(*args)) if PY3 else range(*args)

	###############################################################################
	#                             Function Functions                              #
	###############################################################################

	@staticmethod
	def partial(func, *args, **keywords):
		"""
        Return a partially bounded version of the function **func** by fixing any number of its arguments and keywords. You may pass ``None`` in your list of arguments to specify an argument that should not be pre-filled, but left open to supply at call-time.

        Example:
            >>> substract = lambda a, b: b - a
            >>> sub5 = _.partial(substract, 5)
            >>> sub5(20)
            15
            >>> subFrom20 = _.partial(substract, None, 20)
            >>> subFrom20(5)
            15
        """
		def combine(a, b):
			retval = ()
			for i in range(0, len(a)):
				if a[i] is None:
					retval += tuple([b[0]])
					b = b[1:]
				else:
					retval += tuple([a[i]])
			return retval + b

		def newfunc(*fargs, **fkeywords):
			newkeywords = keywords.copy()
			newkeywords.update(fkeywords)
			return func(*(combine(args, fargs)), **newkeywords)
		return newfunc

	@staticmethod
	def once(func):
		"""
        Creates a version of **func**, as a callable object, that can only be called one time. Repeated calls to the modified function will have no effect, returning the value from the original call.

        Example:
            >>> initialize = _.once(createApplication)
            >>> initialize()
            created
            >>> initialize()
            >>>
        """
		return underscore.before(1, func)

	@staticmethod
	def after(count, func):
		"""
        Creates a version of **func**, as a callable object, that will only be run after first being called **count** times.

        Example:
            >>> delayInit = _.after(2, createApplication)
            >>> delayInit()
            >>> delayInit()
            >>> delayInit()
            created
        """
		class _after(object):
			def __init__(self, after_count, after_func):
				self.count  = after_count
				self.called = 0
				self.func   = after_func

			def __call__(self, *args, **keywords):
				if self.called == self.count:
					return self.func(*args, **keywords)
				else:
					self.called += 1
		return _after(count, func)

	@staticmethod
	def before(count, func):
		"""
        Creates a version of **func**, as a callable object, that can be called no more than **count** times. The result of the last function call is memorized and returned when count has been reached.

        Example:
            >>> createOnly3 = _.before(3, createApplication)
            >>> createOnly3()
            created
            >>> createOnly3()
            created
            >>> createOnly3()
            created
            >>> createOnly3()
            >>>
        """
		class _before(object):
			def __init__(self, before_count, before_func):
				self.count  = before_count
				self.called = 0
				self.retval = None
				self.func   = before_func

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
        Wraps the first **function** inside of the **wrapper** function, passing it as the first argument. This allows the wrapper to execute code before and after the function runs, adjust the arguments, or execute it conditionally. The generated functions can have arguments and keywords, which will be forwarded to the **wrapper**.

        Example:
            >>> func = lambda x: "Hello: " +x
            >>> def wrap(f, *args, **keywords):
            ...     print(args)
            ...     print(keywords)
            ...     print("before, " + f("name") + ", after")
            ...
            >>> wrapper = _.wrap(func, wrap)
            >>> wrapper(1, 2, 3, a=1)
            (1, 2, 3)
            {'a': 1}
            before, Hello: name, after
        """
		def ff(*args, **keywords):
			return wrapper(function, *args, **keywords)
		return ff

	@staticmethod
	def negate(predicate, *args, **keywords):
		"""Returns a new negated version of the **predicate** function (invoked with the arguments).

        Example:
            >>> test = lambda x, y: x and y
            >>> _.negate(test,False,True)
            True
            >>> _.negate(test,True,True)
            False
        """
		return not predicate(*args, **keywords) if hasattr(predicate, '__call__') else not predicate

	@staticmethod
	def compose(*functions):
		"""
        Returns the composition of a list of **functions**, where each function consumes the return value of the function that follows. In math terms, composing the functions ``f()``, ``g()``, and ``h()`` produces ``f(g(h()))``. The composition function can be invoked with arguments, which will be used for the arguments of the innermost function (``h()`` in this example).

        Example:
            >>> greet    = lambda name: "hi: " + name
            >>> exclaim  = lambda statement: statement.upper() + "!"
            >>> welcome  = _.compose(greet, exclaim)
            >>> welcome('moe')
            'hi: MOE!'
            >>>
        """
		def ff(*args,**keywords):
			nextarg = functions[-1](*args, **keywords)
			for i in range(len(functions) - 2, -1, -1):
				nextarg = functions[i](nextarg)
			return nextarg
		return ff

	###############################################################################
	#                       Object (dictionary) Functions                         #
	###############################################################################

	@staticmethod
	def keys(object):
		"""Retrieve all the names of the **object**'s own enumerable properties. Alias of the built-in Python method, but in case of Python3, it returns a list and not an iterator.

        Example:
            >>> _.keys({'one': 1, 'two': 2, 'three': 3})
            ['three', 'two', 'one']
        """
		if not isinstance(object, dict):
			raise TypeError("argument must be a dictionary")
		return list(object.keys()) if PY3 else object.keys()

	@staticmethod
	def values(object):
		"""Retrieve all the names of the object's own enumerable properties. Alias of the built-in Python method.

        In Python3 this returns an iterator; in Python2 a list.

        Example:
            >>> _.values({'one': 1, 'two': 2, 'three': 3})
            [3,2,1]
        """
		if not isinstance(object, dict):
			raise TypeError("argument must be a dictionary")
		return list(object.values()) if PY3 else object.values()

	@staticmethod
	def mapObject(obj, iteratee = None, context = None):
		"""
		**Aliases**:
            :py:meth:`mapObject`, :py:meth:`collectObject`

		Like :py:meth:`map`, but for objects (a.k.a. dictionaries). Transform the value of each property in turn. The **iteratee** is passed three arguments: the ``index`` (or ``key``) of the iteration, the ``value``, and finally a reference to the entire list.
        If **iteratee** is not set or is ``None``, a copy of **obj** is returned.

        Example:
            >>> _.mapObject({'one': 1, 'two': 2, 'three': 3})
            {'one': 1, 'three': 3, 'two': 2}
            >>> _.mapObject({'one': 1, 'two': 2, 'three': 3}, lambda key, val, obj: 3*val)
            {'one': 3, 'three': 9, 'two': 6}
        """
		if not isinstance(obj, dict):
			raise TypeError("argument must be a dictionary")
		if iteratee is None:
			return underscore.clone(obj)
		else:
			transform = lambda key: underscore._exec3(iteratee, context, key, obj[key], obj)
			return {k: transform(k) for k in obj}

	@staticmethod
	def pairs(obj, tupl = False):
		"""Convert an **obj** into a list of ``[key, value]`` pairs. If the value of **tuple** is set to ``True``, an array of tuples is returned, instead of an array of (binary) arrays.

        In Python3 this returns an iterator; in Python2 a list.

        Example:
            >>> _.pairs({'one': 1, 'two': 2, 'three': 3})
            [['three', 3], ['two', 2], ['one', 1]]
            >>> _.pairs({'one': 1, 'two': 2, 'three': 3}, tupl = True)
            [('three', 3), ('two', 2), ('one', 1)]
        """
		if not isinstance(obj, dict):
			raise TypeError("argument must be a dictionary")
		else:
			if tupl:
				return list(obj.items()) if PY3 else obj.items()
			else:
				return [[k,v] for (k,v) in obj.items()]

	@staticmethod
	def invert(obj):
		"""Returns a copy of **obj** where the keys have become the values and the values the keys. For this to work, all of your object's values should be unique and string serializable.

        Example:
            >>> _.invert({"Moe": "Moses", "Larry": "Louis", "Curly": "Jerome"})
            {'Louis': 'Larry', 'Moses': 'Moe', 'Jerome': 'Curly'}
        """
		if not isinstance(obj, dict):
			raise TypeError("argument must be a dictionary")
		else:
			return {v:k for (k,v) in obj.items()}

	@staticmethod
	def findKey(obj, predicate, context = None):
		"""Returns the a key where the predicate truth test passes; if none found, returns ``None``.

        Example:
            >>> _.findKey({"Moe": "Moses", "Larry": "Louis", "Curly": "Jerome"}, lambda val: val == "Jerome")
            Curly
        """
		if not isinstance(obj, dict):
			raise TypeError("argument must be a dictionary")
		else:
			check = lambda val: underscore._exec1(predicate, context, val)
			for key in obj:
				if check(obj[key]):
					return key
			return None

	@staticmethod
	def extend(destination, *sources):
		"""Copy all of the properties in the source objects of **sources** over to the **destination** object. It's in-order, so the last source will override properties of the same name in previous arguments.  Returns **destination** (for possible chaining).

        Example:
            >>> _.extend({'name': 'moe', 'age': '40'}, {'age': 50}, {'age': 60, 'gender': 'male'})
            {'gender': 'male', 'age': 60, 'name': 'moe'}
        """
		if not isinstance(destination, dict) or (False in [isinstance(s, dict) for s in sources]):
			raise TypeError("arguments must be dictionaries")

		for source in sources:
			for key in source:
				destination[key] = source[key]
		return destination

	@staticmethod
	def extendOwn(destination, *sources):
		"""Like **extend**, but only copies *own* properties over to the destination object. Return **destination** (for possible chaining).

        Example:
            >>> _.extendOwn({'name': 'moe', age: '40'}, {'age': 50}, {'age': 60, 'gender': 'male'})
            {'age': 60, 'name': 'moe'}
        """
		if not isinstance(destination, dict) or (False in [isinstance(s, dict) for s in sources]):
			raise TypeError("arguments must be dictionaries")

		for source in sources:
			for key in source:
				if key in destination:
					destination[key] = source[key]
		return destination

	@staticmethod
	def pick(obj, *keys):
		"""
        Return a copy of **obj**, filtered to only have values for the whitelisted **keys** (or array of valid keys). Alternatively, accepts a predicate indicating which keys to pick.

        Example:
            >>> _.pick({'name': 'moe', 'age': 50, 'userid': 'moe1'}, 'name', 'age')
            {'age': 50, 'name': 'moe'}
            >>> a = ['name', 'age']
            >>> _.pick({'name': 'moe', 'age': 50, 'userid': 'moe1'}, *a)
            {'age': 50, 'name': 'moe'}
            >>> _.pick({'name': 'moe', 'age': 50, 'userid': 'moe1'}, lambda val, *args: _.isNumber(val))
            {'age': 50}
        """
		if not isinstance(obj, dict):
			raise TypeError("argument must be a dictionary")
		if len(keys) == 0:
			return {}
		elif hasattr(keys[0], '__call__'):
			return {key: obj[key] for key in obj if keys[0](obj[key], key, obj)}
		else:
			return {key: obj[key] for key in obj if key in keys}

	@staticmethod
	def omit(obj, *keys):
		"""
        Return a copy of **obj**, filtered to omit values for the blacklisted **keys** (or array of valid keys). Alternatively accepts a predicate indicating which keys to pick.

        Example:
            >>> _.omit({'name': 'moe', 'age': 50, 'userid': 'moe1'}, 'name', 'age')
            {'userid': 'moe1'}
            >>> a = ['name', 'age']
            >>> _.omit({'name': 'moe', 'age': 50, 'userid': 'moe1'}, *a)
            {'userid': 'moe1'}
            >>> _.omit({'name': 'moe', 'age': 50, 'userid': 'moe1'}, lambda val, *args: _.isNumber(val))
            {'userid': 'moe1', 'name': 'moe'}
        """
		if not isinstance(obj, dict):
			raise TypeError("argument must be a dictionary")
		if len(keys) == 0:
			return {}
		elif hasattr(keys[0], '__call__'):
			return {key: obj[key] for key in obj if not keys[0](obj[key], key, obj)}
		else :
			return {key: obj[key] for key in obj if key not in keys}

	@staticmethod
	def defaults(obj, *defaults):
		"""Fill in undefined properties in **obj** with the first value present in the following list of **defaults** objects. Return **obj** (for possible chaining)

        Example:
            >>> iceCream = {'flavor': "chocolate"}
            >>> _.defaults(iceCream, {'flavor': "vanilla", 'sprinkles': "lots"})
            {'flavor': 'chocolate', 'sprinkles': 'lots'}
			>>> myDefaults = [{'flavor':'vanilla', 'sprinkles':'lots'}, {'toGo': True}]
			>>> _.defaults(iceCream, *myDefaults)
			{'flavor': 'chocolate', 'sprinkles': 'lots', 'toGo' : True}
        """
		if not isinstance(obj, dict) or (False in [isinstance(s, dict) for s in defaults]):
			raise TypeError("arguments must be dictionaries")

		for default in defaults:
			for key in default:
				if key not in obj :
					obj[key] = default[key]
		return obj

	@staticmethod
	def clone(obj, deep = True):
		"""
        Create a clone of the provided plain **obj**. If ``deep`` is False, then any nested objects or arrays will be copied by reference, not duplicated; otherwise each constituent arrays or dictionaries will also be cloned (recursively).
        """
		import copy
		return copy.deepcopy(obj) if deep else copy.copy(obj)

	@staticmethod
	def has(obj, key):
		"""Return ``True`` if the object contain the given key, ``False`` otherwise. Alias to built in dictionary method"""
		return key in obj

	@staticmethod
	def property(key):
		"""
		**Aliases**:
            :py:meth:`property`, :py:meth:`attribute`

		Returns a function that will itself return the **key** property of any passed-in object.

        Example:
            >>> getName = _.property('name')
            >>> getName(stooges[0])
            moe
            >>> getName(stooges[1])
            larry
        """
		return lambda obj: obj[key]

	@staticmethod
	def propertyOf(obj):
		"""
		**Aliases**:
            :py:meth:`propertyOf`, :py:meth:`attributeOf`

		Inverse of :py:meth:`property`. Takes an **obj** and returns a function which will return the value of a provided property. In effect, the functional equivalent of ``obj[key]`` where ``obj`` is fixed.

        Example:
            >>> getValue = _.propertyOf(stooges[0])
            >>> getValue('name')
            moe
        """
		return lambda key: obj[key]

	@staticmethod
	def matcher(attrs):
		"""Returns a predicate function that will tell if a passed object contains all of the key/value properties present in **attrs**.

        Example:
            >>> checkAge = _.matcher({'age': 60})
			>>> checkAge(stooges[0])
			False
			>>> CheckAge(stooges[2])
			True
        """
		if not isinstance(attrs, dict):
			raise TypeError("argument must be a dictionary")

		def func(obj):
			for k in attrs:
				if k not in obj or obj[k] != attrs[k]:
					return False
			return True
		return func

	@staticmethod
	def isMatch(obj, properties):
		"""Returns ``True`` if the keys and values in **properties** are contained in **obj**, ``False`` otherwise.

        Example:
            >>> _.isMatch(stooge[0], {'age': 40})
            True
        """
		if not isinstance(obj, dict) or not isinstance(properties, dict):
			raise TypeError("arguments must be dictionaries")
		return underscore.matcher(properties)(obj)

	@staticmethod
	def isEqual(obj, other):
		"""Performs an optimized deep comparison between **obj** and **other**, returns ``True`` if they are equal, ``False`` otherwise."""
		return obj == other

	@staticmethod
	def isEmpty(obj):
		"""Returns ``True`` if an enumerable object contains no values (no enumerable own-properties), ``False`` otherwise. For strings and array-like objects the function checks if the length property is 0."""
		return len(obj) == 0

	@staticmethod
	def isArray(obj):
		"""Return ``True`` if **obj** is an Array (i.e., List), ``False`` otherwise."""
		return isinstance(obj, list)

	@staticmethod
	def isTuple(obj):
		"""Return ``True`` if **obj** is an Tuple, ``False`` otherwise."""
		return isinstance(obj, tuple)

	@staticmethod
	def isObject(obj):
		"""Return ``True`` if **obj** is an “Object” (i.e., Dictionary), ``False`` otherwise."""
		return isintance(obj, dict)

	@staticmethod
	def isFunction(obj):
		"""Return ``True`` if **obj** is a function or a method, ``False`` otherwise.

        Example:
            >>> _.isFunction(isPrime)
            True
			>>> _.isFunction(lambda x: x+1)
            True
			>>> _.isFunction(1)
            False
		"""
		return isinstance(obj, (LambdaType, FunctionType, MethodType))

	@staticmethod
	def isCallable(obj):
		"""Return ``True`` if **obj** is callable, ``False`` otherwise. Note that this is a more general form of test than :py:meth:`isFunction`"""
		return hasattr(obj, '__call__')

	@staticmethod
	def isString(obj):
		"""Return ``True`` if **obj** is a string, ``False`` otherwise. For Python2 this checks against a string or a unicode. In (Python3 there is no such distinction.)"""
		return isinstance(obj, basestring)

	@staticmethod
	def isNumber(obj):
		"""Return ``True`` if **obj** is a number (float or integer), ``False`` otherwise."""
		return isinstance(obj, (int, float))

	@staticmethod
	def isFinite(obj):
		"""Return ``True`` if **obj** is number with a finite value, ``False`` otherwise."""
		return isinstance(obj, (int, float)) and not math.isinf(obj)

	@staticmethod
	def isNaN(obj):
		"""Return ``True`` if **obj** is a float with ``NaN`` as value, ``False`` otherwise."""
		return isinstance(obj, float) and math.isnan(obj)

	@staticmethod
	def isBoolean(obj):
		"""Return ``True`` if **obj** is a Boolean, ``False`` otherwise."""
		return isinstance(obj, bool)

	@staticmethod
	def isError(obj):
		"""Return ``True`` if **obj** is an Exception, ``False`` otherwise."""
		return isinstance(obj, Exception)

	@staticmethod
	def isNone(obj):
		"""Return ``True`` if **obj** is ``None``, ``False`` otherwise."""
		return obj is None

	###############################################################################
	#                              Utility Functions                              #
	###############################################################################

	@staticmethod
	def identity(x, *args, **keywords):
		"""Returns the same value that is used as the first argument (and ignore everything else). In math: ``f(x) = x``. This function looks useless, but can be used when debugging other underscore methods."""
		return x

	@staticmethod
	def constant(value):
		"""
        Returns a function that always returns the same **value**.

        Example:
            >>> stooge = {'name': 'moe' }
            >>> const = _.constant(stooge)
            >>> const()
            {'name': 'moe'}
        """
		return lambda *args: value

	@staticmethod
	def noop(*args):
		"""Returns ``None`` irrespective of the arguments passed to it. Useful as the default for optional callback arguments."""
		return None

	@staticmethod
	def times(n, iteratee, context = None):
		"""
        Invokes the given **iteratee** function **n** times. Each invocation of **iteratee** is called with an index argument. Produces an array of the returned values.

        Example:
            >>> _.times(3, _.identity)
            [0, 1, 2]
        """
		return [underscore._exec1(iteratee, context, i) for i in range(0, n)]

	@staticmethod
	def random(min, max = None):
		"""Returns a pseudo-random integer between **min** and **max**, inclusive. If you only pass one argument, it will return a number between 0 and that number. The pseudo-random generator should not be used for security purposes."""
		if isinstance(min, int) and (max is None or isinstance(max,int)) :
			return random.randint(0, min) if max is None else random.randint(min, max)
		else:
			raise TypeError("arguments should be integeters")

	@staticmethod
	def uniqueId(prefix = None):
		"""
        Returns a globally-unique id as a string. If **prefix** is passed, the id will be appended to it. The method relies on the ``uuid.uuid1()`` library function, i.e., is based on the host ID and the current time.
        """
		import uuid
		return str(prefix) + str(uuid.uuid1()) if prefix is not None else str(uuid.uuid1())

	@staticmethod
	def now():
		"""Returns an integer timestamp for the current time"""
		import time
		return int(time.time())

	###############################################################################
	#                                    Chaining                                 #
	###############################################################################

	# Chaining is done by creating an instance of underscore, and catching all method requests
	def __init__(self, val):
		self.current_value = val
		self.chaining_on   = True

	# This method catches **all** attribute dereference attempts. This means that any access to the local variables
	# must be done through the superclass and through the special attributes. A bit convoluted, but does the job...
	def __getattribute__(self, name):
		if name == "value":
			# noinspection PyCallByClass
			def func():
				#
				# i.e.:
				# self.chaining_on = True
				# return self.current_value
				#
				object.__setattr__(self, 'chaining_on', False)
				return object.__getattribute__(self, 'current_value')
			return func
		elif name == "tap":
			def func(f):
				#
				# i.e.:
				# f(self.current_value)
				# return self
				#
				f(object.__getattribute__(self, 'current_value'))
				return self
			return func
		elif name == "__module__" or name == "__doc__" or name not in underscore.__dict__:
			raise AttributeError(name)
		elif object.__getattribute__(self, 'chaining_on'):
			def func(*args):
				#
				# I.e. (approximately)
				# self.current_value = underscore.`name`(self.current_value,*args)
				# return self
				#
				object.__setattr__(self, 'current_value', underscore.__dict__[name].__func__(object.__getattribute__(self, 'current_value'), *args))
				return self
			return func
		else:
			raise AttributeError("Chained value already retrieved, no more chaining")

	@staticmethod
	def chain(obj):
		"""
        Returns a wrapper object for chaining; see the separate description on chaining. The returned object has, beyond the static underscore methods, the additional instance methods:

        **value()**
             Extract the value of the wrapper object. A call to value means that no more chaining is possible.

        **tap(func)**
            Execute the function **func** on the value of the wrapped object; the object itself is returned, and can be used for further chaining. This can be used to 'tap into' the chain.

        Examples:
            >>> _.chain(stooges).sortBy('age').map(lambda st, *args: "%s is %s" % (st['name'], st['age'])).first().value()
            moe is 40
            >>> def pr(a):
            ...        print("intermediate: %s" % a)
            ...
            >>> _.chain([1, 2, 3, 200]).filter(lambda num, *args: num % 2 == 0).map(lambda x, *args: x*x).value()
            [4, 40000]
            >>> _.chain([1, 2, 3, 200]).filter(lambda num, *args: num % 2 == 0).tap(pr).map(lambda x, *args: x*x).value()
            intermediate: [2, 200]
            [4, 40000]
        """
		return underscore(obj)

	###############################################################################
	#                                   Aliases                                   #
	###############################################################################

	# Aliases to some of the core method names
	forEach       = each
	collect       = map
	collectObject = mapObject
	inject        = reduce
	detect        = find
	select        = filter
	any           = some
	include       = contains
	unique        = uniq
	attribute     = property
	attributeOf   = propertyOf

if __name__ == '__main__':
	pr = lambda a: print('intermediate: %s' % a)
	print(underscore.chain([1, 2, 3, 200]).filter(lambda num, *args: num % 2 == 0).map(lambda x, *args: x*x).value())
