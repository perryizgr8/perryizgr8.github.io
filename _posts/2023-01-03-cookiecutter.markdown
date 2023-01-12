---
layout: post
title:  "Cookiecutter: making repetition easy"
categories: dev
---
Developing a web app is an exercise in balance. One critical aspect is to decide between the opposing tendencies of monolithisation and micro-services. Like most decisions, this is always a matter of degree. You can absolutely go too far in one direction and suffer for it.

As the app grows, especially if it is written in a "slow" language like Python, you will find yourself trying to jump for a micro-service for every new feature that comes your way. This is because it becomes much harder to maintain quality and performance in a Python/Django monolith as the codebase grows.

The general tendency in this case is to copy the existing Django project, make your new addition, remove or comment the existing unneeded stuff and deploy it somewhere else. But cruft accumulates, every bad decision made in the app carries forward.

The ideal thing to do in such situations is to create a new service from scratch, preferably in a faster language like Go or Rust. However it's hard to do, and takes a lot of time and effort. This additional delay is hard to justify for a small to medium feature.

In times like these, it is helpful if you have a ready-to-go template to start you off with basic scaffolding already in place. You can start from "Hello, world!" within a minute. Then add your required functionality.

Enter [Cookiecutter](https://github.com/cookiecutter/cookiecutter).

It's easy to create a template using Cookiecutter for a basic Go app that serves a REST API using [Echo](https://echo.labstack.com/). It's set up with common amenities and has a nice starting point for any service.

Have a look at my take at [it](https://github.com/parikshit-parspec/cookiecutter-go).