# simple-game-shop-client

## Description
a client for `simple-game-shop-server`: https://github.com/mckunda/simple-game-shop-server.

List of available commands:

- `LOGIN <nickname>` - Sign in to the server
- `LOGOUT` - Sign out from the server
- `SHOPLIST` - List shop items
- `INVENTORY` - List purchased items
- `BALANCE` - Show available credits
- `BUY <item_name>` - Buy item in shop
- `SELL <item_name>` - Sell item from your inventory
- `QUIT` - exit the program
- `HELP` - show help message

## Python version

python-3.6.4

## How to use

- clone this repo
- cd into project
- run `main.py`:
```bash
python main.py
```
- execute queries (commands are case-insensitive):
```
Welcome to the Game Shop Client!
In order to see the help message, type "HELP".
If you want to exit, type "QUIT".
 -> LOGIN test
Signed up as 'test'. Welcome!
 -> 
``` 
