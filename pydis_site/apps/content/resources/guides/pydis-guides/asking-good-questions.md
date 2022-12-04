---
title: Asking Good Questions
description: A guide for how to ask good questions in our community.
icon: fab fa-discord
toc: 3
---

This document is intended to provide you with the information you need to get help as quickly and effectively as possible.
If you're stuck on a problem or you just don't understand something, you should always feel welcome to ask.

# Before You Ask

Before you ask your question, there are a few things you can do to find an answer on your own.
Experienced developers will do the following:

* Read the official documentation for whatever you're working with
* Use a debugger to inspect your code
* Examine the traceback when your code raises an exception
* Do some research online - for example, on Stack Overflow
* Read the source code for whatever you're working with

Essentially, doing your research is the first step towards a solution to any problem.
If your problem isn't extremely general, we're going to be doing exactly these steps ourselves when helping you, so doing the legwork beforehand saves everyone a lot of time.

If none of the above steps help you or you're not sure how to do some of the above steps, feel free to ask us for help.

# A Good Question

When you're ready to ask a question, there are a few things you should have to hand before forming a query.

* A code example that illustrates your problem
* If possible, make this a minimal example rather than an entire application
* Details on how you attempted to solve the problem on your own
* Full version information - for example, "Python 3.6.4 with `discord.py 1.0.0a`"
* The full traceback if your code raises an exception
* Do not curate the traceback as you may inadvertently exclude information crucial to solving your issue

Your question should be informative, but to the point.
More importantly, how you phrase your question and how you address those that may help you is crucial.
Courtesy never hurts, and please type using correctly-spelled and grammatical language as far as you possibly can.

When you're inspecting a problem, don't be quick to assume that you've found a bug, or that your approach is correct.
While it helps to detail what exactly you're trying to do, you should also be able to give us the bigger picture - describe the goal, not just the step.
Describe the problem's symptoms in chronological order - not your guesses as to their cause.

| Bad Questions | Good Questions |
| ------------- | -------------- |
| Where can I find information on discord.py? | I used Google to try to find more information about "discord.py 1.0.0a", but I couldn't really find anything useful. Does anyone know where I might find a guide to writing commands using this library? |
| Pillow puts my text at the bottom of the image instead of where I wanted it. Why is it broken? | Pillow appears to insert text at the bottom of the image if the given X coordinate is negative. I had a look at the documentation and searched Stack Overflow, but I couldn't find any information on using negative coordinates to position text. Has anyone attempted this? |
| I'm having some trouble writing a YouTube random URL generator - can anyone help? | My YouTube random URL generator appears to be returning false positives for tested URLs, stating that a URL points to a real video when that video doesn't actually exist. Obviously there's some issue with how this is checked, but I can't put my finger on it. Is there anything I can check? |
| I was given this assignment by my teacher, but I'm not sure how to approach it. Does anyone have any ideas? | I have a list of numbers - how do I calculate how many of them are even? Is there a way to remove all the odd numbers from my list? Are there quick ways to find the average of a list of numbers, or add them all together? |


# What Not To Ask
---

#### Q: Can I ask a question?

Yes. Always yes. Just ask.

#### Q: Is anyone here good at Flask / Pygame / PyCharm?

There are two problems with this question:

1. This kind of question does not manage to pique anyone's interest, so you're less likely to get an answer overall.
    On the other hand, a question like `"Is it possible to get PyCharm to automatically compile SCSS into CSS files"` is much more likely to be interesting to someone.
    Sometimes, the best answers come from someone who does not already know the answer, but who finds the question interesting enough to go search for the answer on your behalf.
2. When you qualify your question by first asking if someone is good at something, you are filtering out potential answerers.
    [Not only are people bad at judging their own skill at something](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect), but the truth is that even someone who has zero experience with the framework you're having trouble with might still be of excellent help to you.

So instead of asking if someone is good at something, simply ask your question right away.

#### Q: Can I use `str()` on a `discord.py` Channel object?

Try it yourself and see. Experimentation is a great way to learn, and you'll save a lot of time by just trying things out. Don't be afraid of your computer!

#### Q: My code doesn't work

This isn't a question, and it provides absolutely no context or information.
Depending on the mood of the people that are around, you may even find yourself ignored.
Don't be offended by this - just try again with a better question.

#### Q: Can anyone help me break into someone's Facebook account / write a virus / download videos from YouTube?

We will absolutely not help you with hacking, pirating, or any other illegal activity.
A question like this is likely to be followed up with a ban if the person asking it doesn't back down quickly.

#### Q: Can I send you a private message?

Sure, but keep in mind that our staff members will not provide help via DMs.
We prefer that questions are answered in a public channel so lurkers can learn from them.

#### Q: Can you help me over Teamviewer?

No, sorry.


# Examining Tracebacks

Usually, the first sign of trouble is that when you run your code, it raises an exception.
For beginning programmers, the traceback that's generated for the exception may feel overwhelming and discouraging at first.
However, in time, most developers start to appreciate the extensive information contained in the traceback as it helps them track down the error in their code.
So, don't panic and take a moment to carefully review the information provided to you.

### Reading the Traceback

```py
Traceback (most recent call last):
  File "my_python_file.py", line 6, in <module>
    spam = division(a=10, b=0)
  File "my_python_file.py", line 2, in division
    answer = a / b
ZeroDivisionError: division by zero
```

In general, the best strategy is to read the traceback from bottom to top.
As you can see in the example above, the last line of the traceback contains the actual exception that was raised by your code.
In this case, `ZeroDivisionError: division by zero`, clearly indicates the problem: We're trying to divide by zero somewhere in our code and that obviously can't be right.
However, while we now know which exception was raised, we still need to trace the exception back to the error in our code.

To do so, we turn to the lines above the exception.
Reading from bottom to top again, we first encounter the line where the exception was raised: `answer = a / b`.
Directly above it, we can see that this line of code was `line 2` of the file `my_python_file.py` and that it's in the scope of the function `division`.
At this point, it's a good idea to inspect the code referenced here to see if we can spot an obvious mistake:

```py
# Python Code
1| def division(a, b):
2|    answer = a / b
3|    return answer
```

Unfortunately, there's no obvious mistake in the code at this point, although one thing we do see here is that this function divides `a` by `b` and that the exception will only occur if `b` is somehow assigned the numeric value `0`.

Keeping that observation in the back of our minds, we continue reading the traceback from bottom to top. The next thing we encounter is `spam = division(a=10, b=0)` from `line 6` of the file `my_python_file.py`.
In this case, `<module>` tells us that the code is in the global scope of that file.
While it's already clear from the traceback what's going wrong here, we're passing `b=0` to the function `division`, inspecting the code shows us the same:

```python
5| spam = division(a=10, b=0)
6| print(spam)
```

We have now traced back the exception to a line of code calling the division function with a divisor of `0`.
Obviously, this is a simplified example, but the exact same steps apply to more complex situations as well.

### The Error is Sometimes in the Line Before the Line in the Traceback

Sometimes, the actual error is in the line just before the one referenced in the traceback.
This usually happens when we've inadvertently omitted a character meant to close an expression, like a brace, bracket, or parenthesis.
For instance, the following snippet of code will generate a traceback pointing at the line after the one in which we've missed the closing parenthesis:

```python
# Python Code
1| print("Hello, world!"
2| print("This is my first Python program!")

# Terminal output
Traceback (most recent call last):
  File "my_python_file.py", line 2
    print("This is my first Python program!")
        ^
SyntaxError: invalid syntax
```

The reason this may happen is that Python allows for [implicit line continuation](https://docs.python.org/3/reference/lexical_analysis.html#implicit-line-joining) and will only notice the error when the expression does not continue as expected on the next line.
So, it's always a good idea to also check the line before the one mentioned in the traceback!

### More Information on Exceptions

Further information on exceptions can be found in the official Python documentation:

* [The built-in exceptions page](https://docs.python.org/3/library/exceptions.html) lists all the built-in exceptions along with a short description of the exception.
    If you're unsure of the meaning of an exception in your traceback, this is a good place to start.
* [The errors and exceptions chapter in the official tutorial ](https://docs.python.org/3/tutorial/errors.html) gives an overview of errors and exceptions in Python.
    Besides explaining what exceptions are, it also explains how to handle expected exceptions graciously to keep your application from crashing when an expected exception is raised and how to define custom exceptions specific to your application.

If you encounter an exception specific to an external module or package, it's usually a good idea to check the documentation of that package to see if the exception is documented.
Another option is to paste a part of the traceback, usually the last line, into your favorite search engine to see if anyone else has encountered a similar problem.
More often than not, you will be able to find a solution to your problem this way.
