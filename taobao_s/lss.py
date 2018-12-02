import time
list = []
for i in range(1,101):
    list.append(i)
while len(list) > 1:
    for i in reversed(range(len(list))):
        if (i+1) % 2 != 0:
            lis = list[i]
            list.remove(lis)

print(list)