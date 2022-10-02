---
title: "Code Reviews: A Primer"
description: An introduction and guide to the world of code reviews!
icon: fab fa-github
toc: 3
---

## The What, the Why, and the How

##### The What & The Why

This is a guide that will cover the unsung hero of the coding process: code reviews.
Whether you're working professionally or on an open-source project on GitHub, you'll find that code reviews are an essential part of the process.

So what exactly is a code review? The closest thing to compare it to is proofreading.
In proofreading, you look at an essay someone wrote and give suggestions on how things could be written better or point out mistakes that the writer may have missed.
Code reviewing is the same way.
You're given some code that someone wrote and see if you can find ways to improve it or point out mistakes that the coder may have missed.

"Hemlock", you might say, "Why should I care? Why would this be important?" The thing to remember is that coding is a team effort.
Code reviews help the programs we write to be the very best they can be.
We're all human, and mistakes are made, but by working together, we can correct those mistakes (as best we can) before they get merged into production.
Even if you're not the best coder in the world, you may spot things that even a professional programmer might miss!

##### The How

And now for the most important part of the guide.
This will detail the general process of how to write a code review, what to look for, how to do basic testing, and how to submit your review.
Big thanks to Akarys, who wrote this section of the guide!

---

## Our Code Review Process

> Note: Everything described in this guide is the writer's way of doing code reviews.
> This is purely informative; there's nothing wrong with branching off of this guide and creating your own method.
> We would even encourage you to do so!

We usually do reviews in 3 steps:

1. Analyze the issue(s) and the pull request (PR)
2. Analyze and review the code
3. Test the functionality

So let's jump right into it!

## Step 1: Analyzing the Issue(s) and the Pull Request

Every issue and pull request has a reason for being.
While it's possible to do a code review without knowing that reason, it will make your life easier to get the full context of why it exists and what it's trying to do.
Let's take a look at how we can get that context.

### Analyzing the Issue(s)

In almost every case, the PR will have some linked issues.
On the right-hand side of the PR's page in GitHub, you'll see a section labeled "Linked issues".
Reading the issue(s) and their comments will allow you to know why certain decisions were made.
This will be invaluable when you review the implementation.
The author of the issue may suggest the code be written one way but the PR ends up writing it another.
This happens during the development process: New ideas are thought of, optimizations are found, other ideas are removed, etc.
Even if there are changes, functionality, or fixes that the issue covers should be covered by the PR.

### Analyzing the PR

The author of the PR will (or should) have made comments detailing how they implemented the code and whether it differs from the proposed implementation in the issue.
If they do things differently than suggested, they should also have explained why those changes were made.

Remember that just like in the issue, PR comments have value.
Some of your future concerns about the implementation or even review comments may have already been discussed.
Although, if you disagree with the decision, feel free to comment about it! The more input we get from our reviewers, the better!
The last thing you need to remember is that commit messages are important. They're notes from the PR's author that give details as to what they changed. This can help you keep track of what change happened at what point in development, which can help you get some context about a given change.

Now that you know more about the changes, let's start the fun stuff: the code review!

## Step 2: Reviewing the Code Itself

After all, that's why we're here! Let's dive right in!

### The 1st Read: Getting a Sense of the Code

It's impossible to understand the code in the PR your first time through.
Don't be surprised if you have to read over it a few times in order to get the whole picture.
When reading the code for the first time, we would recommend you to only try to get a sense of how the code flow.
What does this mean, you may ask?
Well, it is about knowing how every individual piece fits together to achieve the desired goal.

Pay close attention to how the functions and classes are called.
Make sure to read the comments and docstrings; they'll help explain sections of the code that may be confusing.
Finally, remember that your goal at the moment is to get a general idea of how the code achieves its goal.
You don't have to understand the finer points at this stage.

### The 2nd Read: Looking at Every Little Detail

Now that you know how the code flows, you can take a closer look at the code.
Comment on anything you think could be done better.
This includes, but is not limited to:

* The general structure of the code
* The variable names
* The algorithm(s) used
* The use or the lack of use of already existing code or a library
* Blocks of code that could benefit from comments
* Spelling
* Anything you see that doesn't seem quite right is worth commenting on. Discussing the things you find benefits everyone involved!

Another good technique is to imagine how you would have implemented a specific functionality and compare it with the proposed implementation.
GitHub has a feature allowing you to mark files as read, and it's recommended to take advantage of it so that you don't lose your place if you take a break.
Now that you know what to comment on, let's take a closer look at how to comment.

### Leaving Good Review Comments

When leaving a comment, don't forget that we can't know what you're thinking; you have to write it down.
Your comment should describe why you think this should be changed and how you propose to change it.
Note that you can omit the latter in some cases if it is outside of your area of expertise for instance.
There's nothing wrong with using your comments to ask questions! If there's something you're not sure about, don't hesitate to ask in your comment.
It might indicate that the PR's author needs to add comments, change variable or function names, or even change a block of code entirely.

GitHub has a handy feature that allows you to leave suggestions.
This means that the author can drop your suggestion into their PR with a click of a button.
If you provide one, great! It will speed up the review process even more!
On the opposite side, note that you aren't required to do all of that when leaving a comment. If you are fixing a typo, leaving a suggestion is enough.

If you have concerns about a particular piece of code for example a race condition, it is totally okay to point it out in a comment, even if you don't have a suggested way to fix it.

## Testing the Functionalities

A code review isn't only about looking at the code; it's also about testing it.
Always try to make sure that the code is working properly before approving the changes.

Something else to note: you are free to review code without testing functionality.
That's totally okay! Just make sure to mention when you submit your review.

### Reviewing the Functionality

When reviewing functionality, keep asking yourself how you would have designed it and then compare your idea with the implementation.
Note that you are allowed to give suggestions about how the functionality should be designed.

Start with the basic usages and work your way up to more complicated ones.
Verify that everything is working as intended.
If it isn't, leave a comment giving what you've done, what should have happened, and what actually happened, along with any potential logs or errors you could have.
If you like, you can even try to pinpoint the issue and find a fix for it. We would be very grateful if you did!

### Objective: Break it

Good functionality should be able to handle edge cases.
Try to throw every edge case you might think of and see how it responds. This might not be needed in some cases, but it's essential for security-related work.
If the implementation has a security breach, you should absolutely find it! Just like in the previous section, if you find something and comment on it, great!
If you manage to find a way to fix it and suggest the fix, even better!

### But what if the Project doesn't even start?

This is a tricky one. Sometimes the project won't even start, keeping you from testing it all together.

In this case, you should try to investigate if it is failing because of an error in the code. If it ends up being because of the functionality, you should comment on that.

If you aren't sure why it isn't starting, feel free to ask us!

## Final Words

You did it!
You are now ready to take on the wild world of code reviewing!
We know that process can seem long, tedious, and not feel like a necessary task, but it is!
We are very grateful to you for reading through this and for your potential future code reviews.
We couldn't move forward without you.
Thank you!
