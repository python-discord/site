---
title: Mutability and Immutability in Python
description: "Mutable and immutable data types: What they are and how they work."
---

Consider this example:
```python
>>> s = "hello"
>>> s.upper()
'HELLO'
>>> s
'hello'
```
This might break your expectations.
After all, you've called the `upper()` method on `s`, so why didn't it change? That's because strings are _immutable_: you can't change them in-place, only create new ones.
In this example, `.upper()` just cannot change the string stored in `s`.

How do you make `s` store `'HELLO'` instead of `'hello'` then? That's possible.
Even though you can't change the original string, you can create a new one, which is like the old one, but with all letters in upper case.

In other words, `s.upper()` doesn't change an existing string.
It just returns a new one.
```python
>>> s = 'hello'
>>> s = s.upper()
>>> s
'HELLO'
```

Let's examine what's going on here.
At first, the variable `s` refers to some object, the string `'hello'`.

![s refers to the string "hello"](/static/images/content/mutability/s_refers_hello.png)

When you call `s.upper()`, a new string, which contains the characters `'HELLO'`, gets created.

![s.upper creates "HELLO"](/static/images/content/mutability/s_upper_creates_HELLO.png)

This happens even if you just call `s.upper()` without any assignment, on its own line:
```python
"hello".upper()
```
In this case, a new object will be created and discarded right away.

Then the assignment part comes in: the name `s` gets disconnected from `'hello'`, and gets connected to `'HELLO'`.

![s gets assigned to "HELLO"](/static/images/content/mutability/s_gets_assigned_to_HELLO.png)

Now we can say that `'HELLO'` is stored in the `s` variable.

Then, because no variables refer to the _object_ `'hello'`, it gets eaten by the garbage collector.

!["hello" Gets Eaten](/static/images/content/mutability/hello_gets_eaten.png)

It means that the memory reserved for that object will be freed. If that didn't happen, the 'garbage' would accumulate over time and fill up all the RAM.
