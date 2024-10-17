command = ""
started = False
while True:
    command = input("> ").lower()
    if command == "start":
        if started:
            print("Car already started")
        else:
            started = True
            print("Car started")
    elif command == "stop":
        if not started:
            print("Car already stopped")
        else:
            started = False
            print("Car stopped")
    elif command == "help":
        print("""
    Available commands:
    start - starts the car
    stop - stops the car
    exit - exit the car
        """)
    elif command == "exit":
        print("You have exited the car")
        break
    else:
        print("Invalid command")