
print("Start gry\nTwoim zadaniem będzie przetransportowanie wszystkich na prawą stronę rzeki, uzwględniając reguły:")
print("1. łódź może wziąć maksymalnie dwie osoby naraz"
      "\n2. jeśli liczba kanibali będzie gdziekolwiek większa niż liczba misjonarzy, to kanibale zjedzą misjonarzy"
      "\n3. łódka nie może robić pustych kursów")


lM = 3  # lM = ilość misjonarzy z lewej
lC = 3  # lC = ilość kanibali z lewej
rM = 0  # rM = ilość misjonarzy z prawej
rC = 0  # rC = ilość kanibali z prawej
userM = 0  # userM = wartość podana przez użytkownika - ilość misjonarzy w podróży z prawej do lewej
userC = 0  # userC = analogicznie dla kanibali
k = 0
print("\nM M M C C C |	 --- | \n")
try:
    while (True):
        while (True):
            print("Z lewej do prawej")
            # uM = user input for number of missionaries for left to right travel
            # uC = user input for number of cannibals for left to right travel
            uM = int(input("Ilu misjonarzy płynie?"))
            uC = int(input("Ilu kanibali płynie?"))

            if ((uM == 0) and (uC == 0)):
                print("Nie można zrobić pustych kursów")
                print("wprowadź ponownie:")
            elif (((uM + uC) <= 2) and ((lM - uM) >= 0) and ((lC - uC) >= 0)):
                break
            else:
                print("złe wprowadzenie: ")
        lM = (lM - uM)
        lC = (lC - uC)
        rM += uM
        rC += uC

        print("\n")
        for i in range(0, lM):
            print("M ", end="")
        for i in range(0, lC):
            print("C ", end="")
        print("| --> | ", end="")
        for i in range(0, rM):
            print("M ", end="")
        for i in range(0, rC):
            print("C ", end="")
        print("\n")

        k += 1

        if (((lC == 3) and (lM == 1)) or ((lC == 3) and (lM == 2)) or ((lC == 2) and (lM == 1)) or (
                (rC == 3) and (rM == 1)) or ((rC == 3) and (rM == 2)) or ((rC == 2) and (rM == 1))):
            print("Kanibale zjadają misjonarzy :(\nGAME OVER X(")

            break

        if ((rM + rC) == 6):
            print("WIN : \n\t Brawo")
            print("Ilość prób")
            print(k)
            break
        while (True):
            print("Podróż z prawej do lewej")
            userM = int(input("Ilu misjonarzy płynie?  "))
            userC = int(input("Ilu kanibali płynie? "))

            if ((userM == 0) and (userC == 0)):
                print("Nie można zrobić pustego kursu")
                print("wprowadź ponownie: ")
            elif (((userM + userC) <= 2) and ((rM - userM) >= 0) and ((rC - userC) >= 0)):
                break
            else:
                print("złe wprowadzenie: ")
        lM += userM
        lC += userC
        rM -= userM
        rC -= userC

        k += 1
        print("\n")
        for i in range(0, lM):
            print("M ", end="")
        for i in range(0, lC):
            print("C ", end="")
        print("| <-- | ", end="")
        for i in range(0, rM):
            print("M ", end="")
        for i in range(0, rC):
            print("C ", end="")
        print("\n")

        if (((lC == 3) and (lM == 1)) or ((lC == 3) and (lM == 2)) or ((lC == 2) and (lM == 1)) or (
                (rC == 3) and (rM == 1)) or ((rC == 3) and (rM == 2)) or ((rC == 2) and (rM == 1))):
            print("Kanibale zjadają misjonarzy :(\n GAME OVER X(")
            break
except EOFError as e:
    print("\nZłe wprowadzenie, spróbuj ponownie")
