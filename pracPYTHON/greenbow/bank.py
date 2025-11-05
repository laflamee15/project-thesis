balance = 0
while True:
    print("1-Show balance")
    print("2-Deposit")
    print("3-Withdraw")
    print("4-Exit")
    choice = int(input("Enter your choice(1-4): "))
    if choice == 1:
        print(balance)
    elif choice == 2:
        amount = int(input("Enter amount to deposit: "))
        if amount > 0:
            balance += amount
            print(f"You've deposited {amount}. Your new balance is {balance}")
        else:
            print("Insufficient amount")
    elif choice == 3:
        amount = int(input("Enter amount to withdraw: "))
        if amount > balance:
            print("Not enough balance")
        elif amount > 0:
            balance -= amount
            print(f"You've withdrawed {amount}. Your new balance is {balance}")
        else: 
            print("Insufficent amount")
    elif choice == 4:
        print("Thank you")
        break