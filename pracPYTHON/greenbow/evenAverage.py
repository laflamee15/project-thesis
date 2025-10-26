numbers = list(map(int, input("Enter number: ").split()))
evenNumbers = [num for num in numbers if num %2 == 0]
if evenNumbers:
    average = (sum(evenNumbers) / len(evenNumbers))
    print(f"Even numbers: {evenNumbers}")
    print(f"Average of even: {round(average, 2)}")
else:
    print("No even numbers")

