def count_even_odd():
    even = 0
    odd= 0
    while True:
        num = int(input("Enter number: "))
        if num == 0:
            break
        elif num < 0:
            raise ValueError("Number cannot be negative ")

        if num % 2 == 0:
            even +=1
        else:
            odd +=1
    print(f"Even numbers: {even}")
    print(f"Odd numbers: {odd}")

    
count_even_odd()