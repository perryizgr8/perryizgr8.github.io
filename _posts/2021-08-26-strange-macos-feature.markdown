---
layout: post
title:  "Strange MacOS feature that clobbers 'find' textboxes"
categories: UI
---
Ever since I started using a Macbook as my work laptop, I've been getting irritated by this feature. It blurs the line between feature and bug, to be honest.

Suppose I have a reference open in Chrome, and I search for a term `foo` on the page using `Cmd+F`. Now, reading the text, I find out that I need to go and change the `bar` function in my code. So I `Cmd+Tab` to my editor, and `Cmd+F` for `bar`, and start changing my code.

Halfway through, I want to re-read something in the reference, so I `Cmd+Tab` back to Chrome, but now Chrome has put `bar` in the find box and I'm somewhere else on the page! Time to get out of my code and try to recall what I had used as the search term here.

This is such a bad design that I absolutely don't understand why anybody would think this is a good idea. Apparently some people on the internet seem to love it though. And Apple engineers found it important enough to include in their OS. I just wish they would have given an option to turn it off.
