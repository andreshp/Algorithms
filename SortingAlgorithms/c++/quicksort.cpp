#include <iostream>
#include <stdlib.h>     /* srand, rand */
#include <time.h>  

using namespace std;

// Función para dividir el array y hacer los intercambios
int divide(int *array, int start, int end) {
    int left;
    int right;
    int pivot;
    int temp;
 
    pivot = array[start];
    left = start;
    right = end;
 
    // Mientras no se cruzen los índices
    while (left < right) {
        while (array[right] > pivot) {
            right--;
        }
 
        while ((left < right) && (array[left] <= pivot)) {
            left++;
        }
 
        // Si todavía no se cruzan los indices seguimos intercambiando
        if (left < right) {
            temp = array[left];
            array[left] = array[right];
            array[right] = temp;
        }
    }
 
    // Los índices ya se han cruzado, ponemos el pivot en el lugar que le corresponde
    temp = array[right];
    array[right] = array[start];
    array[start] = temp;
 
    // La nueva posición del pivot
    return right;
}
 
// Función recursiva para hacer el ordenamiento
void quicksort(int *array, int start, int end)
{
    int pivot;
 
    if (start < end) {
        pivot = divide(array, start, end);
 
        // Ordeno la lista de los menores
        quicksort(array, start, pivot - 1);
 
        // Ordeno la lista de los mayores
        quicksort(array, pivot + 1, end);
    }
}

int main(){
    /* Clock returns the number of clock ticks since the program was launched */
    clock_t start;
    double duration;
    start = clock();

    /* Your algorithm here */
    const int LENGHT = 100;
    int array[LENGHT];

    srand(time(NULL));
    for (int i = 0; i < LENGHT; i++){
        array[i] = rand() % 1000;
    }

    quicksort(array, 0, LENGHT - 1);

    int end = LENGHT - 1;
    cout << "Array ordenado: {";
    for (int i = 0; i < end; i++)
        cout << array[i] << ", ";

    cout << array[end] << "}"; 

    /* End of code */
    duration = ( clock() - start ) / (double) CLOCKS_PER_SEC;
    cout<<"Time: "<< duration << endl;
    return 0;
}