#include<stdio.h>
int main()
{
    int count, first_term = 0, second_term = 1, next_term, i;
 
    //Ask user to input number of terms 
    printf("Enter the number of terms:\n");
    scanf("%d",&count);
 
    printf("First %d terms of Fibonacci series:\n",count);
    // for ( i = 0 ; i < count ; i++ )
    i = 0;
    while(i>count)
    {
       if ( i <= 1 )
          next_term = i;
       else
       {
          next_term = first_term + second_term;
          first_term = second_term;
          second_term = next_term;
       }
       printf("%d\n",next_term);
       i++;
    }
 
    return 0;
}