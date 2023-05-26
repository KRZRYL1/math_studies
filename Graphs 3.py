x = 0
y = 0 
m = 4
n = 3
i = 0
print("Początek = (0,0)")
print("Pojemności = (m,n)")
print("Goal state = (2,y)")

while x != 2 or y != 2:
    r = int(input("Wprowadź krok: "))
    if(r == 1):     # napełniamy pierwsze z wiader
      x = m
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 2):   # napełniamy drugie z wiader
      y = n
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 3):   # wylewamy wodę z pierwszego
      x = 0
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 4):   # wylewamy wodę z drugiego
      y = 0
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 5):   # dolewamy z pierwszego do drugiego
      t = n - y
      y = n
      x -= t
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 6):   # dolewamy z drugiego do pierwszego
      t = m - x
      x = m
      y -= t
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 7):   # przelewamy z pierwszego do drugiego
      y += x
      x = 0
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    elif(r == 8):   # przelewamy z drugiego do pierwszego
      x += y
      y = 0
      if x == 2 or y == 2:
        print('brawo, ',x,y)
        break
    print(x,y)

# przykład: 2826