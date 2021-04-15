---
title: Helping Others
description: The staff take on how to help others in our community.
icon: fab fa-discord
relevant_links:
    Asking Good Questions: ../asking-good-questions
    Help Channel Guide: ../help-channel-guide
    Code of Conduct: /pages/python-discord-code-of-conduct/
---

Python Discord has a lot of people asking questions, be it in the help channels, topical channels, or any other part of the server.
Therefore, you might sometimes want to give people the answers you have in mind.
But you might not be sure how best to approach the issue, or maybe you'd like to see how others handle it.
This article aims to present a few of the general principles which guide the staff on a day-to-day basis on the server.

## Understanding the Problem

Some people are good at asking for help.
They might be able to present their problem accurately and concisely, in which case discussing the problem and giving tips is simple and straight-forward.
But not everyone might be able to do that for their current issue.
Maybe they just don't know what they don't know.

If you feel like there's a gap in your understanding of the problem, it's often a good first step to query the asker for more information. Some of this information might be:

*  More code
*  The way in which the code doesn't work (if that is the issue), be it an exception message with traceback, undesired output, etc.
*  You can sometimes infer what the problem is yourself by requesting short examples of the desired output for specific input.

At this point, it's probably better being safe than sorry.
You don't want to accidentally pursue a direction that isn't even related to the real issue, as it could lead to frustration on both sides.
Beginners especially can be prone to asking a question which presents their attempt at solving the problem, instead of presenting the problem itself.
This is often called an [XY problem](https://xyproblem.info/).

Even if eventually you can't help, simply clarifying what the problem is can help others join in, and give their input.

> #### Example 1:
> A person might ask: *"How do I look at the values inside my function from outside?"*
>
> What they might be asking is: *"How do I return a value from a function?"*


## Understanding the Helpee

Assuming you know what the problem is, it's vital to gauge the level of knowledge of the person asking the question.
There's a stark difference between explaining how to do something to someone experienced, who only lacks knowledge on the specific topic; and someone who is still learning the basics of the language.

Try adjusting the solutions you present and their complexity accordingly.
Teaching new concepts allows the helpee to learn, but presenting too complex of a solution might overwhelm them, and the help session might not achieve its purpose.

> #### Example 2:
> A user might ask how to count how often each word appears in a given text.
> You might lean towards solving it using `collections.Counter`, but is it really the right approach?
> If the user doesn't know yet how to update and access a dictionary, it might be better to start there.

Generally, you should consider what approach will bring the most value to the person seeking help, instead of what is the most optimal, or "right" solution.

Usually, understanding a person's level can be achieved after a short conversation (such as trying to understand the problem), or simply by seeing the person's code and what they need help with.
At other times, it might not be as obvious, and it might be a good idea to kindly inquire about the person's experience with the language and programming in general.


## Teach a Man to Fish...

The path is often more important than the answer.
Your goal should primarily be to allow the helpee to apply, at least to a degree, the concepts you introduce in your answer.
Otherwise, they might keep struggling with the same problem over and over again.
That means that simply showing your answer might close the help channel for the moment, but won't be very helpful in the long-term. 

A common approach is to walk the helpee through to an answer:

* Break the task into smaller parts that will be easier to handle, and present them step by step.
    Try to think of the order of the steps you yourself would take to reach the solution, and the concepts they need to understand for each of those steps.
    If one step requires the helpee to understand several new concepts, break it down further.
* Ask instructive questions that might help the person think in the right direction.

> #### Example 3:
>
> **user**: "Hey, how can I create a sudoku solver?"  
> *helper1 proceeds to paste 40 lines of sudoku solving code*  
> **helper2**: "Are you familiar with lists / recursion / backtracking?"  
> *helper2 proceeds to give the information the user lacks*
>
> With the first replier, there's a much smaller chance of the helpee understanding how the problem was solved, and gaining new tools for future projects.
> It's much more helpful in the long run to explain the new concepts or guide them to resources where they can learn.
>
> This is also an example of gauging the level of the person you're talking to.
> You can't properly help if you don't know what they already learned.
> If they don't know recursion, it's going to take a slower, more detailed approach if you try to explain backtracking to them.
> Likewise if they're not familiar with lists.
>
> The same applies to presenting external resources.
> If they only just started programming, pasting a link to the Python documentation is going to be of little help.
> They are unlikely to be able to get around that website and understand what you expect them to read. In contrast, for a more seasoned programmer, the docs might be just what they need.


## Add a Grain of Salt

Giving people more information is generally a good thing, but it's important to remember that the person helped is trying to soak in as much as they can.
Too much irrelevant information can confuse them, and make them lose sight of the actual solution.
Presenting a solution that is considered a bad practice might be useful in certain situations, but it's important to make sure they are aware it's not a good solution, so they don't start using it themselves.

> #### Example 4:
>
> **user**: "How can I print all elements in a list?"  
> **helper1**: "You can do it like so:"  
>
>     for element in your_list:
>         print(element)
>
> **helper2**: "You can also do it like this:"  
>
>     for i in range(len(your_list)):
>         print(your_list[i])
>
> The second replier gave a valid solution, but it's important that he clarifies that it is concidered a bad practice in Python, and that the first solution should usually be used in this case.


## It's OK to Step Away

Sometimes you might discover you don't have the best chemistry with the person you're talking to.
Maybe there's a language barrier you don't manage to overcome.
In other cases, you might find yourself getting impatient or sarcastic, maybe because you already answered the question being asked three times in the past hour.

That's OK- remember you can step away at any time and let others take over.
You're here helping others on your own free time (and we really appreciate it!), and have no quotas to fill.

At other times, you might start talking with someone and realize you're not experienced in the topic they need help with.
There's nothing wrong with admitting you lack the specific knowledge required in this case, and wishing them good luck.
We can't know everything.

Remember that helping means thinking of what's best for them, and we also wouldn't want to see you become agitated.
We're all here because we enjoy doing this.


## Respect Others Giving Help

You might sometimes see others giving help and guiding others to an answer.
Throwing in additional ideas is great, but please remember both teaching and learning takes concentration, and you stepping in might break it.
You might have another idea to suggest, but you see that there's already a person helping, and that they're handling the situation.
In that case, it might be a good idea to patiently observe, and wait for a good opportunity to join in so as to not be disruptive.
