#include<stdio.h>
int main()
{
   int num1,num2,num3;
   
   //Ask user to input any three integer numbers

   //Store input values in variables for comparsion
   scanf("%d %d %d",&num1,&num2,&num3);

   if((num1>num2)){
      if(num1 > num3)
         return 1;
      else
         return 2;
   }
   else {
      if(num2 > num3)
         return 2;
      else
         return 3;
}
   return 0;
}