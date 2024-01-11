#include <stdio.h>
int main()
{
      int a,b,c;
      float sum;
      float avg;
       
      printf("\nEnter First Number  : ");
      scanf("%d", &a);
      printf("\nEnter Second Number : ");
      scanf("%d",&b);
      printf("\nEnter Third Number : ");
      scanf("%d",&c);
      sum = a+b+c;
      avg=sum/3.0;
      printf("\nAverage of Three Numbers : %.2f",avg);
      return 0;
}
