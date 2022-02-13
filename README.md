# CSSkinsFinder
CS:GO skins parser, which finds undervalued skins on side platform named BitSkins.com
## Features
You can easily find undervalued skins, that are able to be sold in steam for higher price later. Market volume, prices and comissions for each item are taken into account.\
You can setup your search request - change price range, minimum profit rate, save technical information for later processing.\
All results are saved to .csv file that can be used for later processing if necessary.\
Added protection from wrong input.\
You can find .exe file that is ready to use (with my accounts and API keys, there are no money on them, but you are able to see how everything works).
## Accounts required
Besides Steam account with purchased game and absence of Trade Ban, accounts and API keys on [BitSkins](https://bitskins.com/) and [Zenscrape](https://zenscrape.com/) are required.
### Why are these required
You need account and your own API key on BitSkins, simply because this will enable a possibility to find all skins with given parametres in their database. However, their database sometimes is not really precise with prices, and in some cases even getting an average price for last week or month is still far from real prices. Still, it lets to check volume of the market.\
As for Zenscape, we need to get prices information of chosen items directly from Steam, that seems to have protection from machine parsing as viewing all pages for your account can be blocked for some time. To avoid this, we need some kind of VPN, but the problem is requests can be done from 5 to 7 times from each IP. Zenscrape changes your IP for every request and has free version of 1000 requests, that should be enough for some time.
## How to use
To use this insert your API keys into code or simply use ready .exe file
