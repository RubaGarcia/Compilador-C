//#include <stdio.h>
//definición de primeras variables


int prev1 = 1;
int prev2 = 0;

/*
función de fibonacci
f(n)=f(n-1)+f(n-2)
*/
void fib(int n) {
    if (n < 3) {
        return;
    }
    int fn = prev1 + prev2;
    prev2 = prev1;
    prev1 = fn;
    printf("%d ", fn);
    return fib(n - 1);
}

void printFib(int n) {
    if (n < 1) {
        printf("Invalid number of terms\n");
    } else if (n == 1) {
        printf("%d ", 0);
    } else if (n == 2) {
        printf("%d %d", 0, 1);
    } else {
        printf("%d %d ", 0, 1);
        fib(n);
    }
}

int main() {
    int n = 9; // Change this value to print a different number of terms
    printFib(n);
    return 0;
}