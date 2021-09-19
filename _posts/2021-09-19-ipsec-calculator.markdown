---
layout: post
title:  "IPsec overhead calculator"
categories: projects
---
Something I have been working on for the last few weekends is this [IPsec overhead calculator](https://ipsec-overhead-calculator.web.app).

IPsec is a scheme to encrypt IP traffic between two nodes. A common question that comes up when deciding to deploy it is about the overheads introduced by it. You specify the original packet size, and choose which options you would enable, and I calculate the various overheads in the final packet.

Currently this supports only IPv4, because that is what I have worked with. The web app is made using Flutter and Dart. You can look at the code in my [Github repo](https://github.com/perryizgr8/ipsec-overhead-calculator).
