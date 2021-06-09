## Researching the question
While we're always happy to help, learning the same skills that we use to answer your questions will help you become a stronger developer. These are some of the steps we take when answering questions:

* Reading the official documentation for whatever library you're working with
* Use a debugger to inspect your code
* Examine the traceback when your code raises an exception
* Do some research online - for example, on Stack Overflow
* Read the source code for whatever you're working with

Essentially, doing your research is the first step towards a solution to any problem.
If your problem isn't extremely general, we're going to be doing exactly these steps ourselves when helping you, so doing the legwork beforehand saves everyone a lot of time.

If none of the above steps help you or you're not sure how to do some them, feel free to ask us for help.


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

### Syntax Errors: The Error is Sometimes in the Line Before the Error Message

Sometimes, the actual error is in the line just before the one referenced in the traceback. To get help with syntax errors, provide a few lines before and after the one shown in the error message.


### Exceptions from External Packages

If you encounter an exception specific to an external module or package, it's usually a good idea to check the documentation of that package to see if the exception is documented.
Another option is to paste a part of the traceback, usually the last line, into your favorite search engine to see if anyone else has encountered a similar problem.
More often than not, you will be able to find a solution to your problem this way.
