#include <stdio.h>

// Function to print Fibonacci series up to 'n' terms
void printFibonacci(int n) {
    int a = 0, b = 1, next;
    
    printf("Fibonacci Series: ");
    
    for (int i = 0; i < n; i++) {
        if (i == 0) {
            printf("%d ", a);
            continue;
        }
        if (i == 1) {
            printf("%d ", b);
            continue;
        }
        
        next = a + b;
        a = b;
        b = next;
        
        printf("%d ", next);
    }
    
    printf("\n");
}

int main() {
    int n;

    // Ask user for number of terms
    printf("Enter the number of terms for Fibonacci series: ");
    scanf("%d", &n);

    // Print the Fibonacci series
    printFibonacci(n);

    return 0;
}
