---
layout: post
title:  "C macro gotcha"
categories: C macros programming gotcha
---
I'll try to describe the incident that inspired me to start this blog.

The C language has a pre-processor built-in. Before the actual compilation, the human-written code is passed through the pre-processor. It is amost turing complete, according to the geniuses at stack overflow. I find it amazing that the pre-processor itself is capable enough to do many things for which people would expect to need a scripting language.

However, this power and flexibility comes at a price. The pre-processor directives are ugly and hard to read, at least for me. And some times the statements do something you never expected.

In our codebase, we have a macro defined like this:

{% highlight C %}
#define LENGTH_OF_HARDWARE_SPECIFIC_STRUCT \
    sizeof(struct another_arcane_struct) + WEIRD_OFFSET
{% endhighlight %}

Here we define `LENGTH_OF_HARDWARE_SPECIFIC_STRUCT` to be the sum of two values, one size and the other an arbitrary offset. Now let's use this macro in a piece of code that calculates the size of a struct contained within a larger struct.

{% highlight C %}
printf("size of the real data = %d", sizeof(struct big_struct) -
    LENGTH_OF_HARDWARE_SPECIFIC_STRUCT);
{% endhighlight %}

Assuming `sizeof(struct big_struct)` is 100 and `LENGTH_OF_HARDWARE_SPECIFIC_STRUCT` is 30, what do you expect to be printed? 

Hint: It's not 70.

You see, the pre-processor is a simple text replacement machine. The argument that is passed to the `printf()` becomes `sizeof(struct big_struct) - sizeof(struct another_arcane_struct) + WEIRD_OFFSET`. The calculated value is _A - B **+** C_ instead of _A - B **-** C_ that I was expecting.

The fix is simple: enclose the macro definiton in parentheses.

{% highlight C %}
#define LENGTH_OF_HARDWARE_SPECIFIC_STRUCT \
    (sizeof(struct another_arcane_struct) + WEIRD_OFFSET)
{% endhighlight %}

I knew about this gotcha from the first time I read about macros, but it still caught me by surprise. I hope to be more careful about this.

PS: I also hope to post regularly to this blog.
