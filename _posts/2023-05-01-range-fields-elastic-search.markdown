---
layout: post
title:  "How to store ranges in Elasticsearch"
categories: elasticsearch
---
*This is part 1, read part 2 of this series [here](/_posts/2023-05-08-range-fields-elastic-search-2.markdown).*

Elasticsearch is a great index and document based search system. It's amazing for storing a bunch of data and retrieving the right bit very quickly. It has a rich querying system that is highly flexible and overall it's a drop-in, batteries-included search engine that you can host.

I recently found out that Elasticsearch supports range field types. Instead of assigning a single value to a field, you can instead put in a range. These are called [range field types](https://www.elastic.co/guide/en/elasticsearch/reference/current/range.html#range). You can then make [ranged queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) to look up these kind of fields.

Suppose you want to store the attributes of TVs in your index. One of those is the brightness of the TV which is commonly measured in nits. Let's create an index with a range field that can store this info.

{% highlight JSON %}
PUT televisions_index
{
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "brightness": {
                "type": "integer_range"
            }
        }
    }
}
{% endhighlight %}

Now we have an index ready to accept documents about each TV we want to store. Let's store our first TV. This is a Sony Bravia TV whose screen brightness can vary from 100 nits to 300 nits.

{% highlight JSON %}
PUT televisions_index/_doc/sony_bravia
{
    "name": "Sony Bravia",
    "brightness": [
        {
            "gte": 100,
            "lte": 300
        }
    ]
}
{% endhighlight %}

Here `gte` and `lte` stand for "greater than or equal to" and "less than or equal to". This signifies a range of 100 to 300 inclusive.

Now let's store another TV. This LG OLED has two modes. In the standard mode, its screen can go from 100 to 400 nits. But in the HDR mode, the screen can go from 500 to 1000 nits.

{% highlight JSON %}
PUT televisions_index/_doc/lg_oled
{
    "name": "LG OLED",
    "brightness": [
        {
            "gte": 100,
            "lte": 400
        },
        {
            "gte": 500,
            "lte": 1000
        }
    ]
}
{% endhighlight %}

Now let's make a simple query to our index. We want to get a list of TVs that support a brightness value of 700 nits.

{% highlight JSON %}
GET televisions_index/_search
{
    "query": {
        "term": {
            "brightness": {
                "value": 700
            }
        }
    }
}
{% endhighlight %}

This will return only the LG OLED TV in the result, since only that one supports a brightness value of 700 nits.

We can also query for a range of brightness values.

{% highlight JSON %}
GET televisions_index/_search
{
    "query": {
        "range": {
            "brightness": {
                "gte": 150,
                "lte": 250
            }
        }
    }
}
{% endhighlight %}

This will return both TVs in the result, since both of them support 150 to 250 nits of screen brightness.