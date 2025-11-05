import math
nums = list(map(int, input("Enter numbers: ").split()))
pangalawa = list(set(nums))
pangalawa.sort(reverse = True)
if len(pangalawa) >= 2:
    highest = pangalawa[0]
    second_highest = pangalawa[1]
    print(f"Highest number: {highest}")
    print(f'Second highest number: {second_highest}')

    gcd_result = math.gcd(highest, second_highest)
    print(f"The highest number is {highest}, the second highest is {second_highest} the GCD is {gcd_result}")
