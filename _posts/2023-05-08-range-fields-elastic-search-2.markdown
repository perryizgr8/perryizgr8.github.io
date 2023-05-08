---
layout: post
title:  "How to store ranges in Elasticsearch Part 2"
categories: elasticsearch
---
*Read part 1 of this series [here]({% post_url 2023-05-01-range-fields-elastic-search %}).*

Last time we saw how to use range fields to store range values in Elasticsearch. You could store two discontinuous brightness ranges supported by a TV operating in two modes (SDR and HDR). However, we did not associate the ranges with their respective modes.

To do that properly, we need to make use of nested types in Elasticsearch.

{% highlight JSON %}
PUT televisions_nested_index
{
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "brightness": {
                "type": "nested",
                "properties": {
                    "mode": {
                        "type": "text"
                    },
                    "value": {
                        "type": "integer_range"
                    }
                }
            }
        }
    }
}
{% endhighlight %}

Let's put in the same TVs as last time, but with the mode information attached.

{% highlight JSON %}
PUT televisions_nested_index/_doc/sony_bravia
{
    "name": "Sony Bravia",
    "brightness": [
        {
            "mode": "SDR",
            "value": {
                "gte": 100,
                "lte": 300
            }
        }
    ]
}

PUT televisions_nested_index/_doc/lg_oled
{
    "name": "LG OLED",
    "brightness": [
        {
            "mode": "SDR",
            "value": {
                "gte": 100,
                "lte": 400
            }
        },
        {
            "mode": "HDR",
            "value": {
                "gte": 500,
                "lte": 1000
            }
        }
    ]
}
{% endhighlight %}

Now we can query for a specific brightness range in a particular mode. So let's search for a TV that supports 600 to 700 nits in the HDR mode.

{% highlight JSON %}
GET televisions_nested_index/_search
{
    "query": {
        "bool": {
            "must": [
                "nested": {
                    "inner_hits": {},
                    "path": "brightness",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "brightness.mode": {
                                            "value": "HDR"
                                        }
                                    }
                                },
                                {
                                    "range": {
                                        "brightness.value": {
                                            "gte": 600,
                                            "lte": 700
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
    }
}
{% endhighlight %}

This will return the LG TV since it is the only one that supports our required brightness in the HDR mode.

*Thanks to the person who answered [my question on Stack Overflow](https://stackoverflow.com/questions/76167224/storing-and-searching-units-and-value-ranges-in-elasticsearch). It helped me make progress when I was completely stuck.*