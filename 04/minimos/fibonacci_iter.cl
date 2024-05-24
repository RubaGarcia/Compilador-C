void main(){
    int var1 = 1;
    int var2 = 1;
    int aux = 0;
    int i = 10;
    
    /*
    while(i > 0){
        printf("%d,", var1);
        aux = var1+var2;
        var1 = var2;
        var2 = aux;
        i = i - 1;
    }
    */
    while (true){
        printf("%d,", var1);
        aux = var1+var2;
        var1 = var2;
        var2 = aux;
        i = i - 1;
        if (i<0){
            break;
        }
    }
    
}