# stock-checker

Watching an item online but now it's out of stock? This python program can be used to scrape the webpage of the item you want to buy, check for stock availability, and send you a telegram push notification when the item goes back in stock (say if someone makes a return, or more stock becomes available – you'll be the first to know!). 

How it works:
This Python script automates the process of checking the stock availability of a specific item on a webpage (this part requires you to know some html/CSS. You need to know which element youre looking for, for the item you're trying to buy). It uses Selenium to simulate browser interactions, identifies stock status based on specific elements on the webpage, and sends a Telegram notification if the item is in stock. The code and comments should be fairly self explanatory, the part that requires changing for the item you want to buy is the 'check_stock():' function. The code is currently set up to click a specific item size button, look for an out of stock message, and use that to either load the page and check again (after some given time interval that you can set) if the item is out of stock, or send a Telegram notification if the item is in stock.

Requirements:
Chrome and ChromeDriver (make sure they're both the same version, can download from https://googlechromelabs.github.io/chrome-for-testing/)
Selenium (use pip install – 'pip install selenium' in bash on Mac/Linux)
Telegram bot for stock notifications (you can create a Telegram bot using BotFather, obtain the bot token, obtain chat ID by messaging the bot or using an API like getUpdates)

Tips for finding the right webpage element:
Use your browser's developer tools (e.g. right-click on element > Inspect) to locate the elements corresponding to:
- The size or option button you want to select.
- The text or element indicating stock status (e.g. "Out of stock").
- Update the CSS_SELECTOR values in the script with these specific elements.

Happy shopping!


