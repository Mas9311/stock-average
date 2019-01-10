# Stock Average #

A simple menu-driven program to display your potential averages *if* you were to buy additional shares or coins today.<br>
\* This program creates a *symbols* folder and store each of your stock or coin entries for reuse! \*

### Requirements ###

  * A command-line interface (Linux and Mac comes with Terminal by default)
  * [Python 3.x](https://www.python.org/downloads/)

## Usage ##

1. [Download this repo](https://github.com/Mas9311/stock-average/archive/v1.0.zip), and open a Terminal window<br>
1. unzip the new <code>stock-average-1.0.zip</code> folder<br>
1. <code>cd stock-average-1.0</code><br>
1. <code>python3 run.py</code>
     * python3 run.py btc
     * python3 run.py btc 3807.25

## Methodology ##

 * Have you ever wanted to take the mean of N items, then wanted to see the impact for (N + 1) items?<br>
 * i.e. Finding what you need to score on the final to reach a certain letter grade.<br>
 * Thankfully, you don't need to re-enter the those items each time if you record the numerator and denominator.

###### Scenario: ######

 - You previously purchased some shares of a stock at a high price, and the price has dropped since then.
 - You are willing to spend some money today, because it is on sale.
 - You now need to quantify how many shares you would need to purchase at the current price to lower your average.

This program will incrementally display each of your potential averages, so you can gauge for yourself.

##### Formula: #####

Shares are pretty simple to find the mean, since they can only be purchased in increments of whole numbers.

<pre>(n * oldPrice) + (x * currentPrice)
----------------------------------------------
                       (n + x)</pre>

 - For cryptocurrencies, a modified version will be provided to account for purchasing a fraction of a coin.
