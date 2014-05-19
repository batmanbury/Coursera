# quicksort.py
# Coursera | Stanford | Algorithms: Design and Analysis, Part I
# Implementations of quicksort using different pivot elements, each
# counting the number of comparisons made before completing the sort.


comparisons_1 = 0
comparisons_2 = 0
comparisons_3 = 0


def quicksort1(array):
    """Pivot element: first"""
    global comparisons_1
    if array == []:
        return []
    else:
        pivot = array[0]
        lesser = quicksort1([n for n in array[1:] if n < pivot])
        greater = quicksort1([n for n in array[1:] if n > pivot])
        comparisons_1 += len(lesser)
        comparisons_1 += len(greater)
        return lesser + [pivot] + greater


def quicksort2(array):
    """Pivot element: last"""
    global comparisons_2
    if array == []:
        return []
    else:
        pivot = array[-1]
        lesser = quicksort2([n for n in array[:-1] if n < pivot])
        greater = quicksort2([n for n in array[:-1] if n > pivot])
        comparisons_2 += len(lesser)
        comparisons_2 += len(greater)
        return lesser + [pivot] + greater


def quicksort3(array):
    """Pivot element: median-of-three"""
    from numpy import median
    global comparisons_3
    if array == []:
        return []
    else:
        L = len(array)
        mI = (L/2 - 1) + L % 2  #middle index
        mid = array[mI]
        first, last = array[0], array[-1]  #first value, last value
        median = int(median([first, mid, last]))  #median value
        pivot = median
        less = []
        more = []
        for i in array:
            if i < pivot:
                less.append(i)
            if i > pivot:
                more.append(i)
        less = quicksort3(less)
        more = quicksort3(more)
        comparisons_3 += len(less)
        comparisons_3 += len(more)
        return less + [pivot] + more


if __name__ == "__main__":
    with open('1000.txt', 'r') as FILE:
        array = [int(n.strip()) for n in FILE.readlines()]
        a1 = quicksort1(array)
        assert a1 == sorted(array)
        print 'Quicksort 1 comparisons: ', comparisons_1
        a2 = quicksort2(array)
        assert a2 == sorted(array)
        print 'Quicksort 2 comparisons: ', comparisons_2
        a3 = quicksort3(array)
        assert a3 == sorted(array)
        print 'Quicksort 3 comparisons: ', comparisons_3