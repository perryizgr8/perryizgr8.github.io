---
layout: post
title:  "You cannot mark a neighbor STALE in old Linux"
categories: C linux ARP programming
---
Reporting another ARP quirk with the Linux kernel.

On versions lower than 4.9.0, the kernel does not let you modify the stale of any neighbor from `NUD_CONNECTED` to `NUD_STALE`. I don't know what reasoning led to this behavior or if this was a bug, but it works fine in later versions.

As with the last such weirdness, this really only matters if you want to implement a userspace ARP app but still want the kernel to handle standard networking tasks.

The workaround is just to mark the neighor `NUD_FAILED` and then immediately mark it `NUD_STALE`.

Another thing to note is that when a stale neighbor transitions to `NUD_DELAY` due to network activity, the kernel will not notify you about this even if you have registered for the `RTM_GETNEIGH` category via netlink.
