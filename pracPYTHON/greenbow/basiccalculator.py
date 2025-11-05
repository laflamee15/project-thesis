num1, num2 = map(int, input("Enter two integers: ").split())
print("Choose the operation to perform")
print("1-ADDITION")
print("2-SUBTRACTION")
print("3-MULTIPLICATION")
print("4-DIVISION")
choose = int(input())
if choose == 1:
    add = num1 + num2
    print(add)
elif choose == 2:
    sub = num1 - num2 
    print(sub)
elif choose == 3:
    multi = num1 * num2
    print(multi)
elif choose == 4:
    if num2 != 0: 
        print(num1 / num2)
    else:
        print("Invalid")
else:
    print("Invalid choice") 