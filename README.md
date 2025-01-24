# BTC-Price-Bot

A bot that runs 24/7 and collects BTC price every minute from multiple exchanges.

Arbitrage bot idea:
- set up accounts on multiple exchanges with available liquidity in all accounts
- get prices (could be triangular arbitrage)
- check for arbitrage opportunities
- execute order
- find way to set order at specific price, can take less profits in exchange for less risk
- no order should be executed if it cannot be executed at the desired price
- order execute simultaneously on targeted exchanges (buy cheaper on one, sell on another)