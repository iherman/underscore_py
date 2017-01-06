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

	# (
	# 	"groupBy",
	# 	[
	# 		OneTest(
	# 				"groupBy on a dict with a key",
	# 				"{40: [{'age': 40, 'name': 'moe'}], 50: [{'age': 50, 'name': 'larry'}], 60: [{'age': 60, 'name': 'curly'}, {'age': 60, 'name': 'joe'}]}",
	# 				[stooges],
	# 				"_.groupBy(stooges, 'age')"
	# 		)
	# 	]
	# ),
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
