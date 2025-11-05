num = int(input("Enter a number: "))

if num <= 1:
    print("No prime factors")
else:
    i = 2
    print("Prime factors:", end=" ")
    while num > 1:
        if num % i == 0:
            print(i, end=" ")
            num //= i
        else:
            i += 1
