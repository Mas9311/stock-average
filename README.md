# Average Stock #

- - -

A menu-driven system to help you create, modify, and display your stocks' average if you were to buy additional shares today. <br>

## Requirements ##

* A \*nix-based OS in order to use the command-line interface (Terminal) <br>
* [Python 3.x](https://www.python.org/downloads/), but I recommend adding via your package manager (brew, apt, etc) <br>

## Usage ##
 - Linux users should download the package <code>unzip</code> with:<br>
 <code>sudo apt-get install unzip</code> <br><br>
 - [Download](https://github.com/Mas9311/stock-average/archive/master.zip) this repo then open a command line window (Terminal) <br>
 <code>cd <local/path/ABOVE/stock-average-master.zip></code> <br>
 <code>unzip stock-average-master.zip</code> <br>
 <code>cd stock-average-master</code> <br>
 <code>python3 stock_average.py</code>

- - -

## Methodology ##

Have you ever wanted to take the mean of N items, then wanted to see the impact if you add another? (N + 1) <br>
 - Thankfully, there's no need to recompute if you have a running total of the numerator and denominator. <br>

### Shares ###

Shares are pretty simple to find the mean, since they are whole numbers. Here's a scenario:<br>
 - Since you purchased the shares, the price has gone down.
 - You have n stocks at a higher price and want to see what you'd be averaging if you bought x more stocks at the current price.
 - (n * old) + (x * current) / (x + n)

### Crypto ###

Cryptocurrencies have been around for a while now, but it's never too late to think about alternaive investments. <br>
Crypto averaging is a little more challenging, as you don't need to purchased coins in increments of whole numbers. <br>
Here's the scenario: <br>
  - You purchased a fraction of a coin at a higher price and the price has lowered since then. 
  - You now want to find what you would be averaging if you spent additional money today in order to see if your average would be lowered.
    - It's the same formula as stated in the Shares section, but we want to maintain a decimal-precision of 8.
