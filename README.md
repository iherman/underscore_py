# underscore_py
A blatant rewrite of (most of ) the [Javascript underscore module](http://underscorejs.org/) to Python. I found the Javascript module very useful when using Javascript, no reason why not have the same facility in Python…

Documentation is included in the repo, and also [available online](https://cdn.rawgit.com/iherman/underscore_py/master/Doc/build/html/index.html).

## Changes

Version 2.
* Made the module usable from Python 3
* Severed the ties with Python 2.6 and lower (2.6 lacks dictionary comprehension, for example)
* Systematic checks for the type of the arguments, and ``TypeError`` exceptions are raised if there is a problem
* Created the ``test.py`` with a simple test harness, and have most of the methods represented with simple tests (except for very obvious methods that are, e.g., aliases of system functions)
* Added some more examples to some methods

Version 1.
* Initial version
