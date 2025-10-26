
for i in range(1, 100):
    if i % 7 == 0:
        break
    print(i)

for i in range(1, 20):
    if i % 3 == 0:
        pass
    else:
        print(i)

for i in range(1, 10):
    if i == 5:
        pass
    else:
        print(i)

for i in range(1, 100):
    if i % 2 == 0:
        continue
    elif i > 50:
        break
    print(i)
