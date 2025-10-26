def sum_of_digits(n):
    total = 0
    while n > 0:
        digit = n % 10
        total += digit
        n //= 10
    return total
num = int(input("Enter a number: "))
print(f"The total of the number is {sum_of_digits(num)}")

def get_average(grades):
    return sum(grades) / len(grades)
grades = []
for i in range(3):
    grade = float(input(f"Enter your grade {i + 1}: "))
    grades.append(grade)
average = get_average(grades)
print(f"The average is {average}")
