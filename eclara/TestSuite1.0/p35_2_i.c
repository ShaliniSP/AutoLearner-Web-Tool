/* C Program to convert Lower case
 * String to Upper case.
 * Written by: Chaitanya
 */

#include<stdio.h>
#include<string.h>
int main(){
   char str[25];
   int i;

   printf("Enter the string:");
   scanf("%s",str);

   for(i=0;i<=strlen(str);i++){
      if(str[i]>='a'&&str[i]<='z')
         str[i]=str[i]-('a' - 'A');
   }
   printf("\nUpper Case String is: %s",str);
   return 0;
}