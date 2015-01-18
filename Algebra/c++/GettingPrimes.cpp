/////////////////////////////////////
// Author: Andrés Herrera Poyatos
/////////////////////////////////////

# include <iostream>
# include <cmath>
# include <climits>
# include <cstdio>
# include <sstream>
# include <algorithm>
# include <assert.h>

using namespace std;

#define ll long long int

ll i, j, k, N, T, s;
ll primes[10000];

bool is_prime;

int main(){
    
    primes[0] = 2;
    k = 3;
    
    for (i = 1; i < 10000; i++){
        is_prime = true;
        while(is_prime){
            s = (ll)(sqrt(k)) + 1;
            for (j = 1; j < i && primes[j] <= s; j++){
                if (k % primes[j] == 0){
                    is_prime = false;
                }
            }
            if (is_prime){
                primes[i] = k;
                is_prime = false;
            }
            else{
                is_prime = true;
            }
            k +=2;
        }
    }
    
    cin >> T;
    while(T--){
        cin >> N;
        cout << primes[N-1] << endl;
    }
    return 0;    
}