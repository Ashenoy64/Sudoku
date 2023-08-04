#include<iostream>


using namespace std;

void print(int (*ar)[9])
{
    for(int i=0;i<9;i++)
    {   cout<<"|";
        for(int j=0;j<9;j++)
        {
            cout<<ar[i][j]<<" ";
            if((j+1)%3==0)
            {
                cout<<"|";
            } 
           
        }
         cout<<endl;
         if((i+1)%3==0){
            cout<<endl;
         }
    }
}

bool safe(int ar[9][9],int row,int col,int ele)
{
    for(int i=0;i<9;i++)
    {
        if(ar[row][i]==ele){
            return false;
        }
    }
    for(int i=0;i<9;i++){
        if(ar[i][col]==ele){
            return false;
        }
    }
    int a=row-row%3;
    int b=col-col%3;
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            if(ar[i+a][j+b]==ele)
            return false;
        }
    }
    return true;
}

//solves the grid using backtracking
bool solve(int (*ar)[9],int row,int col)
{
    if(row==8 && col==9){
        return true;
    }
    if(col==9){
        col=0;
        row++;
    }
    if (ar[row][col]>0)
    {
        return solve(ar,row,col+1);
    }
   for(int i=1;i<10;i++)
   {
    if(safe(ar,row,col,i))
    {
        ar[row][col]=i;
        if(solve(ar,row,col+1))
        
            return true;
    }
    ar[row][col]=0;  
}
 return false;
}

int random(int a,int b)
{
    return a+(rand()%(b-a+1));
}

void generate(int arr[9][9])//put some random numbers on the grid and solves the grid
{
  int row1,row2,row3;
  int col1,col2,col3;
  do{
        row1=random(0,2);
        row2=random(3,5);
        row3=random(6,8);

        col1=random(0,2);
        col2=random(3,5);
        col3=random(6,8);
        arr[row1][col1]=random(1,9);
        arr[row2][col2]=random(1,9);
        arr[row3][col3]=random(1,9);
        
  }while(!solve(arr,0,0));
}
void remove(int *p,int a[])
{
    int n=random(0,9);
    for(int i=1;i<a[0];i++){
        if(n==a[i])
        {
            *p=0;
            break;
        }    
    }
}

//removes numbers from solved grid depending on diff, diff={1,2,any} any being hardest
void generate_solvable(int arr[9][9],int diff)
{   int a[8];
    if(diff==1)
    {
       a[0]=4,a[1]=1,a[2]=5,a[3]=9;
    }
    else if(diff==2)
    {    
        a[0]=6,a[1]=1,a[2]=5,a[3]=9,a[4]=3,a[5]=7;
    }
    else{
        a[0]=6,a[1]=1,a[2]=5,a[3]=9,a[4]=3,a[5]=7,a[6]=0,a[7]=2;
    }
    for(int i=0;i<9;i++)
    {
        for(int j=0;j<9;j++)
        {
           remove(&arr[i][j],a);
        }
    }
}

int main()
{
    int arr[9][9]={0};
    generate(arr);
    print(arr);
    generate_solvable(arr,2);
    cout<<endl;
    print(arr);
    solve(arr,0,0);
    cout<<endl;
    print(arr);
    
}