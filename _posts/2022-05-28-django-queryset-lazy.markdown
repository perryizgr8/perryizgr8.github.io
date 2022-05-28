---
layout: post
title:  "TIL: Django QuerySets are lazy"
categories: python
---
I remember reading somewhere that Django QuerySets are lazy, they fetch only what is required, when it is required. I remember thinking to myself "Neat! Sounds like a great feature that lets me code without worry!". While that is mostly true, there are times when you can gain a lot of performance if you keep this fact in mind when writing your code.

{% highlight python %}
users = User.objects.filter(car__isnull=False)
{% endhighlight %}

This QuerySet will enumerate all users who have cars. Look at how we can use this inefficiently.

{% highlight python %}
for user in users:
    if user.car.color == "red":
       increase_insurance_premium(user)
{% endhighlight %}

Suppose there are 10000 users, out of which 5000 have cars. Out of those, 500 have red cars, who are the ones were actually interested in right now.

This implementation will make 5000 database queries, once every loop iteration, only to throw away the data in all but 500 cases. As you can imagine, database access is one of the slowest things your app ever does, and we must aim to optimize it.

Re-writing using the filter chaining feature:

{% highlight python %}
users = User.objects.filter(car__isnull=False).filter(car__color="red")
for user in users:
    increase_insurance_premium(user)
{% endhighlight %}

This reduces loop iterations and database queries to 500, thus saving both database operations and program runtime.