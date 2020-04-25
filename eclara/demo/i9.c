

void sort_numbers_ascending(int number[], int count)
{
    
}

void main()
{
   int i, count, number[20];
 
   printf("How many numbers you are gonna enter:");
   scanf("%d", &count);
   printf("\nEnter the numbers one by one:");
   
   for (i = 0; i < count; ++i)
      scanf("%d", &number[i]);
 
   sort_numbers_ascending(number, count);
}
