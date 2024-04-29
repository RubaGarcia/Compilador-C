int main(){
    int previo1 = 1;
    int previo2 = 1;
    for(int i = 0; i < 10;i++){
        int fn = previo1 + previo2;
        previo2 = previo1;
        previo1 = fn;
        printf("%d ", fn);
    }
}