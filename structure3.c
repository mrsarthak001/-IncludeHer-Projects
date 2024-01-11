#include<stdio.h>
int main()
{
    struct s1
    {
        int a;
        char d;
        float c;
    };

    struct s2
    {
        int a;
        float c;
        struct s1 d;
    };

   struct s2 f = {20,23.45,{2,'a',45.34}};

     printf("%d\n",f);
     printf("%d\n",f.a);
     printf("%0.1f\n",f.c);
     printf("%d\n",f.d);
     printf("%d\n",f.d.a);
    printf("%c\n",f.d.d);
     printf("%0.1f\n",f.d.c);
     printf("\n\n\n");

     //pointer variable created;
     struct s2 *n = &f;
     //print address
     printf("%d\n",n);
     printf("%d\n",&n);
      printf("%d\n",&(n->a));
      printf("%d\n",&((*n).a));
//print values corresponding to the addressess;
     printf("%d\n",*n);
     printf("%d\n",(*n).a);
     printf("%d\n",n->a);
     printf("%0.1f\n",n->c);
      printf("%d\n",n->d);
     printf("%d\n",(n->d).a);
     printf("%c\n",(n->d).d);
     printf("%0.1f\n",(n->d).c);


}