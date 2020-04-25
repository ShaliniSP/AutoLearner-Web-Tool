#include <stdio.h>
int main()
{
    char ch;
    bool isVowel = false;

    printf("Enter an alphabet: ");
    scanf("%c",&ch);

    if(ch=='a'||ch=='e'||ch=='i'
    		||ch=='o'||ch=='u')
    {
    	isVowel = true;

    }
    if (isVowel == true)
        printf("%c is a Vowel", ch);
    else
        printf("%c is a Consonant", ch);
    return 0;
}