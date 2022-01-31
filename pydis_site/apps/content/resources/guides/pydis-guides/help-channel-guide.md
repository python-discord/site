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

We have two different kinds of help channels in our community: **topical help channels** and **general help channels**.
The topical channels can be great for longer and broader discussions, whereas a general help channel might be more appropriate for specific troubleshooting. Individual topical channels may have a narrower audience than the general help channels, but that may also be to your advantage if the audience is very familiar with the area of Python you are struggling with.

# Topical Help Channels

The topical help channels move at a slower pace than the general help channels.
They also sometimes attract domain experts. For example, `#async-and-concurrency` has CPython contributors who helped write asyncio, and in `#game-development` you can find the creators and maintainers of several game frameworks.
If your question fits into the domain of one of our topical help channels, and if you're not in a big hurry, then this is probably the best place to ask for help.

![List of topical help channels](/static/images/content/help_channels/topical_channels.png)

Some of the topical help channels have a broad scope, so they can cover many related topics.
For example, `#data-science-and-ai` covers scientific Python, statistics, and machine learning, while `#algos-and-data-structs` covers everything from data structures and algorithms to maths.

Each channel on the server has a channel description which briefly describes the topics covered by that channel. If you're not sure where to post, feel free to ask us which channel is appropriate in `#community-meta`.

# General Help Channels

Our general help channels cycle quickly, with the advantage of attracting a more diverse spectrum of helpers, and getting individual focus and attention on your question. These channels are a great choice for generic Python help, but can be used for domain-specific Python help as well.

## How to Claim a Channel

There are always three help channels waiting to be claimed in the **Available Help Channels** category.

![Available help channels](/static/images/content/help_channels/available_channels.png)
*The Available Help Channels category is always at the top of the server's channel list.*

![Available message](/static/images/content/help_channels/available_message.png)
*This message indicates that a channel is available.*

In order to claim one, simply ask your question into one of the available channels. Be sure to [ask good questions](../asking-good-questions) in order to give yourself the best chances of getting help!

![Channel claimed embed](/static/images/content/help_channels/claimed_channel.png)
*This messages indicates that you've claimed the channel.*

At this point you will have the **Help Cooldown** role which will remain on your profile until your help channel is closed (with the `!close` command) or goes dormant due to inactivity. This ensures that users can claim only one help channel at any given time, giving everyone a chance to have their question seen.

## Frequently Asked Questions

### Q: How long does my help channel stay active?

The channel remains open for **30 minutes** after your last message, or 10 minutes after the last message sent by another user (whichever time comes later).

![Channel dormant message](/static/images/content/help_channels/dormant_message.png)
*You'll see this message in your channel once it goes dormant.*
### Q: No one answered my question. How come?

The server has users active all over the world and all hours of the day, but some time periods are less active than others. It's also possible that the users that read your question didn't have the knowledge required to help you. If no one responded, feel free to claim another help channel a little later.

If you feel like your question is continuously being overlooked, read our guide on [asking good questions](../asking-good-questions) to incease your chances of getting a response.

### Q: My question was answered. What do I do?

Go ahead use the `!close` command if you've satisfactorily solved your problem. You will only be able to run this command in your own help channel, and no one (outside of staff) will be able to close your channel for you.

Closing your help channel once you are finished leads to less occupied channels, which means more attention can be given to other users that still need help.

### Q: Can only Helpers answer help questions?

Definitely not! We encourage all members of the community to participate in giving help. If you'd like to help answer some questions, head over to the **Occupied Help Channels** or **Topical Chat/Help** categories.

Before jumping in, please read our guide on [helping others](../helping-others) which explains our expectations for the culture and quailty of help that we aim for on the server.

Tip: run the `!helpdm on` command in `#bot-commands` to get notified via DM with jumplinks to help channels you're participating in.

### Q: What are the available, occupied, and dormant categories?

The three help channels under **Available Help Channels** are free for anyone to claim. Claimed channels are then moved to **Occupied Help Channels**. Once they close, they are moved to the **Python Help: Dormant** category until they are needed again for **Available Help Channels**.

### Q: Can I save my help session for future reference?

Yes! Because the help channels are continuously cycled in and out without being deleted, this means you can always refer to a previous help session if you found one particularly helpful.

Tip: reply to a message and run the `.bm` command to get bookmarks sent to you via DM for future reference.

### Q: I lost my help channel!

No need to panic. Your channel was probably just closed due to inactivity.
All the dormant help channels are still available at the bottom of the channel list, in the **Python Help: Dormant** category, and also through search.
If you're not sure what the name of your help channel was, you can easily find it by using the Discord Search feature.
Try searching for `from:<your nickname>` to find the last messages sent by yourself, and from there you will be able to jump directly into the channel by pressing the Jump button on your message.

![Dormant help channels](/static/images/content/help_channels/dormant_channels.png)
*The dormant help channels can be found at the bottom of the channel list.*
