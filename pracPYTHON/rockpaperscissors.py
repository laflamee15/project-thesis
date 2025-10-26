import random
print("Choices: 0-Exit, 1-Bato, 2-Papel, 3-Gunting")
choices = {1: "Bato", 2: "Papel", 3:"Gunting"}
while True:
    userMove = int(input("Enter your move(0-3): "))
    if userMove == 0:
        print("Thanks for playing!")
        break
    pcMove = random.randint(1, 3)
    print("Your move", choices[userMove])
    print("PC's move: ", choices[pcMove])
    if userMove == pcMove:
        print("Tie")
    elif (userMove == 1 and pcMove == 3) or (userMove == 2 and pcMove == 1) or (userMove == 3 and pcMove == 2):
        print("PANALO KA DOL")
    else:
        print("Olats")
    print()
    