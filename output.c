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
wynik = wynik+1;

}
printf("%f\n", wynik);
 return 0;
}