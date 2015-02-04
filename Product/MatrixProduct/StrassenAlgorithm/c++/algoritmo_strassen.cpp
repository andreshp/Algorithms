//////////////////////////////////////////////////
// Autor: Andrés Herrera Poyatos
// Estructura de Datos, Práctica 1, Ejercicio 7
///////////////////////////////////////////////////

/* Programa que devuelve el tiempo que el algoritmo de Strassen  para
   multiplicación de matrices tarda en realizar un producto de dos matrices
   de tamaño dado como parámetro */

# include <iostream>
# include <algorithm>
# include <cmath>
#include <ctime>    // Recursos para medir tiempos
#include <cstdlib>  // Para generación de números pseudoaleatorios

using namespace std;

// Coeficiente que indica el tamaño de las matrices a partir del cual se utiliza
// el algoritmo clásico del producto de matrices.
const int UMBRAL_SA = 32;


/**
 * Función para imprimir matrices. Utilizada durante el desarrollo del código.
 */
void imprimirMatriz(int **matriz, int dimension) {
    for (int i=0; i < dimension; i++) {
        for (int j=0; j < dimension; j++) {
            if (j != 0) {
                cout << "\t";
            }
            cout << matriz[i][j];
        }
        cout << endl;
    }
}

/**
 * Algoritmo cásico del producto de matrices. Eficiencia O(n^3).
 */
int **algoritmoClasico(int **A, int **B, int dimension){
    int **C = new int *[dimension];

    for (int i = 0; i < dimension; i++){
        C[i] = new int [dimension];
    }

    for (int i = 0; i < dimension; i++){
        for (int j = 0; j < dimension; j++){
            C[i][j] = 0;
        }
    }

    for (int i = 0; i < dimension; i++){
        for (int k = 0; k < dimension; k++){
            for (int j = 0; j < dimension; j++){
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    return C;
}

/**
 * Función que suma las matrices A y B en C. 
 * Los parámetros translacion permiten sumar Submatrices de Ay B en submatrices de C.
 */
void suma(int  **A, int **B, int **C, int translacion_Ax, int translacion_Ay, int translacion_Bx, int translacion_By, 
    int translacion_Cx, int translacion_Cy, int dimension){ 
    for (int i = 0; i < dimension; i++){
        for (int j = 0; j < dimension; j++){
            C[i+translacion_Cx][j+translacion_Cy] = A[i+translacion_Ax][j+translacion_Ay] + B[i+translacion_Bx][j+translacion_By];
        }
    }
}

/**
 * Función que suma las matrices A y B en C. 
 * Los parámetros translacion permiten sumar Submatrices de Ay B en submatrices de C.
 */
void resta(int  **A, int **B, int **C, int translacion_Ax, int translacion_Ay, int translacion_Bx, int translacion_By, 
    int translacion_Cx, int translacion_Cy, int dimension){
    for (int i = 0; i < dimension; i++) {
        for (int j = 0; j < dimension; j++) {
            C[i+translacion_Cx][j+translacion_Cy] = A[i+translacion_Ax][j+translacion_Ay] - B[i+translacion_Bx][j+translacion_By];
        }
    }   
}

/**
 * Función que computa el producto de A y B recursivamente mediante el algoritmo de Strassen.
 */
int **strassenComputo(int **A, int **B, int dimension){
    
    // Si la dimension de las matrices es menor o igual que el umbral asignado
    // se calcula su producto con el algoritmo clásico.
    if (dimension <= UMBRAL_SA){
        return algoritmoClasico(A, B, dimension);
    }
    else{ // En caso contrario se utiliza el algoritmo de Strassen.

        // Declaración de variables y reserva de memoria:
        int nueva_dimension = dimension/2;
        int **p1, **p2, **p3, **p4, **p5, **p6, **p7;
        int **sumasA, **sumasB;
        int **C;

        sumasA = new int * [nueva_dimension];
        sumasB = new int * [nueva_dimension];
        C = new int * [dimension];

        for (int i = 0; i < nueva_dimension; i++){
            sumasA[i] = new int [nueva_dimension];
            sumasB[i] = new int [nueva_dimension];
        }
        for (int i = 0; i < dimension; i++){
            C[i] = new int [dimension];
        }

        ///////////////////////* CÁLCULO DE p1 ... p7 *///////////////////////////////////////////

        suma(A, A, sumasA, 0, 0, nueva_dimension, nueva_dimension, 0, 0, nueva_dimension); // a11 + a22
        suma(B, B, sumasB, 0, 0, nueva_dimension, nueva_dimension, 0, 0, nueva_dimension); // b11 + b22
        p1 = strassenComputo(sumasA, sumasB, nueva_dimension); // p1 = (a11+a22) * (b11+b22)
        
        suma(A, A, sumasA, nueva_dimension, 0, nueva_dimension, nueva_dimension, 0, 0, nueva_dimension); // a21 + a22
        p2 = strassenComputo(sumasA, B, nueva_dimension); // p2 = (a21+a22) * (b11)
 
        resta(B, B, sumasB, 0, nueva_dimension, nueva_dimension, nueva_dimension, 0, 0, nueva_dimension); // b12 - b22
        p3 = strassenComputo(A, sumasB, nueva_dimension); // p3 = (a11) * (b12 - b22)
 
        resta(B, B, sumasB, nueva_dimension, 0, 0, 0, 0, 0, nueva_dimension); // b21 - b11
        for (int i = 0; i < nueva_dimension; i++){
            for (int j = 0; j < nueva_dimension; j++){
                sumasA[i][j] = A[i+nueva_dimension][j+nueva_dimension]; // sumasA = a22
            }
        }
        p4 = strassenComputo(sumasA, sumasB, nueva_dimension); // p4 = (a22) * (b21 - b11)
 
        suma(A, A, sumasA, 0, 0, 0, nueva_dimension, 0, 0, nueva_dimension); // a11 + a12
        for (int i = 0; i < nueva_dimension; i++){
            for (int j = 0; j < nueva_dimension; j++){
                sumasB[i][j] = B[i+nueva_dimension][j+nueva_dimension]; // sumasB = b22
            }
        }
        p5 = strassenComputo(sumasA, sumasB, nueva_dimension); // p5 = (a11+a12) * (b22)   
 
        resta(A, A, sumasA, nueva_dimension, 0, 0, 0, 0, 0, nueva_dimension); // a21 - a11
        suma(B, B, sumasB, 0, 0, 0, nueva_dimension, 0, 0, nueva_dimension); // b11 + b12
        p6 = strassenComputo(sumasA, sumasB, nueva_dimension); // p6 = (a21-a11) * (b11+b12)
 
        resta(A, A, sumasA, 0, nueva_dimension, nueva_dimension, nueva_dimension, 0, 0, nueva_dimension); // a12 - a22
        suma(B, B, sumasB, nueva_dimension, 0, nueva_dimension, nueva_dimension, 0, 0, nueva_dimension); // b21 + b22
        p7 = strassenComputo(sumasA, sumasB, nueva_dimension); // p7 = (a12-a22) * (b21+b22)
 
        //////////////////////* CÁLCULO DE LA MATRIZ C *///////////////////////////////////////////

        suma(p3, p5, C, 0, 0, 0, 0, 0, nueva_dimension, nueva_dimension); // c12 = p3 + p5
        
        suma(p2, p4, C, 0, 0, 0, 0, nueva_dimension, 0, nueva_dimension); // c21 = p2 + p4
        
        suma(p1, p4, sumasA, 0, 0, 0, 0, 0, 0, nueva_dimension); // p1 + p4
        suma(sumasA, p7, sumasB, 0, 0, 0, 0, 0, 0, nueva_dimension); // p1 + p4 + p7
        resta(sumasB, p5, C, 0, 0, 0, 0, 0, 0, nueva_dimension); // c11 = p1 + p4 - p5 + p7
        
        suma(p1, p3, sumasA, 0, 0, 0, 0, 0, 0, nueva_dimension); // p1 + p3
        suma(sumasA, p6, sumasB, 0, 0, 0, 0, 0, 0, nueva_dimension); // p1 + p3 + p6
        resta(sumasB, p2, C, 0, 0, 0, 0, nueva_dimension, nueva_dimension, nueva_dimension); // c22 = p1 + p3 - p2 + p6
        
        //////////////////////* LIBERACIÓN DE MEMORIA *///////////////////////////////////////////
        
        for (int i = 0; i < nueva_dimension; i++){
            delete [] p1[i];
            delete [] p2[i];
            delete [] p3[i];
            delete [] p4[i];
            delete [] p5[i];
            delete [] p6[i];
            delete [] p7[i];
            delete [] sumasA[i];
            delete [] sumasB[i];   
        }

        delete [] p1;
        delete [] p2;
        delete [] p3;
        delete [] p4;
        delete [] p5;
        delete [] p6;
        delete [] p7;
        delete [] sumasA;
        delete [] sumasB;

        return C;
    }
}

/**
 * Función que devuelve la siguiente potencia de 2 de un número n dado.
 */
int siguientePotencia2(int n){
    return pow(2, int(ceil(log2(n))));
}

/**
 * Algoritmo de Strassen para el producto de matrices.
 * Amplía las matrices A y B a matrices con dimension = siguientePotencia2(dimension) y llama a strassenComputo
 * para calcular el producto. Es necesario ampliar la dimensión pues strassenComputo solo trabaja 
 * con matrices de dimensión potencia de 2.
 */
int **strassenAlgorithm(int **A, int **B, int dimension){
    
    /////////////////* DECLARACIÓN DE VARIABLES Y RESERVA DE ESPACIO *///////////////

    int m = siguientePotencia2(dimension);

    int **Apreparada, **Bpreparada, **Cpreparada, **C;

    Apreparada = new int * [m];
    Bpreparada = new int * [m];
    C = new int * [dimension];

    for (int i = 0; i < m; i++){
        Apreparada[i] = new int [m];
        Bpreparada[i] = new int [m];
    }
    for (int i = 0; i < dimension; i++){
        C[i] = new int [dimension];
    }
    
    for(int i=0; i < m; i++) {
        for (int j=0; j < m; j++) {
            Apreparada[i][j] = 0;
            Bpreparada[i][j] = 0;
        }
    }
    
    for(int i=0; i < dimension; i++) {
        for (int j=0; j < dimension; j++) {
            Apreparada[i][j] = A[i][j];
            Bpreparada[i][j] = B[i][j];
        }
    }

    //////////////////////* CÁLCULO DE LA MATRIZ C *///////////////////////////////////////////

    Cpreparada = strassenComputo(Apreparada, Bpreparada, m);
    for(int i = 0; i < dimension; i++) {
        for (int j = 0; j < dimension; j++) {
            C[i][j] = Cpreparada[i][j];
        }
    }

    //////////////////////* LIBERACIÓN DE MEMORIA *///////////////////////////////////////////

    for (int i = 0; i < m; i++){
        delete [] Apreparada[i];
        delete [] Bpreparada[i];
        delete [] Cpreparada[i];
    }

    delete [] Apreparada;
    delete [] Bpreparada;
    delete [] Cpreparada;

    return C;
}

/**
 * Función void que muestra por pantalla la sintaxis del programa
 */
void sintaxis()
{
  cerr << "Sintaxis:" << endl;
  cerr << "  DIM: dimensión de la matriz cuadrada (>0)" << endl;
  cerr << "  VMAX: Valor máximo (>0)" << endl;
  cerr << "Se genera una matriz cuadrada DIMxDIM con elementos aleatorios en [0,VMAX[" << endl;
  exit(EXIT_FAILURE);
}


int main (int argc, char* argv[]){

    // Lectura de parámetros
    if (argc!=3)
        sintaxis();
    int dimension=atoi(argv[1]);     // Tamaño del vector
    int vmax=atoi(argv[2]);    // Valor máximo
    if (dimension<=0 || vmax<=0)
        sintaxis();
  
    // Generación de dos matrices aleatorias:
    int **A=new int *[dimension];       // Reserva de memoria
    int **B=new int *[dimension];       // Reserva de memoria
    int **C;

    for (int i = 0; i < dimension; i++){
        A[i] = new int [dimension];
        B[i] = new int [dimension];
    }

    srand(time(0));            // Inicialización del generador de números pseudoaleatorios
    for (int i = 0; i < dimension; i++){
        for (int j = 0; j < dimension; j++){
            A[i][j] = rand() % vmax;    // Generar aleatorio [0,vmax[
            B[i][j] = rand() % vmax;    // Generar aleatorio [0,vmax[
        }
    }

    clock_t tini;    // Anotamos el tiempo de inicio
    tini=clock();
  
    C = strassenAlgorithm(A, B, dimension);  // Se llama al algoritmo
    
    clock_t tfin;    // Anotamos el tiempo de finalización
    tfin=clock();

    // Mostramos resultados
    cout << dimension << "\t" << (tfin-tini)/(double)CLOCKS_PER_SEC << endl;
    
    for (int i = 0; i < dimension; i++){
        delete [] A[i];
        delete [] B[i];
        delete [] C[i];
    }

    delete [] A;
    delete [] B;
    delete [] C;
    
    return 0;
}