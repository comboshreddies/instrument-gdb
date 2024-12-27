#include <stdio.h>

int dive(int a) {
  if(a>120)
    return a;
  if(! (a % 10))
    printf("aaa %d\n",a);
  return dive(a+1);
}

int main() {
  dive(0);
  return 0;
}

