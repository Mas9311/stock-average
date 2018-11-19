# Average Stock #

- - -

A simple menu-driven program to display a stocks' average *if* you were to buy additional shares today. 
 * Assists you in the creation and modification of stock_symbol files

## Requirements ##

* A \*nix-based OS in order to use the command-line interface (Terminal) <br>
* [Python 3.x](https://www.python.org/downloads/), but I recommend adding via your package manager (brew, apt, etc) <br>

## Usage ##
0. *(optional)* Linux users should download the package <code>unzip</code> with:<br>
   *  <code>sudo apt-get install unzip</code> <br><br>
1. [Download](https://github.com/Mas9311/stock-average/archive/v1.0.zip) this repo then open a command line window (Terminal) <br>
1. <code>cd <local/path/ABOVE/stock-average-1.0.zip></code> <br>
1. <code>unzip stock-average-1.0.zip</code> <br>
1. <code>cd stock-average-1.0</code> <br>
1. <code>python3 stock_average.py</code>
   * Can have additional arguments of <stock_symbol> <current_price> such as:
     * python3 stock_average.py btc
     * python3 stock_average.py btc 5190.85

- - -

## Methodology ##

Have you ever wanted to take the mean of N items, then wanted to see the impact if you add another? (N + 1) <br>
 - Thankfully, there's no need to recompute if you have a running total of the numerator and denominator. <br>

### Shares ###

Shares are pretty simple to find the mean, since they are whole numbers. <br>
Here's a scenario: <br>
 - You previously purchased shares, the price has dropped since then, and you are willing to purchase additional shares today.
 - You had n stocks (at a higher price) and want to know what the average would be if you bought x additional stocks (at the current price).
 - (n * old) + (x * current) / (x + n)

### Crypto ###

Cryptocurrencies have been around for a while now, but it's never too late to think about alternaive investments. <br>
Crypto averaging is a little more challenging, as you don't need to purchased coins in increments of whole numbers. <br>
You have to add up the ratio (part/whole) for both the numerator and the denominator. <br>
 - Generally, it is the same formula as stated above, but we want to maintain a decimal-precision of 8.
