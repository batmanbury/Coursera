# countSplitInversions.py
# Coursera -- Design and Analysis of Algorithms, Part I
# Matthew T. Banbury
# matbanbury (at) gmail

"""
This file contains all of the 100,000 integers between 1 and
100,000 (inclusive) in some order, with no integer repeated.

Your task is to compute the number of inversions in the file
given, where the ith row of the file indicates the ith entry
of an array.

Because of the large size of this array, you should implement
the fast divide-and-conquer algorithm covered in the video
lectures.
"""
import operator
import time

FILENAME = 'IntegerArray.txt'


def loadArray(filename):
    array = []
    with open(filename, 'r') as f:
        for n in f.readlines():
            array.append(int(n))
    f.close()
    return array


def merge(left, right, compare):
    """
    Returns a tuple of a sorted array (of the merged subarrays left, right)
    and the number of split inversions from the original and sorted lists

    Source: edX.org MIT 6.00.1x, lecture 9-4
    Modified to incorporate split count
    """
    result = []
    i,j = 0, 0
    splits = 0
    lenLeft = len(left)
    lenRight = len(right)
    while i < lenLeft and j < lenRight:
        if compare(left[i], right[j]):
#            tic = time.clock()
            result.append(left[i])
            i += 1
#            toc = time.clock()
#            print 'APPEND LEFT', toc-tic
        else:
#            tic = time.clock()
            result.append(right[j])
            j += 1
            splits += lenLeft - i
#            toc = time.clock()
#            print 'APPEND W/SPLIT', toc-tic
    while (i < lenLeft):
#        tic = time.clock()
        result.append(left[i])
        i += 1
#        toc = time.clock()
#        print 'remaining LEFT', toc-tic
    while (j < lenRight):
#        tic = time.clock()
        result.append(right[j])
        j += 1
#        toc = time.clock()
#        print 'remaining RIGHT', toc-tic
    return result, splits


def mergeSort(L, compare=operator.lt):
    """
    Returns a tuple of the array L, sorted, and the split inversion count
    Source: edX.org MIT 6.00.1x, lecture 9-4
    Modified to incorporate split count
    """
    if len(L) < 2:
        return L, 0
    middle = int(len(L)/2)
    left, a = mergeSort(L[:middle], compare)
    right, b = mergeSort(L[middle:], compare)
    result, c = merge(left, right, compare)
    splits = a + b + c
    return result, splits


if __name__ == "__main__":

    # # TEST CASE - 0
    # ANS = 0
    # array0 = [1,2,3,4,5,6]
    # sortedArray, splits = mergeSort(array0)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # TEST CASE - 1
    # ANS = 3
    # array1 = [1,3,5,2,4,6]
    # sortedArray, splits = mergeSort(array1)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # TEST CASE - 2
    # ANS = 4
    # array2 = [1,5,3,2,4]
    # sortedArray, splits = mergeSort(array2)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # TEST CASE - 3
    # ANS = 10
    # array3 = [5,4,3,2,1]
    # sortedArray, splits = mergeSort(array3)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # TEST CASE - 4 
    # ANS = 5
    # array4 = [1,6,3,2,4,5]
    # sortedArray, splits = mergeSort(array4)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # Test Case - 5
    # ANS = 56
    # array5 = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0]
    # sortedArray, splits = mergeSort(array5)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # Test Case - 6
    # ANS = 590
    # array6 = [37, 7, 2, 14, 35, 47, 10, 24, 44, 17, 34, 11, 16, 48, 1, 39, 6, 33, 43, 26, 40, 4, 28, 5, 38, 41, 42, 12, 13, 21, 29, 18, 3, 19, 0, 32, 46, 27, 31, 25, 15, 36, 20, 8, 9, 49, 22, 23, 30, 45]
    # sortedArray, splits = mergeSort(array6)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    # # Test Case - 7
    # ANS = 2372
    # array7 = [4, 80, 70, 23, 9, 60, 68, 27, 66, 78, 12, 40, 52, 53, 44, 8, 49, 28, 18, 46, 21, 39, 51, 7, 87, 99, 69, 62, 84, 6, 79, 67, 14, 98, 83, 0, 96, 5, 82, 10, 26, 48, 3, 2, 15, 92, 11, 55, 63, 97, 43, 45, 81, 42, 95, 20, 25, 74, 24, 72, 91, 35, 86, 19, 75, 58, 71, 47, 76, 59, 64, 93, 17, 50, 56, 94, 90, 89, 32, 37, 34, 65, 1, 73, 41, 36, 57, 77, 30, 22, 13, 29, 38, 16, 88, 61, 31, 85, 33, 54]
    # sortedArray, splits = mergeSort(array7)
    # print splits
    # print 'Correct?', ANS == splits, '\n'

    print "Original array load time (CLOCK):"
    tic = time.clock()
    array = loadArray(FILENAME)
    toc = time.clock()
    print toc - tic, '\n'

    print "Sort time (CLOCK):"
    tic = time.clock()
    sortedArray, splits = mergeSort(array)
    toc = time.clock()
    print toc - tic, '\n'

    print 'Original array:  ', array[:10], '...'
    del array
    print 'Sorted array:    ', sortedArray[:20], '...', '\n'
    print 'Number of split inversions: ', splits
    del sortedArray
    print 'Correct?', splits == 2407905288