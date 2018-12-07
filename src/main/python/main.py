from client import GameShopClient

if __name__ == '__main__':
    client = GameShopClient()

    print("Welcome to the Game Shop Client!\n"
          "In order to see the help message, type \"HELP\".\n"
          "If you want to exit, type \"QUIT\".")
    message = input(' -> ')

    while True:
        if message.upper() == 'QUIT':
            if client.session_active:
                client.query('LOGOUT')
            print('Goodbye!')
            break
        client.query(message)
        message = input(' -> ')
