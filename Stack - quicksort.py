import random

class Empty(Exception):
    pass


class Stack:

    """Implementacja Stosu"""

    def __init__(self):
        self._data = []  # nowy pusty stos

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()

    def show_all(self):
        return self._data


def quicksort(array):

    """Wersja nierekurencyjna oraz in-place"""

    S = Stack()   # Stos stworzony w celu przechowywania indeksów początkowych i końcowych listy głównej oraz mniejszych
    S.push(0)
    S.push(len(array) - 1)

    while not S.is_empty():
        end = S.pop()         # końcowy indeks
        start = S.pop()       # początkowy indeks

        pivot_index = partition(array, start, end)

        if pivot_index - 1 > start:  # dopóki odległóść indeksów danego początku i końca względem danego pivota
            S.push(start)            # posortowane, otrzymamy indeksy sublisty do kolejnego sortowania
            S.push(pivot_index - 1)

        if pivot_index + 1 < end:
            S.push(pivot_index + 1)
            S.push(end)

    return array


def partition(array, start, end):   # start i end - pozwalają sprawdzić przedział wartości

    """Po kolei porównujemy każdy z elementów danej (sub)listy do ustalonego jako ostatni pivota.
        Iterujemy po indeksie 'j', jeśli dany element jest mniejszy od pivota, zwiększamy indeks 'i' o jeden.
        Nie następuje wtedy żadna zmiana bo i == j .
        Jeśli element natomiast jest większy, 'i' nie rośnie, tworząc róznicę w indeksach, która z kolei wpłynie na
        zamienianie się elementów array[i] oraz array[j].
        Im większa róznica (czyli ilość elementów większych od pivota), tym więcej elementów będzie "przesuwanych"
        (będą one gromadzić się obok siebie).
         Iterując do końca 'j' otrzymamy posegregowaną listę w sposób: mniejsze od pivota po lewej, większe po prawej"""

    pivot = array[end]            # ustalamy pivota (ostatni w liście)
    i = start - 1

    for j in range(start, end):
        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    array[i + 1], array[end] = array[end], array[i + 1]
    return i + 1


def visual_partition(array, start, end):  # start end są wartościami jakie wprowadzamy aby sprawdzić konkretny przedział
    pivot = array[end]
    print(f"Pivot: {pivot}")
    print(f"start: {start}, end: {end}")
    i = start - 1

    for j in range(start, end):
        # print((i,j))
        if array[j] < pivot:
            i += 1
            # print((i,j))
            array[i], array[j] = array[j], array[i]
            print(array)

    array[i + 1], array[end] = array[end], array[i + 1]
    print(array)
    print("Koniec partycji")
    return i + 1

lista = []

for i in range(0,1000):
    lista.append(random.randint(0,100))
print(quicksort(lista))

print(quicksort([0,2,20,3,4,5,0,1,10]))