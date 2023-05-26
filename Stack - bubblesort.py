import random
from matplotlib import pyplot as plt, animation
import sys
import time
from PIL import ImageSequence
from PIL import Image
import gifmaker

def swap(A, i, j):
    """Metoda dla sortowania bąbelkowego - zamiana dwóch wyrazów w liście"""
    A[i],A[j]=A[j],A[i]

def bubblesort(A):

    """Ustawiamy swapped jako True. Wchodzimy do pętli, pierwszy
    warunek zapewnia przechodzenie po kolejnych elementach - ustawiamy
    swapped jako false i przechodzimy do porównania elementów do zamiany"""

    swapped = True

    for i in range(len(A)-1):
        if not swapped:
            pass
        swapped = False

        for j in range(len(A)-1-i):
            if A[j] > A[j+1]:
                swap(A,j,j+1)
                swapped = True
            yield A

    for k in range(len(A)-1):  # metoda zatrzymująca algorytm, po krótkim czasie automatycznie wyłącza program
        if A[k] < A[k+1]:      # sprawdza, czy sortowanie zostało już ukończone (trywialne, ale służy do zatrzymania programu)
            time.sleep(3)
            sys.exit()

def visualize():

    """Metoda do tworzenia animacji"""

    N = 20                      # liczba elementów do sortowania
    A = list(range(1,N+1))      # lista elementów od 1 do N
    random.shuffle(A)           # mieszamy elementy A

    generator = bubblesort(A)

    fig,ax = plt.subplots()
    ax.set_title("Bubble Sort O(n\N{SUPERSCRIPT TWO})") #tytuł, złożoność
    bar_sub = ax.bar(range(len(A)),A,align='edge')

    ax.set_xlim(0,N)
    text = ax.text(0.01,0.95,'',transform=ax.transAxes)
    iteration = [0]

    def update(A,rects,iteration):
        for rect,val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"amount of operations: {iteration[0]}") #zliczanie wykonanych operacji

    anim = animation.FuncAnimation(     # tworzenie animacji
        fig,
        func=update,
        fargs=(bar_sub,iteration),
        frames=generator,
        repeat=True,
        blit=False,
        interval=100,
        save_count=9000,
        )

    anim.save('animacja.gif')
    plt.show()
    plt.close()

if __name__ == "__main__":
    visualize()

