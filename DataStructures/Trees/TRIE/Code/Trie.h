////////////////////////////////////////////////////////////
// Autor: Andrés Herrera Poyatos
// Universidad de Granada, 2º DGMII, Estructura de Datos
// Practica Final, Clase Trie, archivo .h
////////////////////////////////////////////////////////////

/**
 * @file Trie.h
 * @brief Fichero cabecera del TDA Trie.
 *
 * Gestiona una estructura de datos Trie (<http://en.wikipedia.org/wiki/Trie>) que 
 * consiste en un árbol general 
 * con facilidades para la inserción, búsqueda y borrado de elementos. Soporta 
 * además operaciones de búsqueda de elementos con características específicas.
 */

# ifndef TRIE_H
# define TRIE_H

# include <iostream>
# include <stdexcept> // Excepciones
# include <map>       // map
# include <vector>    // vector
# include "GeneralTree.h"

using namespace std;

/**
 * @brief T.D.A. Trie.
 * 
 * ### Descripción del tipo de dato abstracto ###
 *
 * Sea un conjunto *Tbase* cuyos elementos pueden representarse de 
 * forma unívoca como una sucesión, con soporte finito, de elementos del conjunto *Tnode*.
 * Se considera la aplicación \f$f: Tbase \times N \rightarrow Tnode\f$  que
 * proporciona, para cualquier pareja \f$(x,i)\f$ con \f$x \in Tbase\f$ y \f$i \in N\f$,
 * el \f$i\f$-ésima componente de la sucesión elementos del conjunto *Tnode* que 
 * caracteriza a \f$x\f$. Una instancia \f$\omega\f$ del tipo de dato abstracto Trie 
 * definido sobre los conjuntos anteriores consiste en un árbol general (de la clase
 * GeneralTree) sobre el dominio *pair<Tnode,bool>* en el que se insertan ramas que corresponden
 * a la representación en *Tnode* de los elementos de *Tbase* con el bool a false salvo
 * en el último elemento de la rama. Estas ramas comparten 
 * entre sí los prefijos comunes dentro de la estructura del árbol. Para más información 
 * ver <http://en.wikipedia.org/wiki/Trie>.
 * 
 * Un Trie soporta la inserción, borrado y búsqueda de elementos con eficiencia
 * igual a la máxima longitud de las representaciones en *Tnode* de los elementos de
 * *Tbase*. Por tanto, se recomienda su uso cuando esta longitud sea pequeña. Además,
 * puede soportar búsquedas de elementos de *Tbase* que tengan ciertas características
 * en relación a su representación en *Tnode*.
 *
 *
 * Ejemplos de Tries son los siguientes:
 *
 * - Trie en el que los nodos contienen caracteres (*Tnode*) que representan palabras (*Tbase*). 
 *   Bajo estos conjuntos, los Tries se pueden utilizar como diccionarios. A los elementos de *Tbase* 
 *   los denomino habitualmente *words* haciendo alusión a esta representación.
 * - Trie en el que los nodos contienen dígitos (*Tnode*) que representan números (*Tbase*).
 *   Se pueden utilizar para almacenar números con pocos dígitos así como una especie de
 *   radix sort.
 * - Trie en el que los nodos contienen bits (*Tnode*). Pueden representar cualquier información
 *   en binario. El árbol resultante es binario.
 *   
 * Para poder usar el tipo de dato Trie se debe incluir el fichero:
 * 
 * <tt>\#include Trie.h</tt>
 * 
 * El espacio requerido para el almacenamiento del Trie depende de los prefijos compartidos
 * por las representaciones en *Tnode*, siendo en el peor caso O(*nm*) donde *n* es el número
 * de elementos almácenados y *m* la longitud máxima de estas representaciones. 
 *
 * ### Información sobre la Implementación ###
 *
 * La implementación se realiza a partir de la clase GeneralTree. De esta forma se evita el manejo
 * de punteros explícitamente. La clase Trie es además template, lo que permite instanciarla en los
 * ejemplos anteriores. Además de indicarse como template las clases *Tbase* y *Tnode* se debe
 * indicar una clase *f* que contiene dos sobrecargas del operador ():
 *
 * **struct** f{
 * 
 *     int operator()(Tbase element, int i, Tnode & key);
 * 
 *     void operator()(Tbase &element, int i, Tnode key);
 *     
 *     void operator()(Tbase &element, int i);
 * 
 * }; 
 * 
 * La primera de ellas asigna a *key* la componente i-ésima de la representación en *Tnode* de *element*.
 * Devuelve -1 si era la última componente de la representación o i+1 en caso contrario.
 *
 * La segunda sobrecarga asigna *element* aquel elemento de *Tbase* que tiene la misma representación que
 * *element* salvo la i-ésima componente a la que se le asigna *key*.
 *
 * La tercera anula la i-ésima componente del elemento *element*.
 *
 * Esta estructura permite conocer las representaciones de *Tbase* en *Tnode* así como reconstruir sus
 * elementos a partir de los de *Tnode*. Un ejemplo de la misma se tiene en Dictionary.h .
 * 
 * @author Andrés Herrera Poyatos
 * @date 23 de diciembre de 2014
 */
template <class Tbase, class Tnode, class f>
class Trie{

    private:

        /**
         * @brief Estructura que representa un nodo del Trie.
         *
         * ### Descripción del tipo de dato abstracto ###
         *
         * Una instancia *c* del tipo de dato abstracto NodeTrie sobre un dominio *T* consiste en
         * un par formado por un elemento de *Tnode* y un *bool* que indica si el nodo actual es
         * el fin de la representación de un elemento de *Tbase* o no.
         *
         * ### Información sobre la Implementación ###
         *
         * Se implementa mediante un struct privado de la clase Trie. De esta forma solo
         * esta clase puede usar los nodos y sin ningún tipo de restricción. Se proporcionan
         * además dos posibles constructores así como sobrecargas de operadores.
         * 
         * @author Andrés Herrera Poyatos
         * @date 24 de Diciembre de 2014
         */
        struct NodeTrie {
            
            // ----------------------- Datos Miembro ----------------------- //
        
            /**
             *@brief Clave almacenada del tipo de dato *Tnode*.
             *
             * En este campo se almacena la clave que le corresponde a este nodo.
             */
            Tnode key;

            /**
             * @brief Bool que indica si *key* es el final de un elemento de *Tbase* o no.
             */
            bool is_end_of_word;
            
            // ------------------------ Constructores ------------------------ //
        
             /**
             * @brief Constructor por defecto.
             */
            NodeTrie() : is_end_of_word(false)
            {}

            /**
             * @brief Constructor con parámetros.
             * @param key Elemento de *Tnode* que se almacenará en el nodo.
             * @param is_end_of_word Bool que se asignará al dato miembro is_end_of_word.
             */
            NodeTrie(const Tnode & key, bool is_end_of_word): key(key), is_end_of_word(is_end_of_word)
            {}

            /**
             * @brief Sobrecarga del operador ==.
             *
             * Dos elementos de **NodeTrie** se consideran iguales en 
             * caso de serlo sus claves, independientemente de ser fin de
             * palabra o no.
             */
            bool operator==(const NodeTrie & other) const{
                return key == other.key;
            }

            /**
             * @brief Sobrecarga del operador <<.
             *
             * Al imprimir un nodo solo se hace para su clave.
             */
            friend ostream& operator<<(ostream & out, const NodeTrie & other){
                out << other.key;
            }

        };

        /**
         * @brief Árbol General que mantiene la estructura interna del Trie.
         */
        GeneralTree <NodeTrie> tree;

        /**
         * @brief Número de elementos de *Tbase* que contiene el árbol Trie.
         */
        int num_elements;

        /**
         * @brief Calcula de forma recursiva todos los elementos de *Tbase* longitud *lenght*. 
         * @param length    Longitud que deben tener las palabras a calcular.
         * @param solutions Elementos con longitud *length* calculados.
         * @param element   Elemento actual. Se modifica de forma recursiva.
         * @param n         Nodo actual.
         * @param level     Nivel de profundidad actual.
         */
        void elementsWithLength(int length, vector <Tbase> & solutions, Tbase element, typename GeneralTree<NodeTrie>::Node n, int level) const;

        /**
         * @brief Busca el elemento *element* de *Tbase* a partir del nodo *n* y lo elimina.
         * @param  element Elemento de *Tbase* a eliminar.
         * @param  n       Nodo que se considera como raíz a partir de la cual se busca *element*.
         * @return         Devuelve true si se ha encontrado y false en caso contrario.
         */
        bool erase(const Tbase & element, typename GeneralTree<NodeTrie>::Node n);

        /**
         * @brief Busca el elemento *element* de *Tbase* a partir del nodo *n*.
         * @param  element Elemento de *Tbase* a buscar.
         * @param  n       Nodo que se considera como raíz a partir de la cual se busca *element*.
         * @return         Devuelve true si se ha encontrado y false en caso contrario.
         */
        bool find(const Tbase & element, typename GeneralTree<NodeTrie>::Node n) const;

        /**
         * @brief Busca el elemento de *Tbase* contenido en el Trie con mayor puntuación 
         * dentro de los que contienen solo las claves dadas por *keys*.
         * @param element         Elemento de *Tbase* que va almacenando las claves de los nodos previos.
         * @param largest_element Par con los elementos con mayor puntuación y esta última. 
         * @param keys            map con las claves (su puntuación y el número de veces que se pueden repetir) que deben conformar 
         *  la representación de los candidatos. 
         * @param n               Nodo en el que se busca actualmente.
         * @param level           Nivel de profundidad en el árbol.
         *
         * La implementación es recursiva.
         * 
         * **Eficiencia**: O(tree.size() log(keys.size()) ). Habitualmente mucho menos. 
         */
        void highestScoredElement(pair<Tbase,int> element, pair<vector<Tbase>,int> &largest_element, map<Tnode,pair<int,int> > &keys , typename GeneralTree<NodeTrie>::Node n, int level) const;

        /**
         * @brief Inserta el elemento *element* de *Tbase* a partir del nodo *n*.
         * @param  element Elemento de *Tbase* a insertar.
         * @param  n       Nodo que se considera como raíz a partir de la cual se inserta *element*.
         */
        void insert(const Tbase & element, typename GeneralTree<NodeTrie>::Node n);

        /**
         * @brief Busca el elemento de *Tbase* contenido en el Trie cuya representación es 
         * la más larga dentro de las que contienen solo las claves dadas por *keys*.
         * @param element         Elemento de *Tbase* que va almacenando las claves de los nodos previos.
         * @param largest_element Par con los elementos más largos encontrados y su longitud. 
         * @param keys            map con las claves (y el número de veces que se pueden repetir) que deben conformar 
         *  la representación de los candidatos. 
         * @param n               Nodo en el que se busca actualmente.
         * @param level           Nivel de profundidad en el árbol.
         *
         * La implementación es recursiva.
         * 
         * **Eficiencia**: O(tree.size()). Habitualmente mucho menos. 
         */
        void largestElement(Tbase element, pair<vector<Tbase>,int> &largest_element, map<Tnode,int> &keys, typename GeneralTree<NodeTrie>::Node n, int level) const;

        /**
         * @brief Imprime de forma recursiva los elementos de *Tbase* contenidos en el Trie.
         * @param out     Flujo de salida.
         * @param element Elemento de *Tbase* que va almacenando las claves de los nodos previos.
         * @param n       Nodo actual.
         * @param level   Nivel de profundidad en el árbol.
         *
         * **Eficiencia**: O(tree.size())
         */
        void printElements(ostream & out, Tbase element, typename GeneralTree<NodeTrie>::Node n, int level) const;
        
    public:

        /**
         * @brief Constructor por defecto.
         *
         * Reserva los recursos e inicializa la raíz del Trie 
         * pues esta no se utiliza para insertar palabras. 
         * La operación se realiza en tiempo O(1).
         */
        Trie()
        {
            NodeTrie new_root;
            tree.setRoot(new_root);
            num_elements = 0;
        }

        /**
         * @brief Borra todos los elementos del Trie.
         *
         * Borra todos los elementos del árbol interno. 
         * La operación se realiza en tiempo O(n), donde *n* es el 
         * número de nodos de *tree*.
         */
        inline void clear(){
            tree.clear();
        }
        
        /**
         * @brief Indica si el árbol está vacío.
         *
         * La operación se realiza en tiempo O(1).
         */
        inline bool empty() const{
            // La raíz siempre está creada.
            // Se considera que el Trie está vacío cuando la
            // raíz no tiene hijos.
            return tree.leftChild(tree.getRoot()) == NULL;
        }

        /**
         * @brief Busca el elemento *element* de *Tbase* y lo elimina.
         * @param  element Elemento de *Tbase* a eliminar.
         * @return         Devuelve true si se ha encontrado y false en caso contrario.
         * 
         * Se llama a la versión privada de **erase**.
         * 
         * @see erase
         */
        bool erase(const Tbase & element);

        /**
         * @brief Busca el elemento *element* de *Tbase*.
         * @param  element Elemento de *Tbase* a buscar.
         * @return         Devuelve true si se ha encontrado y false en caso contrario.
         * 
         * Se llama a la versión privada de **find**.
         * 
         * @see find
         */
        bool find(const Tbase & element) const;

        /**
         * @brief Busca los elementos de *Tbase* contenidos en el Trie cuya representación es 
         * la más puntuada dentro de las que contienen solo las claves dadas por *keys*.
         * @param keys            map con las claves (su puntuación y el número de veces que se pueden repetir) 
         *                        que deben conformar la representación de los candidatos. 
         * @return Vector con los resultados.
         * Se llama a la versión privada de **highestScoredElement**.
         * 
         * **Eficiencia:** O(tree.size()). Habitualmente mucho menos. 
         * @see highestScoredElement
         */
        vector<Tbase> highestScoredElement(map<Tnode,pair<int,int> > &keys) const;

        /**
         * @brief Inserta el elemento *element* de *Tbase* a partir del nodo *n*.
         * @param  element Elemento de *Tbase* a insertar.
         *
         * Se llama a la versión privada de **insert**.
         *  
         * @see insert
         */
        void insert(const Tbase & element);

        /**
         * @brief Busca los elementos de *Tbase* contenidos en el Trie cuya representación es 
         * la más larga dentro de las que contienen solo las claves dadas por *keys*.
         * @param keys            map con las claves (y el número de veces que se pueden repetir) 
         *                        que deben conformar la representación de los candidatos. 
         * @return Vector con los resultados.
         * Se llama a la versión privada de **largestElement**.
         * 
         * **Eficiencia:** O(tree.size()). Habitualmente mucho menos. 
         * @see largestElement
         */
        vector<Tbase> largestElement(map<Tnode,int> &keys) const;

        /**
         * @brief Sobrecarga del operador de comparación.
         * @param other Trie con el que se desea comparar.
         * @return Devuelve *true* si el Trie receptor tiene los mismos
         * elementos y en el mismo orden, *false* en caso contrario.
         *
         * La operación se realiza en tiempo O(n) utilizando el operador de 
         * comparación de GeneralTree.
         */
        inline bool operator==(const Trie<Tbase, Tnode, f>& other) const{
            return tree == other.tree;
        }

        /**
         * @brief Devuelve el número de elementos de *Tbase* almacenados en el Trie.
         */
        inline int size() const{
            return num_elements;
        }

        /**
         * @brief Devuelve todos los elementos de longitud *length*.
         * @param Longitud de los elementos que se buscan.
         * @return Vector de elementos de *Tbase* con longitud *length*.
         */
        vector<Tbase> elementsWithLength(int length) const;

        /**
         * @brief Sobrecarga del operador de salida. Imprime todos los elementos insertados.
         * @param out Stream de salida.
         * @param other Trie cuyos elementos se imprimen por out.
         * @return Referencia al stream de salida.
         *
         * Llama al método recursivo **printElements**.
         *
         * @see printElements
         */
        friend ostream& operator<<(ostream & out, const Trie<Tbase, Tnode, f> & other){
            if(! other.empty() ){
//                // Se imprimen los elementos del subárbol de cada hijo de la raíz:
//                Tbase element;
//                for (typename GeneralTree<NodeTrie>::Node n = other.tree.leftChild(other.tree.getRoot()); n != NULL; n = other.tree.rightBrother(n)){
//                    other.printElements(out, element, n, 0);
//                }
                for (typename Trie<Tbase,Tnode,f>::Iterator it = other.begin(); it != other.end(); ++it){
                    out << *it << endl;
                }
            }
            return out;
        }

        /**
         * @brief Clase Iterator para el T.D.A. Trie.
         *
         * ### Descripción del tipo de dato abstracto ###
         *
         * Una instancia del T.D.A. Iterator proporciona la posibilidad de recorrer el trie 
         * asociado de forma que siempre apunte al final de un elemento de *Tbase* y pueda
         * devolverlo.
         *
         * ### Información sobre la Implementación ###
         *
         * La implementación se realiza utilizando los iteradores del GeneralTree.
         * El iterador debe apuntar siempre al final de una palabra.
         * Se recorre la estructura mediante el operador ++ que se implementa actualizando
         * el puntero iterador de forma que apunte a la siguiente palabra que contenga el Trie 
         * según el criterio de preorden para los nodos.
         *
         * @author Andrés Herrera Poyatos 
         * @date 28 de Diciembre de 2014 
         */
        class Iterator{
            private:
                /**
                 * @brief Iterador interno de la clase GeneralTree.
                 */
                typename GeneralTree<NodeTrie>::ConstIterator it;

                /**
                 * @brief Elemento de *Tbase* correspondiente a la posición actual del iterador.
                 */
                Tbase word;

            public:
                /**
                 * @brief Constructor por defecto.
                 */
                Iterator()
                {}

                /**
                 * @brief Obtiene la palabra asociada al nodo.
                 */
                inline const Tbase & operator*() const{
                    return word;
                }
                  
                /**
                 * @brief El iterador pasa a apuntar al siguiente nodo según
                 * el criterio de preorden.
                 */
                inline Iterator & operator++(){
                    int level = it.getLevel();
                    do{
                        ++it;
                        // Si se profundiza en el árbol se añade la clave correspondiente:
                        if (it.getLevel() > level){
                            f()(word, it.getLevel(), (*it).key );
                        }
                        else if (it.getLevel() > 0){ // Si se retrocede se eliminan claves y se asigna la nueva:
                            for (int i = level; i > it.getLevel(); i--){
                                f()(word, i);
                            }
                            f()(word, it.getLevel(), (*it).key);
                        }
                        level = it.getLevel();
                    }while ( level > 0 && ! (*it).is_end_of_word );

                    return *this;
                }

                /**
                 * @brief Comprueba si dos iteradores son iguales.
                 * @param i Iterador con el que se compara.
                 * @return True si los dos iteradores son iguales (sus iteradores internos son iguales). 
                 * False en caso contrario.
                 */
                inline bool operator==(const Iterator & i) const{
                    return it == i.it;
                }
                
                /**
                 * @brief Comprueba si dos iteradores son distintos.
                 * @param i Iterador con el que se compara.
                 * @return True si los dos iteradores son diferentes (sus iteradores internos son iguales). 
                 * False en caso contrario.
                 */
                inline bool operator!=(const Iterator & i) const{
                    return it != i.it;
                }

                friend class Trie;
        };

        /**
         * @brief Devuelve un iterador apuntando al primer elemento del Trie..
         */
        inline Iterator begin() const{
            Iterator begin;
            begin.it = tree.begin();
            ++begin;
            return begin;
        }
            
        /**
         * @brief Devuelve un iterador apuntando al nodo nulo.
         */
        inline Iterator end() const{
            Iterator end;
            end.it = tree.end();
            return end;
        }
};

# include "Trie.cpp"

# endif
