
int fib(int n) {
    if (n <= 0) {
        return 1;
    } else if (n == 1) {
        return 1;
    } else {
        return fib(n-1) + fib(n-2);
    }
}

void main() {
    int n = 9;
    int valor = fib(n);
    printf("El numero es: %d", valor);
}