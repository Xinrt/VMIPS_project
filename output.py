with open('fc.txt', 'w') as f:
    for i in range(257):
        for j in range(1, 257):
            f.write(str(j) + '\n')