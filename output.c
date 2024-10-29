#include <stdio.h>
#include <stdlib.h>
int main() {
float x, y, wynik, reszta;
x = 4;
y = 3;
wynik = 0;
reszta = x;
while(reszta<y) {
reszta = reszta-y;
while(reszta>2) {
wynik = wynik+1;
}
wynik = wynik+2;
}
if(wynik==0) {printf("%s\n", "Oh yeah");}
printf("%f\n", wynik);
return 0;
}