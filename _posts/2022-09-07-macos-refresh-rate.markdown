---
layout: post
title:  "MacOS problems with monitor refresh rate"
categories: Apple
---
I have been using a Macbook 13 inch for work for a bit more than two years now. I like to use my nice gaming monitor when I work from home, which I have been doing for more than 3 years now.

I had a version of the laptop which had an Intel CPU in it. It had no problems connecting to my monitor at its native resolution of 2560x1440 at 144 Hz. I barely gave it a thought, the connection never gave me any problems.

For the last 4 months however, I have been using a laptop that is identical to the first one, just with an Apple ARM CPU inside. I must say the experience with this machine has been very annoying when it comes to anything to do with connecting the monitor.

## Variable refresh rate has horrible artifacting
This is a FreeSync monitor, which means it can sync its refresh rate to the content being displayed. In games, this is great because you don't need V-Sync in software, and makes everything looks smoother and without any screen tears.

This mode worked great with the Intel laptop, and it still works perfectly with my gaming PC. With the ARM Macbook, it creates a lot of flickering. I can notice it in my periferal vision and it annoys me to no end.

## Refresh rate settings don't stick
The fix is to set the monitor on a fixed refresh rate from MacOS display settings. If I set it to 144 Hz, the flickering goes away and I get a buttery smooth screen. But MacOS will revert to the variable mode every time you reconnect. It just won't remember the setting. They have also changed the settings app, making it an amazingly tedius process to modify this option now.

## Automate it
MacOS ships with a scripting language called Apple Script. You can use it to automate a lot of UI stuff in the OS. Here's my small script to go into the specific menu 3 layers deep and change the monitor to 144 Hz fixed. I still have to run it every time I connect the monitor, but it's just a click and a 5 second wait. Here's my script in the hope it helps someone else facing the same issue.

<script src="https://gist.github.com/perryizgr8/d3fdb67f0c0884ecd713ddd4177a4c31.js"></script>

## Bonus gotcha: desktop switching speed is linked to the refresh rate
I am a heavy user of virtual desktops. I have a mouse with extra buttons dedicated to switch to the right or left desktop. Changing the refresh rate to 144 Hz slows down the transition between desktops by a lot. It is extremely infuriating to wait for the computer to complete its stupid animation before I am allowed to continue my work. I haven't found any fix to this except just switching to 60 Hz. It makes no sense.
