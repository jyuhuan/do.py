[![Build Status](https://travis-ci.org/jyuhuan/do.py.svg?branch=master)](https://travis-ci.org/jyuhuan/do.py)
[![Code Coverage](https://codecov.io/github/jyuhuan/do.py/coverage.svg?branch=master)](https://codecov.io/gh/jyuhuan/do.py?branch=master)

# do.py
A do-notation decorator for Python.


## Sample Usage

Imagine you're writing a function that does three steps:

- Call `step_one()`, which may return a number or `None`.
- If the call above didn't return a `None`, call `step_two(n)`, which depends on the previously returned number. Again, `step_two()` may return a number or `None`.
- Finally, if the call above didn't return a `None`, return the sum of 100 with the returned number.

A typical implementation of this function

```py
def step_one():
    # Might return None in some cases.
    # Returning 1 as an example.
    return 1

def step_two(n):
    # Might return None in some cases.
    # Returning n + 1 as an example.
    return n + 1

def lots_of_none_checks():
    result_one = step_one()
    if result_one is not None:
        result_two = step_two(result_one)
        if result_two is not None:
            return 100 + result_two
   return None
```

How do we improve this piece of complicated, error-prone code?

Well, the usual approach is to return `Maybe`s instead of direct values. So we rewrite `step_one` and `step_two` as follows:

```py
def step_one():
    return Just(1)

def step_two(n):
    return Just(n + 1)
```

Now we can write the code without all the `None`-checks like this:

```py
def lots_of_flat_maps():
    step_one().flat_map(
        lambda result_one: step_two(result_one).flat_map(
            lambda result_two: 100 + result_two
        )
    )
```

This kind of code is usually referred to as "callback hell" by JavaScript users.

How do we avoid the callback hell, then?

Introducing the decorator `@do`!

Here's how we could write the same code more elegantly with `@do`:

```py
@do(MaybeEv)
def do_elegantly():
    result_one = yield step_one()
    result_two = yield step_two(result_one)
    raise Return(result_two)

# Note that final_result is still a Maybe.
final_result = do_elegantly()
```

where `MaybeEv` is the evidence that witnesses the monad properties of the type `Maybe`, namely the `id` and `flat_map` functions defined for `Maybe`s.

Of course, if you really want a *pure* experience, you may want to rewrite `step_one` and `step_two` as: 

```py
@do(MaybeEv)
def step_one():
    raise Return(1)

@do(MaybeEv)
def step_two(n):
    raise Return(n + 1)
```

## Why `raise Return` instead of `return`?
Unlike Python 3, in Python 2, a generator (that is, any function that uses the keyword `yield` in its body) cannot have a `return` statement. This is a practice borrowed from [Tornado](https://github.com/tornadoweb/tornado). `raise Return` is a work around this limitation.

## Related Work
The `@do` decorator of do.py works the same way as the `Do.Multi` function in [*Fantasy Do*](fantasy-do-repo), a JavaScript library which implements the do-notation using JavaScript's generators. However, the decorator mechanism of Python gives `@do` a neater syntax.

The approach proposed by the blog post [*Monads in Python (with nice syntax!)*] (python-do-blog) is the closest to do.py in terms of syntax. However, that approach only supports a subset of monads. Specifically, any monad in which the `flat_map(m, f)` method invokes the `f` argument more than one time is not supported (e.g., list monads). In do.py, this is not a problem.

## Roadmap
- [ ] Publish on PyPI
- [ ] Make available for both Python 2 and 3


[tornado-repo]: https://github.com/tornadoweb/tornado

[python-do-blog]: http://www.valuedlessons.com/2008/01/monads-in-python-with-nice-syntax.html

[fantasy-do-repo]: https://github.com/russellmcc/fantasydo
