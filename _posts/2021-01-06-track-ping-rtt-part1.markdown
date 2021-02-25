---
layout: post
title:  "Tracking ping RTT to websites - part 1"
categories: raspberry-pi
---
In my quest to employ my Raspberry Pi to some use, I thought why not track ping round trip times to various popular websites. This would be less likely to run into the resource constraints that ruined my [speed test project](https://perryizgr8.github.io/raspberry-pi/2020/09/20/monitoring-speed-rpi.html), since the Pi's network link wouldn't be saturated. Also I decided to use `go` this time instead of `python`, for performance.

## Putting together the program
Go has a great ecosystem with people having written hundreds of packages for common stuff. You can usually import them from GitHub and use them in your project. I used the following:
1. [go-ping](https://github.com/go-ping/ping) - Pings an address and returns various statistics.
2. [go-chart](https://github.com/wcharczuk/go-chart/) - Lets you draw charts from data.

You can look at my code on [GitHub](https://github.com/perryizgr8/pinger). Some explanation about the program follows.

### [mainpage.html](https://github.com/perryizgr8/pinger/blob/master/mainpage.html)
This is the HTML template used to construct the page that is shown in your browser. There is a textbox with a list of websites you'd like to ping, a button to trigger the ping, and a bar chart showing results from last run.

### [webpage.go](https://github.com/perryizgr8/pinger/blob/master/webpage.go)
This is the only piece of code I wrote. `main()` serves the `assets` directory to show the chart, and registers `handler()` for servicing requests to `/`. 

The `handler()` checks the HTTP method used by the client. If it is a `GET`, it displays a default chart `output0.png`. This is just a result we will show before you have run any of your own pings. 

If it is a `POST` then we read the list of sites to ping, pass it to `go-ping` and plot the average RTT for each website using `go-chart`. Then we serve the newly generated chart.

## Try it yourself
Follow the [readme](https://github.com/perryizgr8/pinger/blob/master/README.md) if you'd like to try on your own. This should work on any Raspberry Pi, or even your laptop.

## Future plans
Note that this is part 1. I would like to eventually be able to run this in the background on my pi and have the webpage show a historical chart, instead of just an instantaneous result.