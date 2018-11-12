# Average Stock #

- - -

A menu-driven system to help you create, modify, and display your stocks' average if you were to buy additional shares today. <br>

## Requirements ##

* [Python 3.x](https://www.python.org/downloads/) <br>
* Linux or Unix based OS in the command-line interface <br>

## Usage ##

The following commands will download this repo then run with Python 3: <br>
 - Open a command line window (Terminal) <br>
<code> wget https://github.com/Mas9311/stock-average.git </code> <br>
<code> python3 stock-average.py </code>

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
The only hold up for crypto averaging is you don't need to purchased shares in increments of whole numbers. <br>
  - You purchased a fraction of a coin at a higher price and the price has lowered since then. 
  - You now want to find what you would be averaging if you spent additional money today and see if your avergage would be lowered.
    - It's the same formula as stated in the Shares section, but you want to keep the decimals with a precision of 8.
