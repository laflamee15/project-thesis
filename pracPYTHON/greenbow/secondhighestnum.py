nums = list(map(int, input("Enter number: ").split()))
tolongges = list(set(nums))
tolongges.sort(reverse = True)
if len(tolongges) < 2:
    print("All are the same")
else:
    print(f"{tolongges[1]}")
