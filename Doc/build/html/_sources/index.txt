.. Underscore for Python documentation master file, created by
   sphinx-quickstart on Fri May  6 16:46:54 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Underscore for Python
=====================

This is a Python adaptation of the `Underscore.js <http://underscorejs.org/>`_  JavaScript library. Most of the method definitions have been taken over, following essentially the same definition, order or arguments, etc. Some changes to the Python style and environment was nevertheless necessary, and some of the original functions, closely related to JavaScript and Web Application development (e.g., function related to DOM nodes or HTML escaping) have been skipped.

The typical approach for using the library is::

    from underscore import underscore as _

meaning that the usage syntax becomes::

    _.map([1, 2, 3], lambda num, *args: num * 3)

Chaining
--------

Underscore methods usually return a suitable value to be included in another method’s input. Ie, it is possible to combine two methods as follows::

    _.map(_.filter([1,2,3,200],lambda num,*args: num % 2 == 0),lambda x,*args: x*x)

I.e., the output of the ``filter`` method is used as an argument in ``map``. This may become fairly unreadable, though. An alternative is to use *chaining*::

    _.chain([1,2,3,200]).filter(lambda num,*args: num % 2 == 0).map(lambda x,*args: x*x).value()

The ``_.chain`` method returns a wrapper object around the argument. Calling underscore methods, without the first argument, on this object means invoking the full-blown method with the wrapped object value as a first argument. Each call returns the wrapper with the newly computer value, until the ``value`` method is called. In usage terms, this means that each underscore method is invoked with the value generated in the previous element of the chain as the first argument of the method.

In fact, the call on ``_.chain`` is superfluous. Creating an underscore *instance* is sufficient; ``_.chain`` is just a functional equivalent. I.e., the following is equivalent to the previous example::

    _([1,2,3,200]).filter(lambda num,*args: num % 2 == 0).map(lambda x,*args: x*x).value()

Method definitions
------------------

Most of the methods have an example of usage to make the description clearer. Conceptually, the following Python code precedes all examples::

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

Detailed description of the methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: underscore
   :members:
   :undoc-members:
