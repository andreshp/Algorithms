/* 
* @Author: andreshp
* @Date:   2015-06-21
* @Last Modified by:   andreshp
* @Last Modified time: 2015-06-21
*/

#include <iostream>

using namespace std;

const int MAX_N = 200000;
long array[MAX_N];

//---------------------------- FUNCTIONS ----------------------------//

void query1(long array[], int x, int y, int N){
    long count = 0;
    for (int i = 0; i < y-x+1; i++){
        count = (count + (i+1)*(i+2)) % 1000000007;
        array[x+i] = (array[x+i] + count) % 1000000007;        
    }

    for (int i = y+1; i < N; i++)
        array[i] = (array[i] + count) % 1000000007;    
}

long query2(int array[], int x, int y){
    if (x == 0)
        return array[y];
    else{
        long sol = array[y] - array[x-1];
        if (sol < 0)
            sol = 1000000007 + sol;
        return sol;
    }
}

//------------------------------ MAIN -------------------------------//

int main(){
    int N, Q, t, x, y;
    cin >> N >> Q;
    for (int i = 0; i < N; i++)
        array[i] = 0;

    for (int q = 0; q < Q; q++){
        cin >> t >> x >> y;
        if (t == 1)
            query1(array,x-1,y-1, N);
        else
            cout << query2(array,x-1,y-1);
    }

    return 0;
}