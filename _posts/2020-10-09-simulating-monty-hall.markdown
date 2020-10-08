---
layout: post
title:  "Simulating the Monty Hall problem"
categories: python
---
The [Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem) is a well known probability puzzle which many people find counterintuitive. Personally, even though I now understand the basic maths involved, it still seems absurd. So I decided to simulate the situation.

## The problem
You are in a game show that has three closed doors. Behind one door is a car, and the other two have goats. Your goal is to win the car.

The host asks you to choose a door. Assume you picked door A. The host knows which door has the prize, so he opens one of the remaining doors B or C, that he knows has a goat.

Now he asks if you would like to switch your original choice.
Should you stick with your original door or switch to the other unopened door?

## The paradox
Mathematically, you should always switch. That will give you a ~67% chance of winning the car. Staying with the original door will give you only a ~33% chance.

To many people, including me, this feels quite weird. It is hard to accept this conclusion. My gut says the odds are 50-50. It should not matter if I switch or stay.

Some people try to convince themselves using computer simulations of the problem. You repeat the scenario a large number of times and look at how many times you would have won if you had switched your original choice of door.

So that is what I'm trying to do.

## Simulation
I wrote my simulation in a Python Jupyter notebook. It is quite handy for such demonstrations.

{% highlight python %}
import secrets

doors = [1, 2, 3]
staying_wins = 0
switching_wins = 0
{% endhighlight %}

The `secrets` python module provides cryptographically strong random random numbers. This is our best bet to get "true" random numbers in a deterministic machine like my laptop.

Then we have a list of three doors, and counters for keeping track of which choice would have won in each iteration.

{% highlight python %}
    # Car is behind one door, other two have goats
    car_door = secrets.choice(doors)
    
    # Contestant makes a random choice
    original_choice = secrets.choice(doors)
{% endhighlight %}

The `secrets.choice()` function returns a randomly chosen element from a list.

We first decide which door has the car behind it. Then we ask our virtual contestant to choose his door. These are independent decisions so it is true to the problem.

{% highlight python %}
    # Monty opens a door out of the other two which definitely does not have the car
    if car_door == original_choice:
        # can open any of the other 2 doors
        if car_door == 1:
            opened_door = secrets.choice([2, 3])
        elif car_door == 2:
            opened_door = secrets.choice([1, 3])
        else:
            opened_door = secrets.choice([1, 2])
    else:
        # must open the goat door
        if original_choice == 1:
            if car_door == 2:
                opened_door = 3
            else:
                opened_door = 2
        elif original_choice == 2:
            if car_door == 1:
                opened_door = 3
            else:
                opened_door = 1
        else:
            if car_door == 1:
                opened_door = 2
            else:
                opened_door = 1
{% endhighlight %}

This badly written snippet just decides which door Monty should open out of the remaining two doors not chosen by the contestant. The condition is that Monty knows beforehand the contents of each door and will only open a door with a goat behind it.

{% highlight python %}
    if original_choice == car_door:
        # Count a win for staying
        staying_wins += 1
    else:
        # Count win for switching
        switching_wins += 1
{% endhighlight %}

If staying would have won the car, we count it in `staying_wins`, otherwise we increment `switching_wins`. 

This is put inside a loop that runs a million times.

## Final results
Staying with the original door won 332,053 times, and switching won 667,947 times. That's a 66.79% win rate for switching.

We arrive at the conclusion we already knew from basic probability calculations, but I'm still uncomfortable about it.

## Code
You can look at the code in [my Jupyter notebook](https://github.com/perryizgr8/monty-hall/blob/main/monty-hall.ipynb). If you want, you can try running this for more number of iterations, and the win probability for switching your door should get closer and closer to the ideal 2/3.
