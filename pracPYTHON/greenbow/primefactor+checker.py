num = int(input("Enter a number: "))

# Check if the number is prime
if num <= 1:
    print("Not a prime number (no prime factors)")
else:
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break

    if is_prime:
        print(f"{num} is a Prime number.")
    else:
        print(f"{num} is NOT a Prime number.")
        print("Prime factors:", end=" ")

        # Prime factorization part
        i = 2
        n = num  # copy original number for factorization
        while n > 1:
            if n % i == 0:
                print(i, end=" ")
                n //= i
            else:
                i += 1
