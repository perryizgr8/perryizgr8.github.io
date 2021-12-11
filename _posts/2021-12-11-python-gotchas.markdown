---
layout: post
title:  "TIL: python gotchas"
categories: python
---
Thanks to `pylint`, I came across a couple of python gotchas that weren't obvious to me at first glance.

## Dangerous default value as argument
Python allows you to declare a default value for an argument, if it is not supplied by the caller. Like so:
{% highlight python %}
def badfunc(nums=[]):
    # function logic
{% endhighlight %}

Here, `badfunc` accepts an argument `nums` which is supposed to be a list. If you do not supply anything, this will be initialized to a list. You can do something like this:

{% highlight python %}
def badfunc(nums=[]):
    nums.append(100)
    nums.append(200)
    for num in nums:
        print(num)

badfunc()
{% endhighlight %}

The output will be:
{% highlight bash %}
100
200
{% endhighlight %}

If you would not have designated a default value, you could not append to it, since it would have been undefined. So it is useful in that way.

However, there is a strange gotcha hidden here. What happens if you call the function twice in succession?

{% highlight python %}
print('once:')
badfunc()
print('again:')
badfunc()
{% endhighlight %}

Output:
{% highlight bash %}
once:
100
200
again:
100
200
100
200
{% endhighlight %}

It appears as though the previous instance of `nums` is reused in subsequent calls to the function! I certainly didn't expect that. It behaves like a static variable inside the function. This unexpected behavior is why `pylint` will flag this usage as `warning| Dangerous default value [] as argument`.

You can avoid this quite easily by rewriting the function like this:
{% highlight python %}
def badfunc(nums=None):
    if nums is None:
        nums = []
    nums.append(100)
    nums.append(200)
    for num in nums:
        print(num)
{% endhighlight %}

## Undefined loop variable
Consider this useless piece of code:
{% highlight python %}
def fruit_printer(fruit):
    print(fruit)

def function_runner(func):
    print('running your function...')
    func()

fruits1 = ['apple', 'banana', 'guava']
fruits2 = ['pear', 'watermelon', 'mango']
for fruit in fruits1:
    function_runner(lambda: fruit_printer(fruit))
for fruit in fruits2:
    function_runner(lambda: fruit_printer(fruit))
{% endhighlight %}

If you run this, it works as expected:
{% highlight bash %}
running your function...
apple
running your function...
banana
running your function...
guava
running your function...
pear
running your function...
watermelon
running your function...
mango
{% endhighlight %}

However, `pylint` complains that `warning:(undefined-loop-variable) Using possibly undefined loop variable 'fruit' at line 11`.

Huh? There is no undefined usage of `fruit`. Every time I used it, was inside the loop.

I am unsure why `pylint` is freaking out about this, but one theory pointed out by a coworker is that `function_runner()` may not execute the supplied lambda immediately. It may be some sort of an async function runner (kind of like `futures`). In that case, the function may run when the loop variable `fruit` is out of scope.

The proper thing to do here is to pass the function and the argument separately to `function_runner()`. That way, the value of the variable will be copied over and you need not worry about lifetimes.