result = []
while True:
    num = input("Enter asfas: ")
    if num == 'done':
        break
    try:
        value = int(num)
        if value % 2 == 0:
            result.append(value)
    except ValueError:
        print("Invalid input")
average = sum(result) / len(result)
print(result)
print(average)