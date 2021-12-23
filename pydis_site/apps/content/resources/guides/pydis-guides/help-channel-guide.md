---
title: Help Channels
description: How do help channels work in the Python Discord community?
icon: fab fa-discord
relevant_links:
    Asking Good Questions: ../asking-good-questions
    Role Guide: /pages/server-info/roles
    Helping Others: ../helping-others
---

On the 5th of April 2020, we introduced a new help channel system at Python Discord. This article is a supplementary guide to explain precisely where to go to find help.

We have two different kinds of help channels in our community - **Topical help channels**, and **general help channels**.
Where you should go depends on what you need help with.
These channels also attract different helpers, and move at different speeds, which affects the kind of help you're likely to receive, and how fast you get that help.

# Topical Help Channels

The topical help channels move at a slower pace than the general help channels.
They also sometimes attract domain experts - for example, `#async-and-concurrency` has CPython contributors who helped write asyncio, and in `#game-development` you can find the creators and maintainers of several game frameworks.
If your question fits into the domain of one of our topical help channels, and if you're not in a big hurry, then this is probably the best place to ask for help.

![List of topical help channels](/static/images/content/help_channels/topical_channels.png)

Some of the topical help channels have a broad scope, so they can cover many related topics.
For example, `#data-science-and-ai` covers scientific Python, statistics, and machine learning, while `#algos-and-data-structs` covers everything from data structures and algorithms to maths.

Each channel on the server has a channel description which briefly describes the topics covered by that channel. If you're not sure where to post, feel free to ask us which channel is appropriate in `#community-meta`.

# General Help Channels

Our general help channels cycle quickly, with the advantage of attracting a more diverse spectrum of helpers, and getting individual attention and help for your question. These channels are a great choice for generic Python questions, but they can be used for domain-specific Python help as well. 
Be sure to [ask good questions](../asking-good-questions) in order to give yourself the best chances of getting help. 

## How To Claim a Channel

There are always 3 available help channels waiting to be claimed in the **Python Help: Available** category.

![Available help channels](/static/images/content/help_channels/available_channels.png)

This message is posted when a channel becomes available for use:
![Channel available message](/static/images/content/help_channels/available_message.png)

In order to claim one, simply start typing your question into one of these channels. Once your question is posted, you have claimed this channel it will be moved down to the **Occupied Help Channels** category.

At this point you will have the **Help Cooldown** role which will remain on your profile until your help channel is closed (with the `!closed` command) or goes dormant due to inactivity.

# Frequently Asked Questions

## Q: For how long is the channel mine?

The channel is yours until it has been inactive for **10 minutes**, or 30 minutes until someone participate in the channel. When this happens, we move the channel down to the **Python Help: Dormant** category, and make the channel read-only. After a while, the channel will be rotated back into **Python Help: Available** for the next question. Please try to resist the urge to continue bumping the channel so that it never gets marked as inactive. If nobody is answering your question, you should try to reformulate the question to increase your chances of getting help.

![Channel dormant message](/static/images/content/help_channels/dormant_message.png)
*You'll see this message in your channel when the channel is marked as inactive.*

## Q: I don't need my help channel anymore, my question was answered. What do I do?

Once you have finished with your help channel you or a staff member can run `!dormant`. This will move the channel to the **Python Help: Dormant** category where it will sit until it is returned to circulation. You will only be able to run the command if you claimed the channel from the available category, you cannot close channels belonging to others.

## Q: Are only Helpers supposed to answer questions?

Absolutely not. We strongly encourage all members of the community to help answer questions. If you'd like to help answer some questions, simply head over to one of the help channels that are currently in use. These can be found in the **Python Help: Occupied** category.

![Occupied help channels](/static/images/content/help_channels/occupied_channels.png)

Anyone can type in these channels, and users who are particularly helpful [may be offered a chance to join the staff on Python Discord](/pages/server-info/roles/#note-regarding-staff-roles).

## Q: I lost my help channel!

No need to panic.
Your channel was probably just marked as dormant.
All the dormant help channels are still available at the bottom of the channel list, in the **Python Help: Dormant** category, and also through search.
If you're not sure what the name of your help channel was, you can easily find it by using the Discord Search feature.
Try searching for `from:<your nickname>` to find the last messages sent by yourself, and from there you will be able to jump directly into the channel by pressing the Jump button on your message.

![Dormant help channels](/static/images/content/help_channels/dormant_channels.png)
*The dormant help channels can be found at the bottom of the channel list.*
