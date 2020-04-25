#include <stdio.h>
 
void main()
{
    int num;
    int x = 0;
    int y = x*10;
    int z = y*20;
 
    printf("Enter a number: \n");
    scanf("%d", &num);
    if (num > 0)
        printf("%d is a positive number \n", num);
    else if (num < 0)
        printf("%d is a negative number \n", num);
    else
        printf("0 is neither positive nor negative");
}