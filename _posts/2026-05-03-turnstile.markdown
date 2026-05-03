---
layout: post
title:  "Building Turnstile, a browser selector for Windows"
categories: projects
---
I use multiple browsers on my Windows machine. Edge for work stuff, Firefox for personal browsing, and Chrome — well, Chrome is there just to run Playwright tests. This is not an unusual setup. Many people I know keep at least two browsers around.

The problem starts when you click a link somewhere and it opens in the wrong one. Slack link? Should probably go to Edge since I'm signed into work accounts there. A YouTube link from WhatsApp? Firefox, because that's where I'm logged into my personal Google account. Windows makes you pick one default browser and that's that. Every single link opens in that one browser, regardless of context.

I got tired of copying links, switching browsers, and pasting them. So I built [Turnstile](https://turnstile.perryizgr8.com).

## How it works

Turnstile registers itself as your default browser. When you click a link anywhere on your system, instead of opening it directly, a small popup appears near your cursor showing all your installed browsers. Each one has a number next to it. Press that number, and the link opens in that browser. Press Escape and nothing happens. The whole thing takes less than a second.

It also detects browser profiles. If you have multiple Edge profiles or Firefox profiles set up, they show up as separate entries in the picker. If you have a work profile and a personal profile in Edge, you can pick which one to use right from the popup.

## Automation rules

After using it for a while, I noticed that I always open Slack links in Edge, and YouTube links in Firefox. So I added automation rules. You can define a rule that says "always open links matching `*.slack.com` in Edge", or "always open links from the Slack app in Firefox". Turnstile matches the URL against your rules and skips the picker entirely if it finds a match.

Rules can match on domain patterns or regular expressions, and you can also filter by the application that opened the link. So you can say "links from Discord should always open in Firefox" and that works too.

## Rule suggestions

This is my favourite feature. Turnstile watches which browser you pick for each domain and source app. After a few consistent choices, it suggests a rule. It tells you something like "You've opened links from slack.com in Edge 12 out of 13 times. Create a rule?" If the suggestion makes sense, you accept it and never have to pick again for that domain.

It won't badger you with suggestions. It needs at least 5 events and 85% consistency before it even brings it up. And if you dismiss a suggestion, it won't ask again.

## Source app detection

This was a fun one to implement. When you click a link in an app, Windows passes the URL to the default browser, but doesn't tell the browser which app sent it. Turnstile works around this by using P/Invoke to call into ntdll.dll and figure out which process actually invoked it. If that fails, it falls back to checking which window was in the foreground. This is how it can let you create rules based on which app the link came from, not just the URL.

## How I built it

Turnstile is a WPF app written in C# on .NET 9. I went with WPF because it's the simplest way to get a lightweight, native-looking popup on Windows. The picker window positions itself near your cursor, animates in, and auto-closes if you click away from it.

All the configuration — rules, browser order, usage data — lives in JSON files under `%LOCALAPPDATA%\Turnstile\`. No database, no background service, nothing running when you're not picking a browser.

## Where to get it

You can find it on the Microsoft Store by searching for "Turnstile". More details at [turnstile.perryizgr8.com](https://turnstile.perryizgr8.com).