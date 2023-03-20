---
layout: post
title:  "Self-hosting a Google Photos alternative"
categories: photos
---
A story about my quest to avoid paying Google in perpetuity.

## Google's bait and switch
Google offered their excellent Google Photos app and backup service for many years, with unlimited photo/video backup. The only catch being that your media is compressed and uploaded. But the resulting quality was good enough that I did not mind. My wife and I used it for backing up all our photos, and sharing them with each other.

They ended the unlimited free tier in June 2021. Now we must pay a monthly rent to Google to be able to keep using it as our backup.

## Google's nonsensical pricing

| Plan     | Storage | Monthly Price |
|----------|---------|---------------|
| Basic    | 100 GB  | ₹130          |
| Standard | 200 GB  | ₹210          |
| Premium  | 2 TB    | ₹650          |

I know that my photo library is over 200 GB, maybe around the 1 TB mark. But it is continuously growing. I am sure it will cross 2 TB in the next 5 years, given the ever-increasing quality of our cameras.

So paying every month for 2 TB now, and then inevitably being forced to pay more and more indefinitely is not a very enticing thought. In my opinion, they should charge a low fixed amount (say ₹50) per month, regardless of the amount you're storing, plus a very low amount per gigabyte (say ₹0.0002). That way, everyone pays for the base service equally, and everyone also pays for the storage they are actually consuming.

## PhotoPrism
The first alternative I found was [PhotoPrism](https://www.photoprism.app/), a self-hosted app that you can run on your server, and access from your phone or web. Point it to a folder on your drive and it imports all photos and videos.

Pros:
- Easy to set up.
- Runs on docker, so platform-independent.
- Open source and free.
- Feature-rich, includes face recognition and a powerful search.
- Actively developed, few bugs.

Cons:
- No good way to backup from phone to server.
- No native apps on mobile, have to use horrible and clunky PWA.

The last one is extremely annoying. PWAs are simply not ready. It literally does not feel like a proper app. It feels like a web page. Each button press is laggy, every photo takes a while to load, all around a pain to use. Infuriatingly, it seems like there are no plans for a native app at all. Apparently, the PWA [offers an almost native app-like experience](https://www.photoprism.app/kb/compliance-faq#:~:text=At%20the%20moment%2C%20PhotoPrism%20does%20not%20have%20a,of%20all%20major%20operating%20systems%20and%20mobile%20devices). No, PhotoPrism, it doesn't.

There is an [unofficial Flutter app](https://github.com/thielepaul/photoprism-mobile), but it is currently incompatible with the latest version of PhotoPrism. As far as I can tell, it has been incompatible for over 2 years. So I don't have high hopes from this project.

## Immich
Recently, I stumbled upon [Immich](https://immich.app/), a self-hosted app that has the explicit aim of replacing Google Photos. To that end, it has native mobile apps that work very similar to Google Photos. The apps seem highly polished, and the server is easy to set up using docker compose.

Pros:
- Easy to set up.
- Runs on docker, so platform-independent.
- Open source and free.
- Slick native Android and iOS apps.

Cons:
- Not very feature-rich yet.
- Very active development means things are likely to break.
- Can't import existing photo library.

A strange quirk with Immich is that you can't point it to your existing photo library and have it scan it (as far as I can tell). You must upload photos from your phone using the backup feature, or upload pictures via the web app. In my opinion they went too far in replicating Google Photos here.

## Problem with Immich
I set up the server on my PC, downloaded the app on my phone and started the backup process. The backup always gets stuck on a particular video file. It's not overly huge, about 150 MB. No matter what I did, it always gets stuck on this file and the backup never completes.

## How my server connects to the internet
My "server" is just my PC in my bedroom. It runs Windows 11. I have set up a Cloudflare tunnel to expose a port to a particular DNS record. I input that DNS name in the Immich app's server setting. I need to do this because I don't have a public IP from my ISP, and all ports are effectively blocked due to a double NAT.

## Debugging
I had a suspicion that the issue had something to do with the tunnel. Since the upload gets stuck on a slightly large video, and not on a regular-sized photo, I wondered if the tunnel was restricting uploads above a certain limit. After all, Cloudflare's architecture is built to support small files, and that too in the other direction.

I started a python server using the [uploadserver](https://pypi.org/project/uploadserver/) package. It lets you download and upload files via a rudimentary web interface. I tried to upload a video file of about the same size:
```
~> curl -v 'https://mysite/upload' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary1dMEK7Ts8bf8AZTg' \
  -F "files=@/Users/parikshit/Downloads/clip.mp4"
*   Trying xxx.xxx.xxx.xxx:443...
* Connected to mysite (xxx.xxx.xxx.xxx) port 443 (#0)

...skipped...

< HTTP/2 413
< date: Mon, 20 Mar 2023 14:29:51 GMT
< content-type: text/html
< report-to: {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v3?s=******"}],"group":"cf-nel","max_age":604800}
< nel: {"success_fraction":0,"report_to":"cf-nel","max_age":604800}
< server: cloudflare
< cf-ray: *****-BLR
< alt-svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400
* HTTP error before end of send, stop sending
<
<html>
<head><title>413 Request Entity Too Large</title></head>
<body>
<center><h1>413 Request Entity Too Large</h1></center>
<hr><center>cloudflare</center>
</body>
</html>
```

As suspected, Cloudflare doesn't like it if you try sending large files in the opposite direction. Possibly their network is simply not optimised for that.

## Solution
There are two possible solutions I can think of.

1. Immich is open-source. I could contribute a patch that chunks larger files when uploading.
2. I could use a Wireguard or Tailscale tunnel between my PC and some cloud server, and use that to route my traffic.

I'll post an update when I manage to solve the issue.