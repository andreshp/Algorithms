#include <iostream>
#include <stdlib.h>     /* srand, rand */
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
	/* Clock returns the number of clock ticks since the program was launched */
	clock_t start;
    double duration;
	start = clock();

    /* Your algorithm here */
    const int LENGHT = 2000000;
    int array[LENGHT];

    srand(time(NULL));
    for (int i = 0; i < LENGHT; i++){
    	array[i] = rand() % 10034210;
    }

    HeapSort(array, 0, LENGHT);

    /* int end = LENGHT - 1;
	cout << "Array ordenado: {";
	for (int i = 0; i < end; i++)
		cout << array[i] << ", ";

	cout << array[end] << "}"; */

    /* End of code */
    duration = ( clock() - start ) / (double) CLOCKS_PER_SEC;
	cout<<"Time: "<< duration << endl;
	return 0;
}