"""
This is sort.py. In this file I will be several sort functions (quicksort, mergesort, selection sort, and insertion sort), as well as writing a 'is sorted' function that
whether the list has been sorted, and whether it's even a list at all (and if it is a list of ints). I will also be using timsort (or just sort()) and I will be timing all
of these and comparing them. This all will be printed off to console as well as the timer (which will be taken before and after the sort function is called, so it doesn't
mess up the function timing). I wrote this code. 
"""

from random import seed, sample
from time import perf_counter
from recursioncounter import RecursionCounter

def is_sorted(lyst):
    """
    First checks if it's being given a list. Also checks if the list is entirely ints. If not, then it's not happy. Finally checks if the passed in list is sorted. Returns
    True if sorted, False if not, ValueError if it's not a list, or not entirely ints.
    """
    if isinstance(lyst, list):
        if all(isinstance(entry, int) for entry in lyst):
            if lyst == sorted(lyst):
                return True
            else:
                return False
        else:
            raise ValueError
    else:
        raise ValueError

def selection_sort(lyst):
    """
    Firstly, checks if it's being fed a list. If it isn't, this function raises a ValueError. Then does a selection sort on the passed in list, swapping them as it goes. 
    """
    if isinstance(lyst, list):
        i = 0
        while i< len(lyst)-1:
            min_index = i
            j = i + 1
            while j < len(lyst):
                if lyst[j]<lyst[min_index]:
                    min_index = j
                j+=1
            if min_index != i:
                lyst[i], lyst[min_index] = lyst[min_index], lyst[i]
            i+=1
        
        return lyst
    else:
        raise ValueError

def insertion_sort(lyst):
    """
    Checks to see if it's being fed a list. Raises a Value Error if not, then does a insertion_sort.
    """
    if isinstance(lyst, list):
        i=1
        while i<len(lyst):
            value = lyst[i]
            p = i-1
            while p >= 0 and value < lyst[p]:
                lyst[p+1] = lyst[p]
                p-=1
            lyst[p+1] = value
            i+=1
        return lyst
    else:
        raise ValueError

def merge(lyst, buffer, low, middle, high):
    """
    Helps out the mergesort_helper by merging through the two sublists that it's been fed. Returns a sorted list and uses the buffer array passed into it from mergesort_helper 
    (who got it from mergesort).
    """

    value1=low
    value2=middle

    for i in range(low, high+1):
        if value1>middle:
            buffer[i]=lyst[value2]
            value2+=1
        elif value2>high:
            buffer[i]=lyst[value1]
            value1+=1
        elif lyst[value1]<lyst[value2]:
            buffer[i]=lyst[value1]
            value1+=1
        else:
            buffer[i]=lyst[value2]
            value2+=1
    for i in range(low, high+1):
        lyst[i]=buffer[i]
    return lyst

def mergesort_helper(lyst, buffer, low, high):
    """
    Starts up by instantiating recursion counter, then finds the middle entry. It then passes it into itself, starting with the low half, then the high half. Then calls merge.
    """
    RecursionCounter()
    if low<high:
        middle = (low + high) // 2
        mergesort_helper(lyst, buffer, low, middle)
        mergesort_helper(lyst, buffer, middle+1,high)
        merge(lyst, buffer, low, middle, high)
    else:
        return lyst

def mergesort(lyst):
    """
    Checks if it's even being fed a list. Then revs up. Starts up a buffer (array) to temporarily hold numbers when merging. Calls mergesort_helper to start up the recursion passing in the list, the starting and ending range of 
    the list, and the buffer. 
    """
    if isinstance(lyst, list):
        buffer = [None] * len(lyst)
        lyst = mergesort_helper(lyst, buffer, 0, len(lyst)-1)
        return lyst
    else:
        raise ValueError

def find_me_the_middle(lyst, left, right):
    """
    Grabs the middle, swaps it over to the right and jumps through throwing things over if they are less than or more than the middle point. After sorting through all of them, it
    trades back the current boundary point with the middle that had been thrown over. Returns the boundary point.
    """
    middle = (left + right) // 2
    mid = lyst[middle]
    lyst[middle], lyst[right] = lyst[right], lyst[middle]

    boundary = left

    for i in range(left, right):
        if lyst[i]<mid:
            lyst[i], lyst[boundary] = lyst[boundary], lyst[i]
            boundary +=1
    lyst[right], lyst[boundary] = lyst[boundary], lyst[right]
    return boundary

def quicksort_helper(lyst, left, right):
    """
    Gets passed in a list, as well as it's left most and right most bounds. Passes off info to another function that finds the partition and splits them into higher and lower.
    Then recursively calls itself.
    """
    RecursionCounter()
    if left<right:
        pivotPoint =find_me_the_middle(lyst, left, right)
        quicksort_helper(lyst, left, pivotPoint-1)
        quicksort_helper(lyst, pivotPoint+1, right)
    return lyst

def quicksort(lyst):
    """
    Calls quicksort after making sure that it's been fed a list.
    """
    if isinstance(lyst, list):
        quicksort_helper(lyst, 0, len(lyst)-1)
        return lyst
    else:
        raise ValueError

def main():
    """
    Good ol' main. Gets the random list set up, passes in a copy while timing and printing everything off for my different sorts. This was a fun project!
    """
    seed(0)
    sample_size = 10000
    data = sample(range(sample_size), sample_size)

    print('Running selection sort:')
    s_s_start_time = perf_counter() 
    selection_sort(data.copy())
    s_s_runtime = perf_counter() - s_s_start_time
    print(f'Selection Sort runtime: {s_s_runtime:.5f}')

    print('Running insertion sort:')
    i_s_start_time = perf_counter()
    insertion_sort(data.copy())
    i_s_runtime = perf_counter() - i_s_start_time
    print(f'Insertion sort runtime: {i_s_runtime:.5f}')

    print('Running mergesort: ')
    m_start_time = perf_counter()
    mergesort(data.copy())
    m_runtime = perf_counter() - m_start_time
    print(f'Mergesort runtime: {m_runtime:.5f}')

    print('Running quicksort: ')
    q_start_time = perf_counter()
    quicksort(data.copy())
    q_runtime = perf_counter() - q_start_time
    print(f'Quicksort runtime: {q_runtime:.5f}')

    print('Running timsort: ')
    t_start_time = perf_counter()
    sorted(data.copy())
    t_runtime = perf_counter() - t_start_time
    print(f'Timsort runtime: {t_runtime:.5f} Wow, much fast!')

    
if __name__ == "__main__":
    main()