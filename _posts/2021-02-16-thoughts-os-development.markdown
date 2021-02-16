---
layout: post
title:  "Thoughts on System Software"
categories: C++
---
I have worked as a software engineer for 6 years now. At my first workplace, I worked on the system software that runs on [enterprise network switches](https://www.bing.com/images/search?q=campus%20network%20switch). 

## What is system software?
In its original usage, system software consisted of the components of the operating system running on a computer system. For a while, I did work on such software. This was a real-time OS, with strict time guarantees. It was a single-thread, single address-space OS. That means every piece of code, from critical network protocol logic, to the code that blinks LEDs on the front panel, ran in a sequential manner. If you try to dereference a null pointer in the CLI parser, your switch will crash and reboot, interrupting the network traffic.

Soon after I joined, however, my company moved to an entirely new, Debian Linux based OS. We were moving into a more civilized age. All the software we wrote ran in the userspace. Each logical unit runs as its own Linux process. A crash in the LED controller will not affect anything else at all. In fact it probably won't affect the LEDs either! The process will simply dump core, and restart, usually within milliseconds. It became a bit hard to describe this as "system software", but we kept thinking of ourselves as "system software engineers".

## Building system software
There is a difference between building a "system", and building an "app". For instance, the standard practice for any such shop as ours was to compile an OS image, that you would then install on a network switch. This is equivalent to copying an Ubuntu ISO image onto a flash drive, and installing it to a PC. This is time consuming in a number of ways:

1. Compiling takes time, because even if your change is small, the entire binary has to be re-built.
2. OS images are relatively large in size (hundreds of megabytes to gigabytes). Transferring them to the target takes time.
3. Installing the image takes time because this is basically an OS installation. This takes at least 15 minutes for a latest Linux distro, and even longer for Windows.
4. Debugging is cumbersome, since you need special mechanisms to attach an OS kernel to `gdb`.

## What changed with Linux?
When we switched to a Linux-based system running separate processes, it brought a lot of advantages with it.

1. You could now compile just an app.
2. You could simply copy the executable of that single app onto the switch and run it to look at your changes.
3. Debugging is way easier since now your code is simply a userspace process.

However, since we were still thinking in the old way, we never adopted many of these benefits. Standard practice still remained to compile the entire OS, with our apps, then install the huge OS image onto the switch. But these are small problems to solve, and we eventually did solve them.

## The bigger issue
Since our new OS was also designed with the old "OS development" mindset, we devised an efficient, state-based inter-process communication model that all apps needed to use. It would simplify development, and increase reliability by decoupling everything in the running system.

But the way this was designed, every app needed to link against a shared library that defines the schema for the entire system's configuration. For example, if I want the user to be able to turn on a port locator LED, I need to specify a json attribute that can store that setting.

This now needs to be known by a central database, which can keep track of all such attributes and facilitate communication between apps. To avoid having everyone to craft json queries and parse long json responses, we had a library with simple to use C interfaces. The problem is that every single app depends on this library now. Any change to any attribute's schema, by any feature, will necesitate re-linking or at least re-loading the shared library.

So we come back to compiling/linking everything for every small change. If you don't, things may work, or they may fail in frustrating ways.

## Is there a better way?
I think the key hurdle we need to cross to solve this issue is to stop thinking of ourselves as "system engineers" or that we are in the business of "OS development". We are writing userspace Linux programs, and packaging them up with a standard Linux distro.

Design every app as if you are designing it for a third-party OS. Don't couple things so tightly to your own infrastructure that it is impossible to untangle the mess. Have each app expose a standard API (could be using json, or protobuf), and plan to work with API versions x plus minus 1.

After that, it is just a matter of each app residing in its own repository, running its own tests, on its own release schedule. The entire system will still need to be tested in a simulated setting with the latest versions of each app, before pushing the OS update to critical network infrastructure, but this way you get rid of a lot of headaches that are simply holdovers from the past.
