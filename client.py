from xmlrpc.client import ServerProxy
from datetime import datetime

proxy = ServerProxy('http://localhost:9000')

# Menu of options for users

def select():
    print(
        "Notebook Client\n"
        "Your options:\n"
        "1) Input data\n"
        "2) Read data by topic\n"
        "0) Exit"
    )

    selection = input("Your choice: ")
    return int(selection)

def main():
    while True:
        selection = select()

        if selection == 1:
            
            topic = input("Topic of your note: ")
            title = input("Title of your note: ")
            text = input("Your note: ")
            time = datetime.now()
            timestamp = time.strftime("%d/%m/%Y  %H:%M:%S")

            message = proxy.save(topic, title, text, timestamp)
            print(message)
        
        elif selection == 2:
            
            topic = input("Topic to get data from: ")
            data = proxy.read(topic)

            if data is False:
                print('There was an error reading the data or no data was found.\n')
            else:
                print("\n")
                for note in data:
                    print(note)
                    print("\n")
        
        elif selection == 0:
            print("Shutting down...")
            exit(0)
        
        else:
            print("ERROR! Exiting..")
            exit(0)

main()