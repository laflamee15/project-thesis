users = {
    "juan123": {
        "name": "juan dela hoya",
        "password": "juan12345",
        "balance": 10000
    }
}
username = input("Enter username: ")
input_password = input("Enter your password: ")
if username in users:
    if input_password == users[username]["password"]:
        user_balance = users[username]["balance"]
        print("You've succesfuly logged in!")
        
        while True:
            print('Welcome to our bank')
            print("1-View Balance")
            print("2-Deposit")
            print('3-Withdraw')
            print('4-Exit')
            choose = int(input("Select your option: "))

            if choose == 1:
                print(user_balance)
            elif choose == 2:
                amount = int(input("Enter amount to deposit: "))
                user_balance = user_balance + amount
                print(f"You've succesfully deposited {amount}, your new balance is: {user_balance}")
            elif choose == 3:
                amount = int(input("Enter amount to withdraw: "))
                user_balance = user_balance - amount
                print(f"Youve succesfully withdrawn {amount}, your new balance is {user_balance}")
            elif choose == 4:
                print("Thanks for choosing our bank")
                break
    else:
        print("Wrong password")
else:
    print("Incorrect username")