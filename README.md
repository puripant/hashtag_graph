# Hashtag Graph

My take on [the coding challenge for Insight Data Engineering 2015](https://github.com/InsightDataScience/coding-challenge), 
cleaning tweets and creating a hashtag graph. I implemented in Python 3 just because I wanted to practice.
Any novice mistakes were due to the short time frame, not my inexperience with the language :)

## Cleaning Tweets

It was pretty straightforward. The only new trick I learned was:

    new_text = text.encode().decode("ascii", "ignore")

It basically turns a string `text` into bytes then turns it back to string while ignoring anything but ASCII 
and effectively removing unicodes.

## Hashtag Graph

Actually the task asked for the average degree so I did not have to count and used an observation that 
the summation of all degrees is twice of the number of edges. So the average degree can be simply calculated by:

    2*len(edges)/len(nodes)

To maintain the 60-second window, there are two pointers to an older and newer tweets 
and the repeated edges and nodes in the window need to be tracked.
The numbers of edges and nodes may increase when a new tweet is added.
Conversely, they may decrease when the first pointer increases (and removes old tweets outside the window).
If the counters reach zero, delete them out.

Nothing fancy here but it is hard to tell if it works correctly or not when there is no sample output to verify, 
but maybe that is the point of the challenge. 
I have got some feedbacks that it works well though.
