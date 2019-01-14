# Compute Your Potential Average #

[![image](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

A simple menu-driven program to display your potential averages *if* you were to buy additional shares or coins today.<br>
Note: the **symbols/** folder will be created to store each of your entries so you can reuse them later.

## Usage ##

1. [Download this repo](https://github.com/Mas9311/stock-average/archive/v1.1.zip), and open a Terminal window.<br>
1. <code>unzip</code> the <code>stock-average-1.1.zip</code> file from your downloads.<br>
1. <code>cd</code> into the <code>stock-average-1.1/</code> folder, where an <code>ls</code> would display <code>run.py</code><br>
  - To run the program, enter <code>python3 run.py</code><br>
  - If you want parameters, the first is the symbol followed by the optional current_price, such as:<br>
    * <code>python3 run.py btc</code>
    * <code>python3 run.py btc 3807.25</code>

## Methodology ##

Have you ever wanted to take the mean of N items, then wanted to see the impact for (N + 1) items?<br>
Thankfully, you don't need to re-enter the those items each time if you record the numerator and denominator.

 * i.e. Finding what you need to score on the final to reach a certain letter grade.<br>


###### Scenario: ######

 - You previously purchased some shares of a stock at a high price, and the price has dropped since then.
 - Because the stock is on sale, you are willing to spend some money today to lower your average.
 - You now need to quantify how many shares you would need to purchase at the current price.

This program will display your potential averages incrementally, so you can gauge for yourself.<br>
For cryptocurrencies, potential averages will be displayed in increments of square root of the amount allotted.<br>

#### Formula: ####

*n* represents the amount of shares you previously purchased at the *oldPrice*.<br>
*x* represents the amount of shares you would potentially need to buy at the *currentPrice*.

<pre>(n * oldPrice) + (x * currentPrice)
-----------------------------------
              (n + x)</pre>

For cryptocurrencies, *x* will account for purchasing a fraction of a coin.
