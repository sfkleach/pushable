.. pushable documentation master file, created by
   sphinx-quickstart on Mon Jan 23 08:56:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pushable, Peekable Iterators
############################

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. image:: https://dl.circleci.com/status-badge/img/gh/sfkleach/pushable/tree/main.svg?style=svg
        :target: https://dl.circleci.com/status-badge/redirect/gh/sfkleach/pushable/tree/main

.. image:: https://readthedocs.org/projects/pushable/badge/?version=latest
    :target: https://pushable.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This is a Python package that provides a wrapper class Pushable that turns
ordinary iterators into "peekable & pushable" iterators. Pushable iterators act 
like dynamically expanding queues, allowing you to peek ahead or push items back 
onto a queue that is only expanded as far as necessary. 

Click `here <pushable.html>`_ for the full API.


Basic Usage
===========

We can turn any iterable/iterator into a pushable iterator using the constructor.

.. code-block:: python

   from pushable import Pushable
   count_up = Pushable( range( 0, 5 ) )


We can use it like an ordinary iterator:

.. code-block:: python

   print( next( count_up ) )
   # Prints 0

Or we can look-ahead to see what is coming:

.. code-block:: python

   whats_up_next = count_up.peek()
   print( whats_up_next )
   # Print 1
   print( next( count_up ) )
   # Also prints 1 because peek does not remove the item from the internal queue.

We can even push back items onto it:

.. code-block:: python

   count_up.push("cat")
   count_up.push("dog")
   print( list( count_up ) )
   # Prints 'dog', 'cat', 2, 3, 4

Examples
========

From an iterator such as a file-object, which will iterate over the lines in a file, create a peekable/pushable iterator. This can be useful for example when we want to know if the iterator still has contents or want a sneak peek at what is coming.

.. code-block:: python

   from pushable import Pushable

   def read_upto_two_blank_lines( filename ):
      with open( filename ) as file:
         plines = Pushable( file )
         # Pushable iterators can be used as booleans in the natural way.
         while plines:
               line = next( plines )
               # peekOr makes it safe to look ahead.
               if line == '\n' and plines.peekOr() == '\n':
                  # Two blank lines encountered.
                  break
               else:
                  yield line        


It is also useful to perform "macro-like" transformation.

.. code-block:: python

   from pushable import Pushable

   def translate( text, translations ):
      ptokens = Pushable( text.split() )
      while ptokens:
         token = next(ptokens)
         if token in translations:
               ptokens.multiPush( *translations[token].split() )
         else:
               yield token

   print( ' '.join( translate( 'My name is MYNAME', {'MYNAME':'Fred Bloggs'} ) ) ) 
   # Prints: My name is Fred Bloggs

More Complex Uses
=================

In addition to peeking and popping items, which risks raising a
`StopIteration` exception if there's nothing left on the internal queue, we
can utilise `peekOr` and `popOr` to deliver a default value instead. The 
default value is passed as an optional parameter and falls back to None.

We can also peek and pop multiple values using `multiPeekOr` and `multiPopOr`, 
which return generators. These support skipping over values so that you can
get the 2nd and 3rd value without getting the first e.g.

.. code-block:: python

   (second, third) = Pushable("pqr").multiPop(skip=1, count=2)
   print( second, third )
   # Prints: q r

Lastly, we can push multiple items with `multiPush`:

.. code-block:: python

   count_up.multiPush("cat", "dog", "rabbit")
   count_up.push("dog")
   print( list( count_up ) )
   # Prints: ['cat', 'dog', 'rabbit']




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
