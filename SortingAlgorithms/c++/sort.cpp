#include <iostream>
#include <algorithm>

using namespace std;

int main(){
        const int MAX = 1000;
        int numbers[MAX];
        const int TERMINATOR = -1;
        int length = 0;
        int current_int;

        cin >> current_int;

        while (current_int != TERMINATOR){
            numbers[length] = current_int;
            length++;
            cin >> current_int;
        }

        sort(numbers, numbers + length);

        for (int i = 0; i < length; i++){
                cout << numbers[i] << " ";
        }
}