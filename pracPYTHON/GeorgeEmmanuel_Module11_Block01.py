#1.Christmas Tree
num = 5
layers = 3
for h in range(layers):
    for i in range(num):
        for j in range(num - i - 1):
            print(" ", end="")
        for k in range(2 * i + 1):
            print("*", end="")
        print()
for l in range(3):
        print(" " * (((2 * num - 1) - 3) // 2) + "|||")

#2.Multiplication Table
for i in range(1, 11):
    for j in range(1, 11):
        print(i * j, end="\t")
    print()

#3.Number Diamond
n = 5
for i in range(1, 5 + 1):
     print(" " * (n-i), end="")
     for j in range(1, i+1):
          print(j, end="")
     for j in range(i- 1, 0, -1):
          print(j, end="")
     print()

for i in range(n-1, 0, -1):
     print(" " * (n-i), end="")
     for j in range(1, i +1):
          print(j, end="")
     for j in range(i-1, 0, -1):
          print(j, end="")
     print()
     
'''
"How do nested loops make these patterns possible compared to singled loops?
Nested loops make these patterns possible, because they let us repeat actions inside each row (like printing spaces, numbers, or *), while a single loop would only allow a straight sequence without proper alignment or shape.
'''