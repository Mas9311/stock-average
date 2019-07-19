# Compute Your Potential Average #

[![image](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

Program to display your potential averages *if* you were to buy additional shares or coins today.<br>
Note: the **symbols/** folder will be created to store each of your entries so you can reuse them later.

## Usage ##

#### Select your Operating System for information on downloading and running:

<details><summary>Linux / Unix</summary>
  1. Open a Terminal window and paste: <code>git clone https://github.com/Mas9311/stock-average.git</code><br>
  2. <code>cd stock-average/</code><br>
  3. Run the program: <code>python3 run.py</code><br>
  Append the <code>-h</code> | <code>--help</code> argument to view all accepted arguments.<br>
</details>
<details><summary>Windows</summary>
  1. Open a Terminal window and paste: <code>git clone https://github.com/Mas9311/stock-average.git</code><br>
  2. <code>cd stock-average/</code><br>
  3. Run the program: <code>python.exe run.py</code><br>
  Append the <code>-h</code> | <code>--help</code> argument to view all accepted arguments.<br>
</details>

## Methodology ##

Have you ever wanted to take the mean of N items, then wanted to see the impact for (N + 1) items?<br>

 - i.e. Finding what you need to score on the final exam to attain a desired letter grade.
 
Thankfully, you don't need to re-enter those items every time if you record the numerator and denominator beforehand.<br>


## Scenario:

 - You previously purchased some shares of a stock at a high price, and the price has dropped since then.
 - Because the stock is "on sale", you are willing to spend some money today to help lower your current average.
 - You now need to quantify how many shares you would need to purchase at the current price.

This program will display your potential averages incrementally, so you can gauge for yourself.<br>

 - Command Line Interface will print a wall of text.
 - Graphical User Interface has an option to display as a T-Chart or a Graph.

#### Formula: ####


*n* represents the amount of shares you previously purchased at the *oldPrice*.<br>
*x* represents the amount of shares you would potentially need to buy at the *currentPrice*.

<pre>(n * oldPrice) + (x * currentPrice)
-----------------------------------
              (n + x)</pre>
