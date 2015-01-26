//////////////////////////////////////////////////
// Autor: Andrés Herrera Poyatos
// Date: February, 2014
// Sorting Algorithm: HeapSort
///////////////////////////////////////////////////

/* Programa que devuelve el tiempo que el algoritmo de ordenación heapsort
   tarda en ordenar un array de tamaño dado comoo argumento */

#include <iostream>
#include <stdlib.h>
#include <time.h>  

using namespace std;

inline void Swap(int* array, int i, int j){
	int exchange = array[i];
	array[i] = array[j];
	array[j] = exchange;
}

void MaxHeapify(int* heap, int start, int end){
	int root = start;
	int child = 2 * start + 1;
	while(child < end){
		if (child + 1 < end && heap[child] < heap[child+1])
			child++;
		if (heap[root] < heap[child]){
			Swap(heap, child, root);
		}
		else break;
		root = child;
		child = 2 * root +1;
	}
}

void BuildMaxHeap(int* array, int start, int end){
	for (int i = (end-2)/2; i >= 0; i--)
		MaxHeapify(array, i, end);
}

void HeapSort(int* array, int start, int end){
	BuildMaxHeap(array, start, end);
	while (end > 0){
		Swap(array, 0, end-1);
		end--;
		MaxHeapify(array, 0, end);
	}
}

int main(){

    // Time inicialization:
    srand(time(NULL));
	clock_t start;

    // Array declaration:
    const int LENGHT = 2000000;
    int array[LENGHT];

    for (int i = 0; i < LENGHT; i++){
    	array[i] = rand() % 10034210;
    }

    // Start Sorting
    start = clock();

    HeapSort(array, 0, LENGHT);

    // Total time:
	cout << "Time: " << ( clock() - start ) / (double) CLOCKS_PER_SEC << endl;
	return 0;
}