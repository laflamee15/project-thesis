num = int(input("Enter number: "))
result = 0
while num > 0:
    digit = num % 10 
    result = result * 10 + digit
    num //= 10
print(f"The reversed output is: {result}")

num = int(input("Enter number: "))
result = 0
while num > 0:
    add = num % 10
    result += add
    num //= 10
print(result)


num = int(input("Enter number: "))
prod = 1
while num > 0:
    nibba = num % 10 
    prod *= nibba
    num //= 10
print(prod)


num = int(input("Enter 5 number: "))
odd = 0
even = 0
while num > 0:
    digit = num % 10
    if digit % 2 == 0:
        even += 1
    else:
        odd += 1
    num //= 10
print(f"Even: {even}")
print(f"Odd: {odd}") 


word = input("Enter a word: ")
reverse = ""
for character in word:
    reverse = character + reverse
if word == reverse:
        print("Yes")
else: 
        print("No")

num = int(input("Enter a number: "))
step = 0
while num != 1:
    if num % 2 == 0:
        num /= 2
        step += 1
    else:
        num = (num * 3) + 1
        step += 1
print(step)

num = int(input("Enter 5 number: "))
result = 1
while num > 0:
    digit = num % 10
    result += digit
    num //= 10
print(result)

num = int(input("Enter number: "))
highest = 0
while num > 0:
    digit = num % 10
    if digit > highest:
        highest = digit
        num //= 10
        print(highest)
