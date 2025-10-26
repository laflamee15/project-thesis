num = int(input("Enter a number: "))
binary = ""
while num > 0:
    binary = str(num % 2) + binary
    num //= 2
print("Binary:", binary)
