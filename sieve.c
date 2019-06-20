
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Incorrect number of arguments: Specify the maximum number for which to calculate the primes\n");
        return 1;
    }
    int max_prime = atoi(argv[1]);
    if (max_prime < 10)
    {
        printf("Incorrect maximum prime number, should be at least 10\n");
        return 1;
    }
    printf("Calculating all primes p < %i...\n", max_prime);
    bool primes[max_prime+1];
    primes[0] = false;
    primes[1] = false;
    for (int i=2; i< max_prime+1; ++i)
    {
        primes[i] = true;
    }
    
    for (int i=2; i<max_prime+1; ++i)
    {
        if (primes[i])
        {
            for (int j=2*i; j<max_prime+1; j+=i)
            {
                primes[j] = false;
            }
        }
    }
    printf("Primes are:\n\t");
    int printed_primes = 0;
    for (int i=2; i<max_prime+1; ++i)
    {
        if (primes[i])
        {
            printf("%i ", i);
            if (printed_primes++ % 10 == 0)
            {
                printf("\n\t");
            }
        }
    }   
    printf("\n");
    return 0;
}