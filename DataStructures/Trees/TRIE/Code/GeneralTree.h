////////////////////////////////////////////////////////////
// Autor: Andrés Herrera Poyatos
// Universidad de Granada, 2º DGMII, Estructura de Datos
// Practica Final, Clase GeneralTree, archivo .h
////////////////////////////////////////////////////////////

/**
 * @file GeneralTree.h
 * @brief Fichero cabecera del TDA GeneralTree.
 *
 * Gestiona un árbol general con facilidades para la inserción,
 * obtención y borrado de subárboles, así como la entrada y salida de datos
 * y el recorrido mediante iteradores.
 */

# ifndef GENERAL_TREE
# define GENERAL_TREE

# include <iostream>
# include <stdexcept> // Excepciones

using namespace std;

/**
 * @brief T.D.A. GeneralTree.
 * 
 * ### Descripción del tipo de dato abstracto ###
 *
 * Una instancia *a* del tipo de dato abstracto GeneralTree sobre un dominio 
 * *T* se puede construir como:
 *
 * - Un objeto vacío (árbol vacío) si no contiene ningún elemento. 
 *   Lo denotamos {}.
 *   
 * - Un árbol que contiene un elemento destacado, el nodo raíz, con un valor 
 *   *e* perteneciente a *T* (denominado *clave*), y *k* subárboles 
 *   \f$(T_1, \ldots, T_k)\f$ del T.D.A. GeneralTree sobre *T*. Estos subárboles
 *   pueden ser hijos de la raíz o bien hermanos (a la derecha) de la misma.
 *
 * Cada nodo mantiene un puntero a su padre, hermano a la derecha e hijo más
 * a la izquierda, lo que permite obtener la jerarquía de árbol pertinente.
 *
 * La clase GeneralTree sirve como base para desarrollar árboles generales
 * con características extras que los hagan útiles como estructuras de datos.
 * Este es el caso, por ejemplo, de los árboles *Trie*.
 * 
 * Para poder usar el tipo de dato GeneralTree se debe incluir el fichero
 * 
 * <tt>\#include GeneralTree.h</tt>
 * 
 * El espacio requerido para el almacenamiento del Árbol General es O(*n*), donde 
 * *n* es el número de nodos del árbol.
 *
 * ### Información sobre la Implementación ###
 *
 * La implementación se realiza utilizando punteros entre los nodos que se alojan
 * en memoria dinámica. Se proporcionan métodos públicos para el manejo de los
 * nodos escondiendo los punteros internos así como iteradores que recorran la estructura
 * de árbol.
 *
 * @author Andrés Herrera Poyatos
 * @date 23 de diciembre de 2014
 */

template <class T>
class GeneralTree{

    private:

        /**
         * 
         * @brief Estructura que representa un nodo del árbol general.
         *
         * ### Descripción del tipo de dato abstracto ###
         *
         * Una instancia *c* del tipo de dato abstracto NodeP sobre un dominio *T* consiste en
         * una terna formada por un elemento de *T* y dos punteros a dos objetos NodeP que permite
         * la creación de un Árbol General cuyos nodos están enlazados según la relación 
         * padre -- hijo más a la izquierda -- hermano derecha.
         *
         * ### Información sobre la Implementación ###
         *
         * Se implementa mediante un struct privado de la clase General Tree. De esta forma solo
         * esta clase puede usar los nodos y sin ningún tipo de restricción. Se proporcionan
         * además dos posibles constructores.
         * 
         * @author Andrés Herrera Poyatos
         * @date 23 de Diciembre de 2014
         */
        struct NodeP {
            
            // ------------------- Datos Miembro -------------------- //
        
            /**
             *@brief Clave almacenada del tipo de dato *T*.
             *
             * En este campo se almacena la clave que le corresponde a este nodo.
             */
            T key;
            /**
             * @brief Puntero al hijo más a la izquierda.
             *
             * En este campo se almacena un puntero al nodo raíz del subárbol más a 
             * la izquierda, o un puntero nulo si no lo tiene.
             */
            NodeP *leftc; // left child
            /**
             * @brief Puntero al hermano derecho.
             *
             * En este campo se almacena un puntero al nodo raíz del subárbol 
             * hermano derecho, o el valor 0 si no tiene.
             */
            NodeP *rightb; // right brother
            /**
             * @brief Puntero al padre.
             *
             * En este campo se almacena un puntero al nodo padre, 
             * o un puntero nulo si el nodo es la raíz.
             */
             NodeP *parent;

            // ------------------- Constructores -------------------- //
        
             /**
             * @brief Constructor por defecto.
             */
            NodeP() : leftc(NULL), rightb(NULL), parent(NULL)
            {}
            /**
             * @brief Constructor con parámetros.
             * @param key Elemento de *T* que se almacenará en el nodo..
             * @param leftc Puntero al hijo izquierda.
             * @param rightb Puntero al hermano derecha.
             * @param parent Puntero al padre.
             */
            NodeP(const T & key, NodeP * leftc, NodeP * rightb, NodeP * parent): key(key), leftc(leftc), rightb(rightb), parent(parent)
            {}
        };

        // ------------------- Datos Miembro -------------------- //
     
        /**
         * @brief Puntero a la raíz del árbol.
         *
         * Este miembro es un puntero al primer nodo, que corresponde a la raíz 
         * del árbol. En caso de ser un árbol vacío se representa mediante un puntero nulo.
         */
        NodeP *root;

        /**
         * @brief Destruye el subárbol cuya raíz es indicada como argumento.
         * @param n Raíz del subárbol a destruir.
         *
         * Libera los recursos que ocupa el subárbol de raíz *n* junto con el de
         * sus hermanos derecha.
         */
        void destroy(NodeP * n);

        /**
         * @brief Copia un subárbol.
         * @param origin Puntero a la raíz del subárbol a copiar.
         * @param destination Referencia al puntero del que colgará la copia.
         * @param parent Puntero al padre del futuro nodo *destination*.
         *
         * Hace una copia de todo el subárbol que cuelga de *origin* en el puntero
         * *destination*. A \e destination->parent se le asigna *parent*.
         */
        void copy(NodeP * origin, NodeP *& destination, NodeP * parent);
          
        /**
         * @brief Devuelve el número de nodos (size) del subárbol del cual *n* es raíz.
         * @param n Raíz del subárbol del cual se pretende obtener su tamaño.
         *
         * Cuenta cuántos nodos cuelgan de *n*, incluido éste.
         */
        int sizeP(const NodeP * n) const;
        
        /**
         * @brief Comprueba si dos subárboles dados son iguales.
         * @param n1 Primer subárbol a comparar.
         * @param n2 Segundo subárbol a comparar.
         *
         * Comprueba si son iguales los subárboles que tienen como raíz a *n1* y *n2*. 
         * Para ello deberán tener los mismos nodos en las mismas posiciones y 
         * con las mismas claves.
         */
        bool areEqual(const NodeP * n1, const NodeP * n2) const;
    
        /**
         * @brief Escribe un subárbol en un stream dado.
         * @param out Stream de salida donde se escribe el árbol.
         * @param n Nodo del que cuelga el subárbol a escribir.
         *
         * Escribe en el flujo de salida todos los nodos del subárbol que cuelga 
         * del nodo *n* siguiendo un recorrido en preorden. 
         * La sintaxis seguida para la impresión es la siguiente:
         *
         * - Si el nodo es nulo, imprime el carácter 'x'.
         * - Si el nodo no es nulo, imprime el carácter 'n' seguido de un 
         *   espacio y la clave correspondiente.
         */
        void printTree(ostream & out, NodeP * n) const;
  
        /**
         * @brief Lee un subárbol a partir de un string dado.
         * @param in Stream de entrada desde el que se lee el árbol.
         * @param n Referencia al nodo que contendrá el subárbol leído.
         *
         * Lee del flujo de entrada *in* los elementos de un árbol según el 
         * formato que se presenta en el método printTree.
         *
         * @see printTree
         */
        void readTree(istream& in, NodeP *& n, NodeP * parent);
      
  public:

        /**
         * @brief Tipo Node
         * 
         * Este tipo nos permite manejar cada uno de los nodos del árbol. Los 
         * valores que tomará serán tantos como nodos en el árbol (para poder 
         * referirse a cada uno de ellos) y además un valor destacado
         * \e nulo (0), que indica que no se refiere a ninguno de ellos.
         *
         * Una variable \e n de este tipo se declara
         *
         * <tt>GeneralTree::Node n;</tt>
         *
         * Las operaciones válidas sobre el tipo node son:
         *
         * - Operador de Asignación (=).
         * - Operador de comprobación de igualdad (==).
         * - Operador de comprobación de desigualdad (!=).
         */
        typedef struct NodeP * Node;

        /**
         * @brief Constructor por defecto.
         *
         * Reserva los recursos e inicializa el árbol a vacío {}. La operación se
         * realiza en tiempo O(1).
         */
        GeneralTree() : root(NULL)
        {}
    
        /**
         * @brief Constructor de raíz
         * @param key Clave de la raíz
         *
         * Reserva los recursos e inicializa el árbol con un único nodo raíz
         * de clave key. La operación se realiza en tiempo O(1).
         */
        GeneralTree(const T& key) : root(new NodeP(key, NULL, NULL, NULL))
        {}

        /**
         * @brief Constructor de copia.
         * @param other GeneralTree a copiar
         *
         * Construye el árbol duplicando el contenido de *other* en el árbol 
         * receptor. La operación se realiza en tiempo O(*n*), donde *n* es 
         * el número de elementos de *other*.
         */
        GeneralTree(const GeneralTree<T> & other){
            copy(other.root, root, NULL);
        }

        /**
         * @brief Destructor
         *
         * Libera los recursos ocupados por el árbol receptor. La operación se 
         * realiza en tiempo O(n), donde n es el número de elementos del árbol.
         */
        ~GeneralTree(){
            destroy(root);
        }

        /**
         * @brief Operador de asignación.
         * @param other GeneralTree a copiar.
         * @return Referencia al árbol receptor para posibles encadenaciones.
         *
         * Asigna el valor del árbol duplicando el contenido de *other* en el árbol 
         * receptor. La operación se realiza en tiempo O(n), donde *n* es el número de 
         * elementos de *other*.
         */
        GeneralTree<T> & operator=(const GeneralTree<T> & other);

        /**
         * @brief Reinicia el árbol a un nuevo nodo raíz.
         * @param key Clave a asignar al nodo raíz.
         *
         * Vacía el árbol receptor y le asigna un único nodo cuya etiqueta es *key*.
         */
        inline void setRoot(const T & key){
            destroy(root);
            root = new NodeP(key, NULL, NULL, NULL);
        }
    
        /**
         * @brief Devuelve la raíz del árbol.
         */
        inline const Node & getRoot() const{
            return root;
        }

        /**
         * @brief Devuelve el hijo más a la izquierda de un nodo dado.
         * @param n Nodo del que se quiere obtener el hijo más a la izquierda.
         * @pre *n* no es nulo.
         *
         * En caso de no tener hijos se devuelve NULL.
         */
        Node & leftChild(const Node n) const{
            if (n != NULL)
                return n->leftc;
            else
                throw runtime_error("El nodo del que se pretende obtener el hijo de la izquierda es nulo");
        }
    
        /**
         * @brief Devuelve el hermano situado a la derecha de un nodo dado.
         * @param n Nodo del que se quiere obtener el hermano a la derecha.
         * @pre *n* no es nulo
         *
         * En caso de no tener hermanos a la derecha se devuelve NULL.
         */
        inline Node & rightBrother(const Node n) const{
            if (n != NULL)
                return n->rightb;
            else
                throw runtime_error("El nodo del que se pretende obtener el hermano a la derecha es nulo");
        }

        /**
         * @brief Devuelve el nodo padre de un nodo dado.
         * @param n Nodo del que se quiere obtener el padre.
         * @pre *n* no es nulo.
         *
         * En caso de no tener padre se devuelve NULL.
         */
        inline Node & parent(const Node n) const{
            if (n != NULL)
                return n->parent;
            else
                throw runtime_error("El nodo del que se pretende obtener su padre es nulo");
        }

        /**
         * @brief Devuelve una referencia a la clave de un nodo dado.
         * @param n Nodo del que se quiere obtener la clave.
         * @pre *n* no es nulo
         */
        inline T& key(const Node n){
            if (n != NULL)
                return n->key;
            else
                throw runtime_error("El nodo del que se pretende obtener su clave es nulo");
        }

        /**
         * @brief Devuelve una referencia constante a la clave de un nodo dado.
         * @param n Nodo del que se quiere obtener la clave.
         * @pre *n* no es nulo
         */
        inline const T& key(const Node n) const{
            if (n != NULL)
                return n->key;
            else
                throw runtime_error("El nodo del que se pretende obtener su clave es nulo");
        }
    
        /**
         * @brief Poda el subárbol iniciado por n.
         * @param n Nodo que inicia el subárbol a podar. 
         * @param destination Árbol que recibe la rama cortada.
         * @pre *n* no es nulo y es un nodo válido del árbol receptor.
         *
         * Asigna un nuevo valor al árbol *destination*, con todos los elementos del 
         * subárbol del nodo *n* en el árbol receptor. Éste se queda sin 
         * dichos nodos. La operación se realiza en tiempo O(numChild(parent(n))).
         */
        void pruneSubtree(Node n, GeneralTree<T> & destination);

        /**
         * @brief Poda el subárbol hijo más a la izquierda.
         * @param n Nodo al que se le podará la rama hijo más a la izquierda. 
         * @param destination Árbol que recibe la rama cortada.
         * @pre *n* no es nulo y es un nodo válido del árbol receptor.
         *
         * Asigna un nuevo valor al árbol *destination*, con todos los elementos del 
         * subárbol izquierdo del nodo *n* en el árbol receptor. Éste se queda sin 
         * dichos nodos. La operación se realiza en tiempo O(1).
         */
        void pruneLeftChild(Node n, GeneralTree<T> & destination);

        /**
         * @brief Poda el subárbol hermano derecha.
         * @param n Nodo al que se le podará la rama hermano derecha. 
         * @param destination Árbol que recibe la rama cortada.
         * @pre *n* no es nulo y es un nodo válido del árbol receptor.
         *
         * Asigna un nuevo valor al árbol *destination*, con todos los elementos del 
         * subárbol hermano derecho del nodo *n* en el árbol receptor. Éste se queda 
         * sin dichos nodos. La operación se realiza en tiempo O(1).
         */
        void pruneRightBrother(Node n, GeneralTree<T> & destination);
    
        /**
         * @brief Inserta el subárbol dado en el hijo más a la izquierda.
         * @param n Nodo en el que se insertará el árbol *tree* como hijo más a la izquierda.
         * @param tree Árbol que se insertará como hijo más a la izquierda.
         * @pre *n* no es nulo y es un nodo válido del árbol receptor.
         *
         * El árbol *tree* se inserta como hijo más a la izquierda del nodo *n*
         * del árbol receptor. El árbol *tree* queda vacío y los nodos que 
         * estaban en el subárbol hijo más a la izquierda de *n* se desplazan a 
         * la derecha, de forma que el anterior hijo más a la izquierda pasa a ser
         * el hermano a la derecha del nuevo hijo más a la izquierda.
         */
        void insertLeftChild(Node n, GeneralTree<T> & tree);
    
        /**
         * @brief Inserta el subárbol dado en el hermano derecha.
         * @param n Nodo al que se insertará el árbol *tree* como hermano a la derecha. 
         * @param tree Árbol que se insertará como hermano derecho.
         * @pre *n* no es nulo y es un nodo válido del árbol receptor
         *
         * El árbol *tree* se inserta como hermano derecho del nodo *n* del 
         * árbol receptor. El árbol *tree* queda vacío y los nodos que estaban a 
         * la derecha del nodo *n* pasan a la derecha del nuevo nodo.
         */
        void insertRightBrother(Node n, GeneralTree<T>& tree);
        
        /**
         * @brief Borra todos los elementos del árbol.
         *
         * Borra todos los elementos del árbol. 
         * La operación se realiza en tiempo O(n), donde *n* es el 
         * número de elementos del árbol.
         */
        inline void clear(){
            destroy(root);
            root = NULL;
        }
        
        /**
         * @brief Devuelve el número de elementos del árbol.
         *
         * La operación se realiza en tiempo O(n) llamando a **sizeP**.
         * @see sizeP
         */
        inline int size() const{
            return sizeP(root);
        }
        
        /**
         * @brief Indica si el árbol está vacío.
         *
         * La operación se realiza en tiempo O(1).
         */
        inline bool empty() const{
            return root == NULL;
        }
        
        /**
         * @brief Sobrecarga del operador de comparación.
         * @param other GeneralTree con el que se desea comparar.
         * @return Devuelve *true* si el árbol receptor tiene los mismos
         * elementos y en el mismo orden, *false* en caso contrario.
         *
         * La operación se realiza en tiempo O(n) utilizando **areEqual**.
         * @see areEqual
         */
        inline bool operator==(const GeneralTree<T>& other) const{
            return areEqual(root, other.root);
        }
        
        /**
         * @brief Sobrecarga del operador de comparación (diferencia)
         * @param other GeneralTree con el que se desea comparar.
         * @return Devuelve *true* si el árbol receptor no tiene los mismos 
         * elementos y en el mismo orden, *false* en caso contrario.
         *
         * La operación se realiza en tiempo O(n) utilizando **areEqual**.
         * @see areEqual
         */
        bool operator!=(const GeneralTree<T>& other) const{
            return ! areEqual(root, other.root);
        }
          
        /**
         * @brief Sobrecarga del operador de entrada.
         * @param in Stream de entrada.
         * @param other Árbol que se construye a partir de la lectura.
         * @return Referencia al stream de entrada.
         *
         * Lee de *in* un árbol y lo almacena en *other*. El formato aceptado para
         * la lectura se puede consultar en el método **printTree**.
         * @see readTree
         */
        friend istream& operator>>(istream & in, GeneralTree<T> & other){
            other.readTree(in, other.root, NULL);
            return in;
        }
        
        /**
         * @brief Sobrecarga del operador de salida.
         * @param out Stream de salida.
         * @param other Árbol que se imprime por out.
         * @return Referencia al stream de salida.
         *
         * Escribe en la salida todos los nodos del árbol *other* siguiendo un 
         * recorrido en preorden. El formato de impresión puede consultarse
         * en el método **printTree**.
         * @see printTree
         */
        friend ostream& operator<<(ostream & out, const GeneralTree<T> & other){
            other.printTree(out, other.root);
            return out;
        }

        /**
         * @brief Clase Iterator para el T.D.A. General Tree con recorrido en preorden.
         *
         * ### Descripción del tipo de dato abstracto ###
         *
         * Una instancia del T.D.A. Iterator proporciona la posibilidad de recorrer el árbol 
         * general asociado de raíz *root* en preorden.
         *
         * ### Información sobre la Implementación ###
         * 
         * La implementación se realiza mediante un puntero a un nodo (**template**) del árbol.
         * Se recorre la estructura mediante el operador ++ que se implementa actualizando
         * el puntero interno de forma que apunte al siguiente nodo según el criterio de preorden.
         *
         * @author Andrés Herrera Poyatos 
         * @date 23 de Diciembre de 2014 
         */
        class Iterator{
            private:
                /**
                 * @brief Puntero a un nodo del árbol.
                 *
                 * El funcionamiento interno del Iterador consiste en mover
                 * este puntero por los diferentes nodos del árbol.
                 */
                Node it;
                /**
                 * @brief Puntero a la raíz del árbol sobre el que se itera.
                 *
                 * Permite saber si dos iteradores iteran por el mismo árbol.
                 */
                Node root;

                /**
                 * @brief Nivel del nodo apuntado por *it*.
                 *
                 * La raíz (*root*) tiene nivel 0.
                 */
                int level;

            public:
                /**
                 * @brief Constructor por defecto.
                 */
                Iterator() : it(NULL), root(NULL), level(0)
                {}

                /**
                 * @brief Obtiene la etiqueta del nodo.
                 */
                inline T & operator*(){
                    return it->key;
                }

                /**
                 * @brief Obtiene el nodo actual.
                 */
                inline Node getNode() const{
                    return it;
                }

                /**
                 * @brief Obtiene el nivel del nodo actual.
                 */
                inline int getLevel() const{
                    return level;
                }
                  
                /**
                 * @brief El iterador pasa a apuntar al siguiente nodo según
                 * el criterio de preorden.
                 */
                Iterator & operator++();

                /**
                 * @brief Comprueba si dos iteradores son iguales.
                 * @param i Iterador con el que se compara.
                 * @return True si los dos iteradores son iguales (la raíz y el nodo son iguales). 
                 * False en caso contrario.
                 */
                inline bool operator==(const Iterator & i) const{
                    return root == i.root && it == i.it;
                }
                
                /**
                 * @brief Comprueba si dos iteradores son distintos.
                 * @param i Iterador con el que se compara.
                 * @return True si los dos iteradores son diferentes (la raíz o  el nodo son diferentes). 
                 * False en caso contrario.
                 */
                inline bool operator!=(const Iterator & i) const{
                    return root != i.root || it != i.it;
                }

                /**
                 * @brief Comprueba si el iterador es nulo o no.
                 */
                inline bool isNull() const{
                    return it == NULL;
                }
                
                friend class GeneralTree;
        };

        /**
         * @brief Clase ConstIterator para el T.D.A. General Tree con recorrido en preorden.
         *
         * ### Descripción del tipo de dato abstracto ###
         *
         * Una instancia del T.D.A. ConstIterator proporciona la posibilidad de recorrer el árbol 
         * general asociado de raíz *root* en preorden.
         *
         * ### Información sobre la Implementación ###
         * 
         * La implementación se realiza mediante un puntero a un nodo (**template**) del árbol.
         * Se recorre la estructura mediante el operador ++ que se implementa actualizando
         * el puntero interno de forma que apunte al siguiente nodo según el criterio de preorden.
         *
         * @author Andrés Herrera Poyatos 
         * @date 23 de Diciembre de 2014 
         */
        class ConstIterator{
            private:
                /**
                 * @brief Puntero a un nodo del árbol.
                 *
                 * El funcionamiento interno del Iterador consiste en mover
                 * este puntero por los diferentes nodos del árbol.
                 */
                Node it;
                /**
                 * @brief Puntero a la raíz del árbol sobre el que se itera.
                 *
                 * Permite saber si dos iteradores iteran por el mismo árbol.
                 */
                Node root;

                /**
                 * @brief Nivel del nodo apuntado por *it*.
                 *
                 * La raíz (*root*) tiene nivel 0.
                 */
                int level;

            public:
                /**
                 * @brief Constructor por defecto.
                 */
                ConstIterator() : it(NULL), root(NULL), level(0)
                {}

                /**
                 * @brief Obtiene la etiqueta del nodo.
                 */
                inline const T & operator*() const{
                    return it->key;
                }

                /**
                 * @brief Obtiene el nivel del nodo actual.
                 */
                inline int getLevel() const{
                    return level;
                }
                
                /**
                 * @brief Obtiene el nodo actual.
                 */
                inline const Node getNode() const{
                    return it;
                }

                /**
                 * @brief El iterador pasa a apuntar al siguiente nodo según
                 * el criterio de preorden.
                 */
                ConstIterator & operator++();

                /**
                 * @brief Comprueba si dos iteradores son iguales.
                 * @param i Iterador con el que se compara.
                 * @return True si los dos iteradores son iguales (la raíz y el nodo son iguales). False en caso contrario.
                 */
                inline bool operator==(const ConstIterator & i) const{
                    return root == i.root && it == i.it;
                }
                    
                /**
                 * @brief Comprueba si dos iteradores son distintos.
                 * @param i Iterador con el que se compara.
                 * @return True si los dos iteradores son diferentes (la raíz o  el nodo son diferentes). False en caso contrario.
                 */
                inline bool operator!=(const ConstIterator & i) const{
                    return root != i.root || it != i.it;
                }

                                /**
                 * @brief Comprueba si el iterador es nulo o no.
                 */
                inline bool isNull() const{
                    return it == NULL;
                }

                
                friend class GeneralTree;
        };
                 
        /**
         * @brief Devuelve un iterador apuntando a la raíz del árbol. Nivel 0.
         */
        inline Iterator begin(){
            Iterator begin;
            begin.it = begin.root = root;
            return begin;
        }
        
        /**
         * @brief Devuelve un iterador constante apuntando a la raíz del árbol. Nivel 0.
         */
        inline ConstIterator begin() const{
            ConstIterator begin;
            begin.it = begin.root = root;
            return begin;
        }
    
        /**
         * @brief Devuelve un iterador apuntando al nodo nulo. Nivel 0.
         */
        inline Iterator end(){
            Iterator end;
            end.it = NULL;
            end.root = root;
            return end;
        }
        
        /**
         * @brief Devuelve un iterador constante apuntando al nodo nulo. Nivel 0.
         */
        inline ConstIterator end() const{
            ConstIterator end;
            end.it = NULL;
            end.root = root;
            return end;
        }
    
        /**
         * @brief Devuelve un iterador al hijo del nodo *n* con clave *key*.
         * @param  n   Nodo del que se pretende encontrar un hijo con clave *key*.
         * @param  key Clave que se busca en los hijos de *n*.
         * @return Iterador al hijo en caso de que exista o end() es caso contrario.
         *
         * La búsqueda es lineal sobre la lista de hijos. Para mejorar este aspecto
         * los hijos deberían almacenarse en un árbol binario balanceado.
         */
        Iterator isChild(Node n, T key);
    
        /**
         * @brief Devuelve un iterador constante al hijo del nodo *n* con clave *key*.
         * @param  n   Nodo del que se pretende encontrar un hijo con clave *key*.
         * @param  key Clave que se busca en los hijos de *n*.
         * @return Iterador constante al hijo en caso de que exista o end() es caso contrario.
         *
         * La búsqueda es lineal sobre la lista de hijos. Para mejorar este aspecto
         * los hijos deberían almacenarse en un árbol binario balanceado.
         */
        ConstIterator isChild(Node n, T key) const;

};

# include "GeneralTree.cpp"

# endif
