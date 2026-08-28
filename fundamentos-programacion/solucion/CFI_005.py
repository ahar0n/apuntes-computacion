cuenta = 0
for i in range(1,51,1):
    if (i % 3 == 0) or (i % 5 == 0):
        continue

    print(i)
    cuenta += 1

print(f"Fueron mostrados {cuenta} numeros.")