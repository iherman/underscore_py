#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import sys
# Tricks to handle Python3
PY3 = sys.version_info.major > 2

from underscore import underscore as _
import math
from collections import OrderedDict

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
stooges = [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}, {'name':'joe', 'age':60}]
stooges0 = [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}]


class OneTest:
	def __init__(self, testName, toExpect, toDisplay, toEval, supressOutput = False):
		glob = globals()
		self.name      = testName
		pr = lambda name, variable: "  >>> %s = %s" % (name, variable)
		self.toDisplay = [pr(k, x) for x in toDisplay for k in glob if glob[k] == x]
		self.toExpect  = toExpect
		self.toEval    = toEval
		self.supressOutput = supressOutput

	def execute_and_display(self):
		print("\n= Test: '%s' =" % self.name)
		if self.toExpect and len(self.toExpect) != 0:
			print("Expected:\n  >>> " + self.toExpect)
		print("Test run:")
		if self.toDisplay is not None and len(self.toDisplay) != 0:
			_.forEach(self.toDisplay, lambda x, *args: print(x))
		print("  >>> " + self.toEval)
		if self.supressOutput:
			eval(self.toEval)
		else:
			print("  >>> " + str(eval(self.toEval)))







_tests = [
	(
		"each",
		[
			OneTest(
					"each with list",
				    "1\n2\n3",
					[],
					"_.each([1, 2, 3], lambda x,*args: print(x))",
					True
			),

			OneTest(
					"each with dict",
					"33\n22\n11",
					[],
					"_.each({'one': 11, 'two': 22, 'three': 33}, lambda x,*args: print(x))",
					True
			)
		]
	),

	(
		"map",
		[
			OneTest(
					"map with list",
					"[3, 6, 9]",
					[],
					"_.map([1, 2, 3], lambda num, index, list: num * 3)"
			),

			OneTest(
					"map with dict",
					"[12, 8, 4] (in some order!)",
					[],
					"_.map({'one': 1, 'two': 2, 'three': 3}, lambda val, key, *args: val * 4)"
			),

			OneTest(
					"map with no iterator function",
					"[1, 2, 3, 4]",
					[],
					"_.map([1, 2, 3, 4])"
			)
		]
	),
	(
		"reduce",
		[
			OneTest(
					"reduce with list",
					"7",
					[],
					"_.reduce([1, 2, 3], lambda memo, num, *args: memo + num, 1)"
			),
			OneTest(
					"reduce with list",
					"6",
					[],
					"_.reduce([1, 2, 3], lambda memo, num, *args: memo + num)"
			),
			OneTest(
					"reduce with dictionary",
					"48",
					[],
					"_.reduce({'one':1,'two':2,'three':3,'four':4},lambda memo, value, *args: memo*value, 2)"
			),
			OneTest(
					"reduce with dictionary",
					"[2, 4, 6]",
					[],
					"_.reduce({'one':1,'two':2,'three':3,'four':4},lambda memo, value, *args: memo*value)"
			),
		]
	),
	(
		"find",
		[
			OneTest(
					"find with list",
					"2",
					[],
					"_.find([1, 2, 3, 4, 5, 6], lambda num: num % 2 == 0)"
			),
		]
	),
	(
		"filter",
		[
			OneTest(
					"filter with list",
					"2",
					[],
					"_.filter([1, 2, 3, 4, 5, 6], lambda num, *args: num % 2 == 0)"
			),
		]
	),
	(
		"where",
		[
			OneTest(
					"where with dictionary",
					"[{'title': 'The tempest', 'year': 1611, 'author': 'Shakespeare'}, {'title': 'Cymbeline', 'year': 1611, 'author': 'Shakespeare'}]",
					[listOfPlays],
					"_.where(listOfPlays, {'author': 'Shakespeare', 'year': 1611})"
			),
		]
	),
	(
		"findWhere",
		[
			OneTest(
					"findWhere with dictionary",
					"{'title': 'The tempest', 'year': 1611, 'author': 'Shakespeare'}",
					[listOfPlays],
					"_.findWhere(listOfPlays, {'author': 'Shakespeare', 'year': 1611})"
			),
		]
	),
	(
		"every",
		[
			OneTest(
					"every with a list",
					"False",
					[],
					"_.every([True, 1, None, 'yes'], _.identity)"
			),
			OneTest(
					"every with a list with default predicate",
					"False",
					[],
					"_.every([True, 1, None, 'yes'])"
			),
		]
	),
	(
		"some",
		[
			OneTest(
					"some with a list",
					"True",
					[],
					"_.some([None, 0, True, False])"
			),
		]
	),
	(
		"pluck",
		[
			OneTest(
					"pluck from a directory",
					"['moe', 'larry', 'curly', 'joe']",
					[stooges],
					"_.pluck(stooges, 'name')"
			),
		]
	),
	(
		"max",
		[
			OneTest(
					"max on a list",
					"4",
					[],
					"_.max([1,2,3,4])"
			),
			OneTest(
					"max on a list with predicate",
					"1",
					[],
					"_.max([1,2,3,4], lambda x: -x)"
			),
			OneTest(
					"max on an empty list",
					"inf",
					[],
					"_.max([])"
			),
			OneTest(
					"max on an dict",
					"{'name': 'curly', 'age': 60}",
					[stooges],
					"_.max(stooges, lambda stooge: stooge['age'])"
			),
		]
	),
	(
		"min",
		[
			OneTest(
					"min on a list",
					"1",
					[],
					"_.min([1,2,3,4])"
			),
			OneTest(
					"min on a list with predicate",
					"4",
					[],
					"_.min([1,2,3,4], lambda x: -x)"
			),
			OneTest(
					"min on an empty list",
					"-inf",
					[],
					"_.min([])"
			),
			OneTest(
					"min on an dict",
					"{'name': 'moe', 'age': 40}",
					[stooges],
					"_.min(stooges, lambda stooge: stooge['age'])"
			),
		]
	),
	(
		"sortBy",
		[
			OneTest(
					"sort by on a list",
					"[5, 4, 6, 3, 1, 2]",
					[],
					"_.sortBy([1, 2, 3, 4, 5, 6], lambda num: math.sin(num))"
			),
			OneTest(
					"sort by on a dictionary with a predicate name",
					"[{'age': 60, 'name': 'curly'}, {'age': 60, 'name': 'joe'}, {'age': 50, 'name': 'larry'}, {'age': 40, 'name': 'moe'}]",
					[stooges],
					"_.sortBy(stooges, 'name')"
			),
		]
	),
	(
		"groupBy",
		[
			OneTest(
					"groupBy on a dict with a function",
					"{1.0: [1.3], 2.0: [2.1, 2.4]}",
					[stooges],
					"_.groupBy([1.3, 2.1, 2.4], lambda num: math.floor(num))"
			),
			OneTest(
					"groupBy on a dict with a key",
					"{40: [{'age': 40, 'name': 'moe'}], 50: [{'age': 50, 'name': 'larry'}], 60: [{'age': 60, 'name': 'curly'}, {'age': 60, 'name': 'joe'}]}",
					[stooges],
					"_.groupBy(stooges, 'age')"
			)
		]
	),
	(
		"indexBy",
		[
			OneTest(
					"indexBy on a dict with a key",
					"{40: {'name': 'moe', 'age': 40}, 50: {'name': 'larry', 'age': 50}, 60: {'name': 'curly', 'age': 60}}",
					[stooges0],
					"_.indexBy(stooges0, 'age')"
			)
		]
	),
	(
		"countBy",
		[
			OneTest(
					"countBy on a dict with a key",
					"{'even': 2, 'odd': 3}",
					[],
					"_.countBy([1, 2, 3, 4, 5], lambda num: 'even' if num % 2 == 0 else 'odd')"
			)
		]
	),
	(
		"shuffle",
		[
			OneTest(
					"shuffle",
					"(random order of [1,2,3,4,5])",
					[],
					"_.shuffle([1, 2, 3, 4, 5, 6])"
			)
		]
	),
	(
		"sample",
		[
			OneTest(
					"single sample",
					"(random sample of [1,2,3,4,5])",
					[],
					"_.sample([1, 2, 3, 4, 5, 6])"
			),
			OneTest(
					"sample of three",
					"(random sample of length 3 [1,2,3,4,5])",
					[],
					"_.sample([1, 2, 3, 4, 5, 6], 3)"
			)
		]
	),
	(
		"partition",
		[
			OneTest(
					"partition of array",
					"[[1, 3, 5], [0, 2, 4]]",
					[],
					"_.partition([0, 1, 2, 3, 4, 5], lambda num: num % 2 != 0)"
			),
			OneTest(
					"partition of tuple",
					"[[1, 3, 5], [0, 2, 4]]",
					[],
					"_.partition((0, 1, 2, 3, 4, 5), lambda num: num % 2 != 0)"
			),
		]
	),
]
AllTests = OrderedDict(_tests)


def run_tests(argv):
	def display_one_test_group(key) :
		print("\n=== Run test group '%s' ===" % key)
		# If this were not a test, this should use _.each :-)
		for test in AllTests[key] :
			test.execute_and_display()
		print("=== End of test group '%s' ===" % key)

	if len(argv) > 1:
		if argv[1] == 'all':
			# If this were not a test, this should use _.each :-)
			for key in AllTests:
				display_one_test_group(key)
		else:
			display_one_test_group(sys.argv[1])
	else:
		key = list(AllTests.keys())[-1] if PY3 else AllTests.keys()[-1]
		display_one_test_group(key)

if __name__ == '__main__':
	run_tests(sys.argv)
