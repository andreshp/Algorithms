# include <iostream>
# include <cstdlib>
# include <time.h>

using namespace std;

/*
    FUNCTION: peakFinding2D
    INPUT: A nxm matrix, its start and end colums, its rows number and the integers where the function will save the peak's position.
    OUTPUT: Peak's Position.
    ALGORITHM: Finding a 2D peak with Binary Search in the colums, according to the max of them. Time 0(nlog(m)). Recursive.
*/

void peakFinding2D(int** matrix, int start, int end, int n, int &peak_i, int &peak_j){
    int middle = (start + end)/2, pos_max = 0;
    for (int i = 1; i < n; i++){
        if (matrix[i][middle] > matrix[pos_max][middle]){
            pos_max = i;
        }
    }
    if (start < middle && matrix[pos_max][middle-1] > matrix[pos_max][middle]){
        return peakFinding2D(matrix, start, middle-1, n, peak_i, peak_j);
    }
    else if (end > middle && matrix[pos_max][middle+1] > matrix[pos_max][middle]){
        return peakFinding2D(matrix, middle+1, end, n, peak_i, peak_j);
    }
    else{
        peak_i = pos_max;
        peak_j = middle; 
    }
}

int main(){
    const int n = 50000, m = 10000, ;
    srand(time(NULL));
    int **matrix = new int*[n]; 
    int peak_i = 0, peak_j = 0;
    
    for(int i = 0; i < n; i++){
        matrix[i] =  new int[m];
    }
    for (int i = 0; i < n; i++){
        for (int j = 0; j < m; j++){
            matrix[i][j] = rand() % 1000;
        }
    }

    /* Clock returns the number of clock ticks since the program was launched */
    double duration;
    clock_t start;
    start = clock();
    peakFinding2D(matrix, 0, m-1, n, peak_i, peak_j);

    /* End of code */
    duration = (double)(clock() - start ) / (double) CLOCKS_PER_SEC;
    cout << "There is a peak in the position (" << peak_i << ", " << peak_j << ") of the matrix. It's value is: " << matrix[peak_i][peak_j] << endl;
    cout<<"Time: "<< duration << endl;

    // Output:
    //cout << "Matriz: \n";
    //for (int i = 0; i < n; i++){
    //    for (int j = 0; j < m; j++){
    //        cout << matrix[i][j] << " ";
    //    }
    //    cout << endl;
    //}


}