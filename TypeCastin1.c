#include<stdio.h>
#define pf printf
int main()
{
    int a = 300;
    char *b = (char *)&a;
    b++;
    *b = 2;
    pf("%d",a);
}