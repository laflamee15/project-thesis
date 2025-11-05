students = {"James": "12345", "Emman": "123456"}
username = input("Enter your username: ")
input_password = input("Enter your password: ")
if username in students:
    if input_password == students[username]:
        print("Youre in")
    else:
        print("wrong password")
else:
    print("Username does not exist")