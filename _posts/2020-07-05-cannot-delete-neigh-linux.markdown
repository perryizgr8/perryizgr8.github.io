---
layout: post
title:  "You cannot delete neighbors in Linux"
categories: C linux ARP programming
---
Linux maintains a list of known IP neighbors. You can look at the list using the `iproute2` family of commands.

{% highlight bash %}
$ ip neigh show
192.168.0.1 dev enp0s3 lladdr 51:53:00:17:34:09 REACHABLE
{% endhighlight %}

You can add neighbors, change their details or modify the state. But you cannot delete a neighbor. There is a command to delete `ip neigh del` but it just puts the neighbor in the `NUD_FAILED` state. The entry still persists. Linux will remove it only when it feels like it.

It looks like Linux won't let you delete neighbors even if you're using the `netlink` interface. This was surprising to me, since I usually thought of `netlink` as a form of direct control over the kernel.

This could have real consequences if you ever want to implement a userspace ARP app, but still want the kernel to perform basic network functions.