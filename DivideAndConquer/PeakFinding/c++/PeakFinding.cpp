# include <iostream>
# include <cstdlib>
# include <ctime>

using namespace std;

/*
    FUNCTION: peakFinding
    INPUT: An array and it's start and end position.
    OUTPUT: Peak's Position.
    ALGORITHM: Finding a peak with Binary Search. Time 0(log(n)). Recursive.
*/
int peakFinding(int* array, int start, int end){
    int middle = (start + end)/2;
    
    if (start < middle && array[middle-1] > array[middle]){
        return peakFinding(array, start, middle-1);
    }
    else if (end > middle && array[middle] < array[middle+1]){
        return peakFinding(array, middle+1, end);
    }
    else{
        return middle; 
    }
}

int main(){

    srand(time(NULL));
    const long long size = 100000;
    int array[size];
    
    for (int i = 0; i < size; i++){
        array[i] = rand() % 100000;
    }

    /* Clock returns the number of clock ticks since the program was launched */
    clock_t start;
    double duration;
    start = clock();

    int pos_peak = peakFinding(array,0, size-1);

    cout << "There is a peak in the position " << pos_peak << " of the array. It's value is: " << array[pos_peak] << endl;
    /* End of code */
    duration = ( clock() - start ) / (double) CLOCKS_PER_SEC;
    cout<<"Time: "<< duration << endl;

    // Output array:
    //cout << "Array: {";
    //for (int i = 0; i < size-1; i++)
    //    cout << array[i] << ", ";
    //cout << array[size-1] << "}" << endl;


}