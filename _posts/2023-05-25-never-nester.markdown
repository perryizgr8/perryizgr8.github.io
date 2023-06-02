---
layout: post
title:  "Nested code considered harmful"
categories: programming
---
I recently watched [a YouTube video](https://youtu.be/CFRhGnuXG-4) that presented the benefits of never nesting your code more than a few levels. I've felt that it expressed in words what I'd always known within. So let me explain.

## Nesting
Consider the following function that performs the common spline reticulation procedure.

{% highlight cpp %}
int reticulate_the_splines(network, curves) {
    if(curves.size() > 0) {
        if(network.status() == ONLINE) {
            for(auto c: curves) {
                network.add_curve(c)
            }
        } else {
            std::cout << "The network is not ONLINE.";
        }
    } else {
        std::cout << "No curves to add to the network.";
    }
}
{% endhighlight %}

Inside the function, there are up to 3 levels of nesting. The deepest nesting is on the line:

{% highlight cpp %}
                network.add_curve(c)
{% endhighlight %}

In more complicated functions, it is common to encounter even deeper levels of nesting, due to `if...else` conditions and loops.

## Refactoring
Let's try to decrese the level of nesting in the above function.

{% highlight cpp %}
int reticulate_the_splines(network, curves) {
    if(curves.size() <= 0) {
        std::cout << "No curves to add to the network.";
    }
    if(network.status() != ONLINE) {
        std::cout << "The network is not ONLINE.";
    }
    for(auto c: curves) {
        network.add_curve(c)
    }
}
{% endhighlight %}

This function only has at most one level of nesting. I find it to be much more readable. The control flow seems to be more clearly visible. At a glance you can understand that having no curves or a network that's not online are error states that prevent the function from carrying out its operation.

Once the error checking is out of the way, it is very clear that the function loops over `curves` and adds each to the `network`. In the nested version, this main logic was buried deep beneath condition checks, and the error handling was dispersed across the entire length of the function.

The video makes a very detailed and visual point. If you aren't convinced by my justification here, be sure to give it a watch!