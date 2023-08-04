from numpy import array
from random import randint as random

def safe(l,row,col,ele):
    for i in range(9):
        if l[row,i]==ele:
            return False
        if l[i,col]==ele:
            return False
    
    a=row-row%3
    b=col-col%3
    for i in range(3):
        for j in range(3):
            if l[i+a,j+b]==ele:
                return False

    return True

#Solves the grid using backtracking 
def solve(ar,row,col):
    if row==8 and col==9:
        return True
    if col==9:
        col=0
        row+=1

    if ar[row,col]>0:
        return solve(ar,row,col+1)
    
    for i in range(1,10):
        if safe(ar,row,col,i):
            ar[row,col]=i
            if solve(ar,row,col+1):
                return True
        ar[row,col]=0

    return False


#generates a completed grid by putting some random number on the grid
def generate(arr):
    while True:
        row1=random(0,2);
        row2=random(3,5);
        row3=random(6,8);

        col1=random(0,2);
        col2=random(3,5);
        col3=random(6,8);
        arr[row1,col1]=random(1,9);
        arr[row2,col2]=random(1,9);
        arr[row3,col3]=random(1,9);
        if solve(arr,0,0):
            break


#removes numbers from solved grid to generate solvable grid based on dif
def generate_solvable(arr,diff):
    if diff==1:
        diff=5
    elif diff==2:
        diff=3
    else:
        diff=2
    for i in range(9):
        for j in range(9):
            a=random(1,100)
            if a%diff==0:
                arr[i,j]=0

def multiple_sol(arr):
    for i in range(9):
        for j in range(9):
            if arr[i,j]==0:
                break
    sol=[]
    for k in range(9):
        if safe(arr,i,j,k):
            sol.append(k)

    


l2=array([[0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]])



if __name__=="__main__":
    l=array([[0,1,0,0,8,6,0,7,4],
    [0,0,4,0,0,7,0,0,0],
    [0,0,6,0,0,0,8,0,0],
    [9,0,0,0,4,0,0,5,0],
    [0,4,0,2,0,5,0,8,0],
    [0,8,0,0,3,0,0,0,1],
    [0,0,8,0,0,0,1,0,0],
    [0,0,0,8,0,0,7,0,0],
    [3,7,0,1,9,0,0,4,0]])
    #solve(l,0,0)
    l2=array([[0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]])
    generate(l2)
    generate_solvable(l2,2)
    print(l2)