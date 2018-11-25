# Average Stock #

A simple menu-driven program to display a given stock's average *if* you were to buy additional shares today and assists you in the creation and modification of stock_symbol files. 

## Requirements ##

* Command-line interface (Terminal) <br>
* [Python 3.x](https://www.python.org/downloads/)
  * Windows:  Processor's architecture: Right Click Start button (Windows logo) > System > System type: 32 or 64-bit?
    * Once you've downloaded Python 3.x, follow [these instructions](https://docs.python.org/3.7/using/windows.html) to make an executable for python.exe
  * { **Linux**, **Mac** } I recommend adding via your respective package managers: {<code>apt-get</code>, <code>brew</code>} <code>install python</code>
  * If you don't want to download python3 or find it too confusing, just use an [online compiler](https://realpython.com/installing-python/#online-python-interpreters)

## Usage ##

The python interpreter commnds are OS-dependent, but I will walk you through how to invoke in Windows, Linux, and Unix (Mac OS). <br>
Start by downloading this repo by clicking [here](https://github.com/Mas9311/stock-average/archive/v1.0.zip), then follow the steps below <br>

### Windows ###

1. Right click the stock-master-1.0 file in your Downloads folder, then select Extract All
1. Remove the *\stock-average-1.0* from the end of the default path, copy the path starting with C:\ as we will use this later, and extract the files.
1. Open the command prompt [Win + R] and type <code>py </code> then paste the path.

### *nix-based OS ###

0. Linux users should download the package <code>unzip</code> which can be downloaded with:<br>
   * <code>sudo apt-get install unzip</code> <br><br>
1. Open a command line window (Terminal) and type the following commands: <br>
1. <code>cd <local/path/ABOVE/stock-average-1.0.zip></code> <br>
1. <code>unzip stock-average-1.0.zip</code> <br>
1. <code>cd stock-average-1.0</code> <br>
1. <code>python3 stock_average.py</code>
   * Can have additional arguments of <stock_symbol> <current_price> such as:
     * <code>python3 stock_average.py btc</code>
     * <code>python3 stock_average.py btc 5190.85</code>

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
