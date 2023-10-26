print(type(42.0))
x = 2.5e6
print(x)
for i in range(1, 5): 
    print(i, "multiplicado por 8 =", i * 8)
    

games = []

while True:
    a = input()
    if a == "":
        break
    else:
        games.append(a)
print(games)

