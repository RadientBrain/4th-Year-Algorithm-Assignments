'''

Name: Chetan Maheshwari
Question 3::: Non Deterministic Sort

'''



import random 
from random import randint



def is_sorted(a): 
    n = len(a) 
    for i in range(0, n-1): 
        if (a[i] > a[i+1] ): 
            return False
    return True


def shuffle(a): 
    n = len(a) 
    for i in range (0,n): 
        r = random.randint(0,n-1) 
        a[i], a[r] = a[r], a[i] 
    #print("Permutations:",a)

def nonDetSort(a): 
    count = 0
    # n = len(a) 
    while (is_sorted(a)== False): 
        shuffle(a)
        count+=1
    print("Total Permutations:",count)
  

def random_points(n=30):
    coordinates = [ randint(0, n) for _ in range(n)]
    print (coordinates)
    return coordinates


if __name__ == "__main__":
    a = random_points(10)
    
    print("Original List:",a)
    nonDetSort(a) 
    print("Sorted array :", a)