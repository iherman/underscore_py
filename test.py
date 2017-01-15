#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import sys
# Tricks to handle Python3
PY3 = sys.version_info.major > 2

from underscore import underscore as _
import math
from collections import OrderedDict

def isPrime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
         return False;
    if n % 2 == 0:
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True


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
stooges  = [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}, {'name':'joe', 'age':60}]
stooges0 = [{'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}]
stooges2 = [{'name': 'moe', 'age': 40}, {'name': 'curly', 'age': 60}]

class OneTest:
	def __init__(self, testName, toExpect, toDisplay, toEval, supressOutput = False):
		"""
		testName: arbitrary text to label the output of a specific toExpect
		toExpect: a string that shows what the correct output of the test should be
		toDisplay: (possibly empty) array of variables in this module that should be displayed as part of the test.
		toEval: the test that should be executed. There are two flavours:
			- toEval is a string; this is displayed and then run through Python's eval. This means it is an expression, not an assignment
			- toEval is list of tuples. Each tuple is a string and a boolean; the string is to be executed via Python's exec (if the second element of the tuple is True) or through eval (if the second element of the tuple is False). This means that the string may refer to an assignment (if using exec). The list is typically used when the test requires several consecutive statements, eg, for function functions. Such an array typically ends with a ('command', False) tuple.
		supressOutput: if the output of the (last) command should be displayed or not. For some tests, the result is a side-effect of some internal functions, in which case the output of the last command may not be relevant...
		"""
		self.glob = glob = globals()
		self.name      = testName
		pr = lambda name, variable: " >>> %s = %s" % (name, variable)
		self.toDisplay = [pr(k, x) for x in toDisplay for k in glob if glob[k] == x]
		self.toExpect  = toExpect
		self.toEval    = toEval
		self.supressOutput = supressOutput

	def execute_and_display(self):
		print("\n== Test: '%s' ==" % self.name)
		if self.toExpect and len(self.toExpect) != 0:
			print("= Expected:\n" + self.toExpect)
		print("= Test run:")
		if self.toDisplay is not None and len(self.toDisplay) != 0:
			_.forEach(self.toDisplay, lambda x, *args: print(x))
		if isinstance(self.toEval,str):
			print(" >>> " + self.toEval)
			if self.supressOutput:
				eval(self.toEval)
			else:
				print(str(eval(self.toEval)))
		else:
			# In some cases an array of calls must be executed, with first few strings setting variables...
			for i in range(0, len(self.toEval)):
				command, toExec = self.toEval[i]
				print(" >>> " + command)
				if i < len(self.toEval) - 1:
					if toExec:
						exec(command, self.glob)
					else:
						if self.supressOutput:
							eval(command)
						else:
							print(str(eval(command)))
				else:
					# Last one has to display the results, unless explicitly supressed
					if self.supressOutput:
						if toExec:
							exec(command, self.glob)
						else:
							eval(command)
					else:
						if toExec:
							exec(command, self.glob)
						else:
							print(str(eval(command)))

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
	(
		"first",
		[
			OneTest(
					"first element",
					"5",
					[],
					"_.first([5, 4, 3, 2, 1])"
			),
			OneTest(
					"first three elements",
					"[5, 4, 3]",
					[],
					"_.first([5, 4, 3, 2, 1],3)"
			),
		]
	),
	(
		"initial",
		[
			OneTest(
					"initial part of array",
					"[5, 4, 3, 2]",
					[],
					"_.initial([5, 4, 3, 2, 1])"
			),
			OneTest(
					"initial with three elements removed",
					"[5, 4]",
					[],
					"_.initial([5, 4, 3, 2, 1],3)"
			),
		]
	),
	(
		"last",
		[
			OneTest(
					"last element of array",
					"1",
					[],
					"_.last([5, 4, 3, 2, 1])"
			),
			OneTest(
					"last three elements of array",
					"[3, 2, 1]",
					[],
					"_.last([5, 4, 3, 2, 1],3)"
			),
		]
	),
	(
		"rest",
		[
			OneTest(
					"rest of array",
					"[4, 3, 2, 1]",
					[],
					"_.rest([5, 4, 3, 2, 1])"
			),
			OneTest(
					"rest of array starting by index '3'",
					"[2, 1]",
					[],
					"_.rest([5, 4, 3, 2, 1],3)"
			),
		]
	),
	(
		"compact",
		[
			OneTest(
					"remove 'falsy' values",
					"[1, 2, 3, 4, 5]",
					[],
					"_.compact([0, 1, False, 2, '', 3, None, 4, float('nan'), 5])"
			),
		]
	),
	(
		"flatten",
		[
			OneTest(
					"'deep' flatten",
					"[1, 2, 3, 4]",
					[],
					"_.flatten([1, [2], [3, [[4]]]])"
			),
			OneTest(
					"'shallow' flatten",
					"[1, 2, 3, 4]",
					[],
					"_.flatten([1, [2], [3, [[4]]]], shallow = True)"
			),
		]
	),
	(
		"without",
		[
			OneTest(
					"array with two elements removed",
					"[1, 2, 3, 4]",
					[],
					"_.without([1, 2, 1, 0, 3, 1, 4], 0, 1)"
			),
		]
	),
	(
		"union",
		[
			OneTest(
					"Union of arrays",
					"[1, 2, 3, 101, 10]",
					[],
					"_.union([1, 2, 3], [101, 2, 1, 10], [2, 1])"
			),
		]
	),
	(
		"intersection",
		[
			OneTest(
					"Intersection of arrays",
					"[1, 2]",
					[],
					"_.intersection([1, 2, 3], [101, 2, 1, 10], [2, 1])"
			),
			OneTest(
					"Intersection of arrays 2nd.",
					"[2]",
					[],
					"_.intersection([1, 2, 3], [101, 2, 1, 10], [2])"
			),
		]
	),
	(
		"difference",
		[
			OneTest(
					"Difference of arrays",
					"[1, 3, 4]",
					[],
					"_.difference([1, 2, 3, 4, 5], [5, 2, 10])"
			),
			OneTest(
					"Difference of arrays",
					"[3, 4]",
					[],
					"_.difference([1, 2, 3, 4, 5], [5, 2, 10], [1])"
			),
		]
	),
	(
		"uniq",
		[
			OneTest(
					"Duplicate free version of array",
					"[1, 2, 3, 4]",
					[],
					"_.uniq([1, 2, 1, 3, 1, 4, 2])"
			),
			OneTest(
					"Duplicate free version of sorted array",
					"[1, 2, 3, 4, 5]",
					[],
					"_.uniq([1, 1, 1, 2, 3, 4, 4, 5], isSorted = True)"
			),
			OneTest(
					"Uniq version of transformed array",
					"[1.5, 2.0, 3.0, 4.0]",
					[],
					"_.uniq([1.5, 1.7, 2.0, 2.5, 2.5, 3.0, 4.0], iteratee = math.floor)"
			),
		]
	),
	(
		"zip",
		[
			OneTest(
					"Zip arrays",
					"[['moe', 30, True], ['larry', 40, False], ['curly', 50, False]]",
					[],
					"_.zip(['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False])"
			),
			OneTest(
					"Zip tuples",
					"[('moe', 30, True), ('larry', 40, False), ('curly', 50, False)]",
					[],
					"_.zip(('moe', 'larry', 'curly'), (30, 40, 50), (True, False, False))"
			),
		]
	),
	(
		"object",
		[
			OneTest(
					"Object created with pairs in arrays",
					"{'larry': 40, 'curly': 50, 'moe': 30}",
					[],
					"_.object([['moe', 30], ['larry', 40], ['curly', 50]])"
			),
			OneTest(
					"Object created with pairs in arrays",
					"{'larry': 40, 'curly': 50, 'moe': 30}",
					[],
					"_.object([('moe', 30), ('larry', 40), ('curly', 50)])"
			),
			OneTest(
					"Object created with separate arrays",
					"{'larry': 40, 'curly': 50, 'moe': 30}",
					[],
					"_.object(['moe', 'larry', 'curly'], [30, 40, 50])"
			),
		]
	),
	(
		"indexOf",
		[
			OneTest(
					"Simple indexOf",
					"1",
					[],
					"_.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2)"
			),
			OneTest(
					"Simple indexOf using a start and end indeces",
					"4",
					[],
					"_.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2, 3, 6)"
			),
			OneTest(
					"Simple indexOf with negative result",
					"-1",
					[],
					"_.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 10)"
			),
		]
	),
	(
		"lastIndexOf",
		[
			OneTest(
					"Simple lastIndexOf",
					"7",
					[],
					"_.lastIndexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2)"
			),
			OneTest(
					"lastIndexOf using a start and end indeces",
					"4",
					[],
					"_.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 2, 3, 6)"
			),
			OneTest(
					"lastIndexOf with negative result",
					"-1",
					[],
					"_.indexOf([1, 2, 3, 1, 2, 3, 4, 2, 5], 10)"
			),
		]
	),
	(
		"sortedIndex",
		[
			OneTest(
					"Simple sorted index",
					"3",
					[],
					"_.sortedIndex([10, 20, 30, 40, 50], 35)"
			),
			OneTest(
					"sorted index pointing to the last place in the array",
					"5",
					[],
					"_.sortedIndex([10, 20, 30, 40, 50], 55)"
			),
			OneTest(
					"sorted index with a simple iteratee",
					"1",
					[stooges2],
					"_.sortedIndex(stooges2, {'name': 'larry', 'age': 50}, 'age')"
			),
		]
	),
	(
		"findIndex",
		[
			OneTest(
					"findIndex with negative results",
					"-1",
					[],
					"_.findIndex([4, 6, 8, 12, 14, 16], isPrime)"
			),
			OneTest(
					"findIndex with positive results",
					"2",
					[],
					"_.findIndex([4, 6, 3, 12, 14, 16], isPrime)"
			),
			OneTest(
					"findIndex with negative results on a subarray",
					"-1",
					[],
					"_.findIndex([4, 6, 3, 12, 14, 16], isPrime, startIndex=3)"
			),
			OneTest(
					"findIndex with positive results on a subarray",
					"2",
					[],
					"_.findIndex([4, 6, 3, 12, 14, 16], isPrime, startIndex=1, endIndex=5)"
			),
		]
	),
	(
		"findLastIndex",
		[
			OneTest(
					"findIndex with negative results",
					"-1",
					[],
					"_.findLastIndex([4, 6, 8, 12, 14, 16], isPrime)"
			),
			OneTest(
					"findLastIndex with positive results",
					"4",
					[],
					"_.findLastIndex([2, 6, 7, 12, 13, 16], isPrime)"
			),
			OneTest(
					"findLastIndex with positive results on a subarray",
					"4",
					[],
					"_.findLastIndex([2, 6, 7, 12, 13, 16], isPrime, startIndex = 1)"
			),
			OneTest(
					"findLastIndex with positive results on a subarray",
					"2",
					[],
					"_.findLastIndex([2, 6, 7, 12, 13, 16], isPrime, startIndex = 1, endIndex = 3)"
			),
		]
	),
	(
		"range",
		[
			OneTest(
					"range, starting with 0",
					"[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]",
					[],
					"_.range(10)"
			),
			OneTest(
					"range with an explicit starting value",
					"[3, 4, 5, 6, 7, 8, 9]",
					[],
					"_.range(3, 10)"
			),
			OneTest(
					"range with explicit step",
					"[3, 5, 7, 9]",
					[],
					"_.range(3, 10, 2)"
			),
		]
	),
	(
		"partial",
		[
			OneTest(
					"partial 1.",
					"15",
					[],
					[
						("sub = lambda a,b:b-a", True),
						("sub5 = _.partial(sub,5)", True),
						("sub5(20)", False)
					]
			),
			OneTest(
					"partial 2.",
					"15",
					[],
					[
						("sub = lambda a,b:b-a", True),
						("subFrom20 = _.partial(sub,None,20)", True),
						("subFrom20(5)", False)
					]
			),
		]
	),
	(
		"before",
		[
			OneTest(
					"before 3",
					"created\ncreated\ncreated",
					[],
					[
						("createApplication = lambda : print('created')", True),
						("createOnly3 = _.before(3,createApplication)", True),
						("createOnly3()", False),
						("createOnly3()", False),
						("createOnly3()", False),
						("createOnly3()", False)
					],
					True
			),
		]
	),
	(
		"after",
		[
			OneTest(
					"after 2",
					"created",
					[],
					[
						("createApplication = lambda : print('created')", True),
						("delayInit = _.after(2,createApplication)", True),
						("delayInit()", False),
						("delayInit()", False),
						("delayInit()", False)
					],
					True
			),
		]
	),
	(
		"once",
		[
			OneTest(
					"create only once",
					"created\n ",
					[],
					[
						("createApplication = lambda : print('created')", True),
						("initialize = _.once(createApplication)", True),
						("initialize()", False),
						("initialize()", False),
					],
					True
			),
		]
	),
	(
		"wrap",
		[
			OneTest(
					"Wrap a function",
					"Do something with the arguments: (1, 2, 3)\nHello: 'tester'\nDo something after execution of wrapped",
					[],
					[
						("func = lambda x : print('Hello: \"' + x + '\"')", True),
						("def wrapper(f,*args,**keywords): print('Do something with the arguments: ' + str(args)); f('tester'); print('Do something after execution of wrapped')", True),
						("wrapped = _.wrap(func, wrapper)", True),
						("wrapped(1,2,3)", False),
					],
					True
			),
		]
	),
	(
		"negate",
		[
			OneTest(
					"Negate false",
					"True",
					[],
					[
						("test = lambda x, y: x and y", True),
						("_.negate(test,False,True)", False),
					]
			),
			OneTest(
					"Negate True",
					"False",
					[],
					[
						("test = lambda x, y: x and y", True),
						("_.negate(test,True,True)", False),
					]
			),
		]
	),
	(
		"compose",
		[
			OneTest(
					"composition of greeting",
					"hi: MOE!",
					[],
					[
						("greet    = lambda name: 'hi: ' + name", True),
						("exclaim  = lambda statement: statement.upper() + '!'", True),
						("welcome  = _.compose(greet, exclaim)", True),
						("welcome('moe')", False)
					]
			),
		]
	),
	(
		"keys",
		[
			OneTest(
					"Keys of a dict",
					"['three', 'two', 'one'] (in some order)",
					[],
					"_.keys({'one': 1, 'two': 2, 'three': 3})"
			),
		]
	),
	(
		"values",
		[
			OneTest(
					"Valuse of a dict",
					"[1,3,2] (in some order)",
					[],
					"_.values({'one': 1, 'two': 2, 'three': 3})"
			),
		]
	),
	(
		"mapObject",
		[
			OneTest(
					"Map object without an iterator (simply a clone)",
					"{'one': 1, 'three': 3, 'two': 2}",
					[],
					"_.mapObject({'one': 1, 'two': 2, 'three': 3})"
			),
			OneTest(
					"Map object with an iterator",
					"{'one': 1, 'three': 3, 'two': 2}",
					[],
					"_.mapObject({'one': 1, 'two': 2, 'three': 3}, lambda key, val, obj: 3*val)"
			),
		]
	),
	(
		"pairs",
		[
			OneTest(
					"pairs in the form of arrays",
					"{'one': 1, 'three': 3, 'two': 2}",
					[],
					"_.pairs({'one': 1, 'two': 2, 'three': 3})"
			),
			OneTest(
					"pairs in the form of a tuple",
					"{'one': 1, 'three': 3, 'two': 2}",
					[],
					"_.pairs({'one': 1, 'two': 2, 'three': 3}, tupl = True)"
			),
		]
	),
	(
		"invert",
		[
			OneTest(
					"invert the object",
					"{'Louis': 'Larry', 'Moses': 'Moe', 'Jerome': 'Curly'}",
					[],
					'_.invert({"Moe": "Moses", "Larry": "Louis", "Curly": "Jerome"})'
			),
		]
	),
	(
		"findKey",
		[
			OneTest(
					"find an existing key",
					"Curly",
					[],
					'_.findKey({"Moe": "Moses", "Larry": "Louis", "Curly": "Jerome"}, lambda val: val == "Jerome")'
			),
			OneTest(
					"look for a non-existing key",
					"None",
					[],
					'_.findKey({"Moe": "Moses", "Larry": "Louis", "Curly": "Jerome"}, lambda val: val == "Philipp")'
			),
		]
	),
	(
		"extend",
		[
			OneTest(
					"find an existing key",
					"{'gender': 'male', 'age': 60, 'name': 'moe'}",
					[],
					"_.extend({'name': 'moe', 'age': '40'}, {'age': 50}, {'age': 60, 'gender': 'male'})"
			),
		]
	),
	(
		"extendOwn",
		[
			OneTest(
					"find an existing key",
					"{'age': 60, 'name': 'moe'}",
					[],
					"_.extendOwn({'name': 'moe', 'age': '40'}, {'age': 50}, {'age': 60, 'gender': 'male'})"
			),
		]
	),
	(
		"pick",
		[
			OneTest(
					"pick via a series of keys",
					"{'age': 50, 'name': 'moe'}",
					[],
					"_.pick({'name': 'moe', 'age': 50, 'userid': 'moe1'}, 'name', 'age')"
			),
			OneTest(
					"find an existing key",
					"{'age': 50, 'name': 'moe'}",
					[],
					[
						("a = ['name', 'age']", True),
						("_.pick({'name': 'moe', 'age': 50, 'userid': 'moe1'}, *a)", False)
					]
			),
			OneTest(
					"pick via a series of keys via a predicate",
					"{'age': 50}",
					[],
					"_.pick({'name': 'moe', 'age': 50, 'userid': 'moe1'}, lambda val, *args: _.isNumber(val))"
			),
		]
	),
	(
		"omit",
		[
			OneTest(
					"omit via a series of keys",
					"{userid': 'moe1'}",
					[],
					"_.omit({'name': 'moe', 'age': 50, 'userid': 'moe1'}, 'name', 'age')"
			),
			OneTest(
					"omit an existing key",
					"{userid': 'moe1'}",
					[],
					[
						("a = ['name', 'age']", True),
						("_.omit({'name': 'moe', 'age': 50, 'userid': 'moe1'}, *a)", False)
					]
			),
			OneTest(
					"omit via a series of keys via a predicate",
					"{'name': 'moe', userid': 'moe1'}",
					[],
					"_.omit({'name': 'moe', 'age': 50, 'userid': 'moe1'}, lambda val, *args: _.isNumber(val))"
			),
		]
	),
	(
		"default",
		[
			OneTest(
					"omit an existing key",
					"{'flavor': 'chocolate', 'sprinkles': 'lots'}",
					[],
					[
						("iceCream = {'flavor': 'chocolate'}", True),
						("_.defaults(iceCream, {'flavor': 'vanilla', 'sprinkles': 'lots'})", False)
					]
			),
			OneTest(
					"omit an existing key",
					"{'flavor': 'chocolate', 'sprinkles': 'lots', 'toGo' : True}",
					[],
					[
						("iceCream = {'flavor': 'chocolate'}", True),
						("myDefaults = [{'flavor':'vanilla', 'sprinkles':'lots'}, {'toGo': True}]", True),
						("_.defaults(iceCream, *myDefaults)", False)
					]
			),
		]
	),
	(
		"default",
		[
			OneTest(
					"shallow clone",
					"{'flavor': 'chocolate', 'sprinkles': 'lots', 'toGo' : True}",
					[],
					"_.clone({'flavor': 'chocolate', 'sprinkles': 'lots', 'toGo' : True})"
			),
			OneTest(
					"deep clone",
					"{'flavor': 'chocolate', 'sprinkles': { 'nut': True, 'sultana': False}, 'toGo' : True}",
					[],
					"_.clone({'flavor': 'chocolate', 'sprinkles': { 'nut': True, 'sultana': False}, 'toGo' : True}, deep = True)"
			),
		]
	),
	(
		"property",
		[
			OneTest(
					"function to get 'name'",
					"joe\nmoe",
					[stooges, stooges0],
					[
						("getName = _.property('name')", True),
						("getName(stooges[3])", False),
						("getName(stooges0[0])", False)
					]
			),
		]
	),
	(
		"propertyOf",
		[
			OneTest(
					"function to get values of a dict",
					"joe\n60",
					[stooges],
					[
						("getValue = _.propertyOf(stooges[3])", True),
						("getValue('name')", False),
						("getValue('age')", False)
					]
			),
		]
	),
	(
		"propertyOf",
		[
			OneTest(
					"function to get values of a dict",
					"joe\n60",
					[stooges],
					[
						("getValue = _.propertyOf(stooges[3])", True),
						("getValue('name')", False),
						("getValue('age')", False)
					]
			),
		]
	),
	(
		"matcher",
		[
			OneTest(
					"function to probe key/value pair",
					"False\nTrue",
					[stooges],
					[
						("checkAge = _.matcher({'age': 60})", True),
						("checkAge(stooges[0])", False),
						("checkAge(stooges[2])", False),
					]
			),
		]
	),
	(
		"isMatch",
		[
			OneTest(
					"matching objects",
					"True\nFalse",
					[stooges],
					[
						("probe = {'age':40}", True),
						("_.isMatch(stooges[0], probe)", False),
						("_.isMatch(stooges[3], probe)", False),
					]
			),
		]
	),
	(
		"isFunction",
		[
			OneTest(
					"test 1.",
					"True",
					[],
					"_.isFunction(isPrime)"
			),
			OneTest(
					"test 2.",
					"True",
					[],
					"_.isFunction(lambda x: x+1)"
			),
			OneTest(
					"test 3.",
					"False",
					[],
					"_.isFunction(1)"
			),
		]
	),
	(
		"times",
		[
			OneTest(
					"test 1.",
					"[0, 1, 2]",
					[],
					"_.times(3, _.identity)"
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
