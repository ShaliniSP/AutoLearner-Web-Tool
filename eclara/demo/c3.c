#include <stdio.h>
float average(int a, int b){
    return (float)(a+b)/2;
}
int main()
{
    int num1, num2;
    float avg;


    scanf("%d",&num1);

    scanf("%d",&num2);

    avg = average(num1, num2);

    //%.2f is used for displaying output upto two decimal places
    printf("%f",avg);

    return 0;
}