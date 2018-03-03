# do.py
A do-notation decoration for Python.


## Sample Usage
Imagine you're writing a function that does three steps:
- Call `step_one()`, which may return a number or `None`.
- If the call above didn't return a `None`, call `step_two()`, which depends on the returned number. Again, `step_two()` may return a number or `None`.
- Finally, if the call above didn't return a `None`, return the sum of 100 with the returned number.

A typical implementation of this function

```py
def step_one():
    # Might return None in some cases
    # Returning 1 as an example
    return 1

def step_one(n):
    # Might return None in some cases
    # Returning n + 1 as an example
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

Well, the usual approach is to return `Maybe`s instead of direct values. So we rewrite `step_one` and `step_one` as follows:

```py
def step_one():
    return Just(1)

def step_two(n):
    return Just(n + 1)
```

Now we can write the code without all the `None`-checks like this:

```py
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
@do(Maybe)
def do_without_none_checks(x):
    result_one = yield step_one()
    result_two = yield step_two()
    raise Return(result_two)

final_result = do_without_none_checks(6)
```

Of course, if you really want a pure and consistent experience, you may want to rewrite `step_one` and `step_one` as: 

```py
@do(Maybe)
def step_one():
    raise Return(1)

@do(Maybe)
def step_two():
    raise Return(2)
```

## What's `raise Return`?
Unlike Python 3, in Python 2, a generator (that is, any function that uses the keyword `yield` in its body) cannot have a `return` statement. This is a practice borrowed from [Tornado](https://github.com/tornadoweb/tornado). `raise Return` is a work around this limitation.

## Roadmap
- [ ] Write tests
- [ ] Publish on PyPI
- [ ] Make available for both Python 2 and 3
