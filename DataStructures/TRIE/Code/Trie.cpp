////////////////////////////////////////////////////////////
// Autor: Andrés Herrera Poyatos
// Universidad de Granada, 2º DGMII, Estructura de Datos
// Practica Final, Clase Trie, archivo .cpp
////////////////////////////////////////////////////////////

/**
 * @file Trie.cpp
 * @brief Implementación del TDA Trie.
 *
 * Para una mayor descripción ver "Trie.h".
 */

# include "Trie.h"

////////////////////////////* MÉTODOS PRIVADOS *///////////////////////////////


/*______________________________ elementsWithLength ______________________________ */

template <class Tbase, class Tnode, class f>
void Trie<Tbase, Tnode, f>::elementsWithLength(int length, vector <Tbase> & solutions, Tbase element, typename GeneralTree<NodeTrie>::Node n, int level) const {
    f()(element, level, tree.key(n).key);
    level++;
    if (level < length){
        for (n = tree.leftChild(n); n != NULL; n = tree.rightBrother(n)){
            elementsWithLength(length, solutions, element, n, level);
        }
    }
    else if (tree.key(n).is_end_of_word){
        solutions.push_back(element);
    }
}

/*__________________________________ erase ___________________________________ */

template <class Tbase, class Tnode, class f>
bool Trie<Tbase, Tnode, f>::erase(const Tbase & element, typename GeneralTree<NodeTrie>::Node n){
    int i = 0;
    NodeTrie key;
    typename GeneralTree<NodeTrie>::Iterator it;
    bool Tnode_found = true;
    typename GeneralTree<NodeTrie>::Node aux;
    GeneralTree<NodeTrie> other;
    
    while( Tnode_found &&  (i = f()(element, i, key.key)) != -1 ){
        if ( (it = tree.isChild(n, key)) != tree.end() ){
            n = it.getNode();
        }
        else{
            Tnode_found = false;
        }
    }

    Tnode_found = Tnode_found ? (tree.key(n)).is_end_of_word : false; 
    
    if ( Tnode_found ){
        (tree.key(n)).is_end_of_word = false;
        while(tree.leftChild(n) == NULL &&  ! (tree.key(n)).is_end_of_word && tree.parent(n) != NULL){
            aux = tree.parent(n);
            tree.pruneSubtree(n, other);
            n = aux;
        }
    }

    return Tnode_found;
}

/*__________________________________ find ___________________________________ */

template <class Tbase, class Tnode, class f>
bool Trie<Tbase, Tnode, f>::find(const Tbase & element, typename GeneralTree<NodeTrie>::Node n) const{
    int i = 0;
    NodeTrie key;
    typename GeneralTree<NodeTrie>::ConstIterator it;
    bool Tnode_found = true;

    while( Tnode_found &&  (i = f()(element, i, key.key)) != -1 ){
        if ( (it = tree.isChild(n, key)) != tree.end() ){
            n = it.getNode();
        }
        else{
            Tnode_found = false;
        }
    }

    return Tnode_found && (*it).is_end_of_word;
}

/*______________________________ highestScoredElement ______________________________ */

template <class Tbase, class Tnode, class f>
void Trie<Tbase, Tnode, f>::highestScoredElement(pair<Tbase, int> element, pair<vector<Tbase>,int> &highest_scored, map<Tnode,pair<int,int> > &keys, typename GeneralTree<NodeTrie>::Node n, int level) const{

    typename map<Tnode,pair<int,int> >::iterator current_key;

    if ( (current_key = keys.find(tree.key(n).key)) != keys.end() && current_key->second.second > 0 ){ // Si la clave actual está libre en keys:

        current_key->second.second--;                  // Se bloquea
        f()(element.first, level, tree.key(n).key);    // Se añade a element
        element.second += current_key->second.first;   // Se suma su puntuación

        if (tree.key(n).is_end_of_word){               // Si element es una palabra:
            if (highest_scored.second < element.second){            // - Si tiene mayor puntuación que las
                highest_scored.first.clear();                       //   palabras guardadas las sustituye.
                highest_scored.first.push_back(element.first);
                highest_scored.second = element.second;
            }
            else if (highest_scored.second == element.second){      // - Si tiene la misma puntuación se añade.
                highest_scored.first.push_back(element.first);
            }  
        } 

        // Se llama recursivamente a highestScoredElement por cada hijo de n:
        level++;
        for (n = tree.leftChild(n); n != NULL; n = tree.rightBrother(n)){
            highestScoredElement(element, highest_scored, keys, n, level);        
        }

        current_key->second.second++;                // Se libera la clave
    }
}

/*_________________________________ insert _________________________________ */

template <class Tbase, class Tnode, class f>
void Trie<Tbase, Tnode, f>::insert(const Tbase & element, typename GeneralTree<NodeTrie>::Node n){
    int i = 0;
    NodeTrie key;
    typename GeneralTree<NodeTrie>::Iterator it;
    bool Tnode_found = true;
    
    while( Tnode_found && (i = f()(element, i, key.key)) != -1 ){
        if ( (it = tree.isChild(n, key)) != tree.end() ){
            n = it.getNode();
        }
        else{
            Tnode_found = false;
            i--;
        }
    }

    GeneralTree<NodeTrie> aux;
    while((i = f()(element, i, key.key)) != -1){
        aux.setRoot(key);
        tree.insertLeftChild(n, aux);
        n = tree.leftChild(n);
    }

    tree.key(n).is_end_of_word = true;
}

/*______________________________ largestElement ______________________________ */

template <class Tbase, class Tnode, class f>
void Trie<Tbase, Tnode, f>::largestElement(Tbase element, pair<vector<Tbase>,int> &largest_element, map<Tnode,int> &keys, typename GeneralTree<NodeTrie>::Node n, int level) const{

    typename map<Tnode,int>::iterator current_key;

    if ( (current_key = keys.find(tree.key(n).key)) != keys.end() && current_key->second > 0 ){ // Si la clave actual está libre en keys:

        current_key->second--;                              // Se bloquea
        f()(element, level, tree.key(n).key);               // Se añade a element
    
        if (tree.key(n).is_end_of_word){                    // Si element es una palabra:
            if (largest_element.second < level){            // - Si tiene mayor longitud que las
                largest_element.first.clear();              //   palabras guardadas las sustituye.
                largest_element.first.push_back(element);
                largest_element.second = level;
            }
            else if (largest_element.second == level){      // - Si tiene la misma longitud se añade.
                largest_element.first.push_back(element);
            }  
        } 

        // Se llama recursivamente a largestElement por cada hijo de n:
        level++;
        for (n = tree.leftChild(n); n != NULL; n = tree.rightBrother(n)){
            largestElement(element, largest_element, keys, n, level);        
        }

        current_key->second++;                              // Se desbloquea la clave
    }
}

/*______________________________ printElements ______________________________ */

template <class Tbase, class Tnode, class f>
void Trie<Tbase, Tnode, f>::printElements(ostream & out, Tbase element, typename GeneralTree<NodeTrie>::Node n, int level) const{
    f()(element, level, tree.key(n).key);
    if (tree.key(n).is_end_of_word){
        out << element << endl;
    }
    level++;
    for (n = tree.leftChild(n); n != NULL; n = tree.rightBrother(n)){
        printElements(out, element, n, level);
    }
}
        
/*___________________________________________________________________________________ */

////////////////////////////* MÉTODOS PÚBLICOS *///////////////////////////////

/*______________________________ elementsWithLength ______________________________ */

template <class Tbase, class Tnode, class f>
vector<Tbase> Trie<Tbase, Tnode, f>::elementsWithLength(int length) const{
    Tbase element;
    vector <Tbase> solutions;

    for (typename GeneralTree<NodeTrie>::Node n = tree.leftChild(tree.getRoot()); n != NULL; n = tree.rightBrother(n)){
        elementsWithLength(length, solutions, element, n, 0);
    }

    return solutions;
}

/*_______________________________ erase _______________________________ */

template <class Tbase, class Tnode, class f>
bool Trie<Tbase, Tnode, f>::erase(const Tbase & element){
    return erase(element, tree.getRoot());
}

/*_______________________________ find _______________________________ */

template <class Tbase, class Tnode, class f>
bool Trie<Tbase, Tnode, f>::find(const Tbase & element) const{
    return find(element, tree.getRoot());
}

/*_______________________________ highestScoredElement _______________________________ */

template <class Tbase, class Tnode, class f>
vector<Tbase> Trie<Tbase, Tnode, f>::highestScoredElement(map<Tnode,pair<int,int> > &keys) const{
    if(! empty() ){
        if (! keys.empty() ){
            
            pair<Tbase,int> element;
            element.second = 0;
            pair<vector<Tbase>,int> highest_scored;
            highest_scored.second = -1;
    
            for (typename GeneralTree<NodeTrie>::Node n = tree.leftChild(tree.getRoot()); n != NULL; n = tree.rightBrother(n)){
                highestScoredElement(element, highest_scored, keys, n, 0);
            }

            return highest_scored.first;
        }
        else{
            throw runtime_error("Trie: highestScoredElement: No se han proporcionado claves.");           
        }
    }
    else{
        throw runtime_error("Trie: highestScoredElement: El árbol está vacío.");
    }
}

/*_______________________________ insert _______________________________ */

template <class Tbase, class Tnode, class f>
void Trie<Tbase, Tnode, f>::insert(const Tbase & element){
    insert(element, tree.getRoot());    
    num_elements++;    
}

/*_______________________________ largestElement _______________________________ */

template <class Tbase, class Tnode, class f>
vector<Tbase> Trie<Tbase, Tnode, f>::largestElement(map<Tnode,int> &keys) const{
    if(! empty() ){
        if (! keys.empty() ){
            Tbase element;
            pair<vector<Tbase>,int> largest_element;
            largest_element.second = -1;
    
            for (typename GeneralTree<NodeTrie>::Node n = tree.leftChild(tree.getRoot()); n != NULL; n = tree.rightBrother(n)){
                largestElement(element, largest_element, keys, n, 0);
            }

            return largest_element.first;
        }
        else{
            throw runtime_error("Trie: largestElement: No se han proporcionado claves.");           
        }
    }
    else{
        throw runtime_error("Trie: largestElement: El árbol está vacío.");
    }
}

/*__________________________________________________________________________ */

