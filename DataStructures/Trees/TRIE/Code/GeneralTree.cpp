////////////////////////////////////////////////////////////
// Autor: Andrés Herrera Poyatos
// Universidad de Granada, 2º DGMII, Estructura de Datos
// Practica Final, Clase GeneralTree, archivo .cpp
////////////////////////////////////////////////////////////

/**
 * @file GeneralTree.cpp
 * @brief Implementación del TDA GeneralTree.
 *
 * Para una mayor descripción ver "GeneralTree.h".
 */

////////////////////////////* MÉTODOS PRIVADOS *///////////////////////////////

/*______________________________ destroy ______________________________ */

template <class T>
void GeneralTree<T>::destroy(NodeP * n){
    if(n != NULL){
        destroy(n->leftc);
        destroy(n->rightb);
        delete n;
    }
}

/*________________________________ copy ______________________________ */

template <class T>
void GeneralTree<T>::copy(NodeP * origin, NodeP *& destination, NodeP * parent){
    destination = new NodeP(origin->key, NULL, NULL, parent);

    if (origin->rightb != NULL){
        copy(origin->rightb, destination->rightb, parent);
    }

    if (origin->leftc != NULL){
        copy(origin->leftc, destination->leftc, destination);
    }
}

/*______________________________ sizeP ______________________________ */

template <class T>
int GeneralTree<T>::sizeP(const NodeP * n) const{
    int size = 1;
    for (NodeP* hijo = n->leftc; hijo != NULL; hijo = hijo->rightb){
        size += sizeP(hijo);
    }
    return size;
}

/*_______________________________ areEqual _____________________________ */

template <class T>
bool GeneralTree<T>::areEqual(const NodeP * n1, const NodeP * n2) const{
    return (n1 == n2) ? true : (n1->key == n2->key) && areEqual(n1->rightb, n2->rightb) && areEqual(n1->leftc, n2->leftc);
}

/*________________________________ printTree ____________________________ */

template <class T>
void GeneralTree<T>::printTree(std::ostream & out, NodeP * n) const{
    if (n == NULL){
        out << 'x';
    }
    else{
        out << "n " << n->key;
        printTree(out, n->leftc);
        printTree(out, n->rightb);
    }
}

/*________________________________ readTree ______________________________ */

template <class T>
void GeneralTree<T>::readTree(std::istream& in, NodeP * & n, NodeP * parent){
    char ch;
    in >> ch;
    
    if (ch == 'x'){
        n = NULL;
    }
    else if (ch == 'n'){
        in >> ch;
        T key;
        in >> key;
        n = new NodeP(key, NULL, NULL, parent);
        readTree(in, n->leftc, n);
        readTree(in, n->rightb, parent);
    }
    else{
        throw runtime_error("El formato del árbol leido es incorrecto");
    }
}

/*__________________________________________________________________________ */

////////////////////////////* MÉTODOS PÚBLICOS *///////////////////////////////
    
/*__________________________ Operador de Asignación __________________________ */

template <class T>
GeneralTree<T>& GeneralTree<T>::operator=(const GeneralTree<T> & other){
    destroy(root);
    copy(other.root, root, NULL);
    return this;
}

/*__________________________ pruneSubtree __________________________ */
    
template <class T>
void GeneralTree<T>::pruneSubtree(Node n, GeneralTree<T> & destination){
    if(n != NULL){
        if (parent(n) != NULL){
            if (leftChild(parent(n)) != n){
                NodeP * m;
                for(m = leftChild(parent(n)); n != rightBrother(m); m = rightBrother(m));
                rightBrother(m) = rightBrother(n);
            }
            else{
                leftChild(parent(n)) = rightBrother(n);
            }
        }
        n->parent = n->rightb = NULL;
        destination.clear();
        destination.root = n;
    }
}

/*__________________________ pruneLeftChild __________________________ */
    
template <class T>
void GeneralTree<T>::pruneLeftChild(Node n, GeneralTree<T> & destination){
    if (n->leftc != NULL){
        NodeP *left = n->leftc->rightb;
        destination.root = n->leftc;
        n->leftc = left;
    }
}
    
/*__________________________ pruneRightBrother __________________________ */

template <class T>
void GeneralTree<T>::pruneRightBrother(Node n, GeneralTree<T> & destination){
    if (n->rightb != NULL){
        NodeP *right = n->right->rightb;
        destination.root = n->right;
        n->rightb = right;
    }
}

/*__________________________ insertLeftChild __________________________ */

template <class T>
void GeneralTree<T>::insertLeftChild(Node n, GeneralTree<T> & tree){
    NodeP *right = n->leftc;
    NodeP *iter = n->leftc = tree.getRoot();
    n->leftc->parent = n;

    while(iter->rightb != NULL){
        iter = iter->rightb;
    }

    iter->rightb = right;

    tree.root = NULL;
}
    
/*__________________________ insertRightBrother __________________________ */

template <class T>
void GeneralTree<T>::insertRightBrother(Node n, GeneralTree<T> & tree){
    NodeP *right = n->rightb;
    NodeP *iter = n->rightb = tree.getRoot();
    n->rightb->parent = n->parent;

    while(iter->rightb != NULL){
        iter = iter->rightb;
    }

    iter->rightb = right;

    tree.root = NULL;
}

/*_______________________________ isChild _______________________________ */

template <class T>
typename GeneralTree<T>::Iterator GeneralTree<T>::isChild(Node n, T key){
    Node child = leftChild(n);
    bool is_child = false;

    // Búsqueda lineal sobre los hijos:
    while(child != NULL && ! is_child){
        if (this->key(child) == key){
            is_child = true;
        }
        else{
            child = rightBrother(child);
        }
    }

    Iterator it_child;
    it_child.it = child;
    it_child.root = root;
    return it_child;
}

// Versión con iterador constante:

template <class T>
typename GeneralTree<T>::ConstIterator GeneralTree<T>::isChild(Node n, T key) const{
    Node child = leftChild(n);
    bool is_child = false;

    // Búsqueda lineal sobre los hijos:
    while(child != NULL && ! is_child){
        if (this->key(child) == key){
            is_child = true;
        }
        else{
            child = rightBrother(child);
        }
    }

    ConstIterator it_child;
    it_child.it = child;
    it_child.root = root;
    return it_child;
}

/*__________________________________________________________________________ */

///////////////////////////////* CLASE ITERADOR *//////////////////////////////////

/*_______________________________ Sobrecarga del operador ++ _______________________________ */

template <class T>
typename GeneralTree<T>::Iterator & GeneralTree<T>::Iterator::operator++(){
    if (it != NULL){
        if (it->leftc != NULL){ // Si hay un hijo a la izquierda se mueve a él.
            it = it->leftc;
            level++;
        }
        else if (it->rightb != NULL){ // Else Si hay un hermano a la derecha se mueve a él.
            it = it->rightb;
        }
        else{  // Else se mueve al hermano a la derecha del primer padre que lo tenga.
            while(it != NULL && it->rightb == NULL){ 
                it = it->parent;
                level--;
            }
            it = it != NULL ? it->rightb : NULL; // Si it == NULL ya se ha recorrido el árbol.               
        }                        
    }
    else{
        it = root; // El recorrido es cíclico.
    }
    return *this;
}

/*_______________________________ Sobrecarga del operador ++ _______________________________ */
// Versión Constante:

template <class T>
typename GeneralTree<T>::ConstIterator & GeneralTree<T>::ConstIterator::operator++(){
    if (it != NULL){
        if (it->leftc != NULL){ // Si hay un hijo a la izquierda se mueve a él.
            it = it->leftc;
            level++;
        }
        else if (it->rightb != NULL){ // Else Si hay un hermano a la derecha se mueve a él.
            it = it->rightb;
        }
        else{  // Else se mueve al hermano a la derecha del primer padre que lo tenga.
            while(it != NULL && it->rightb == NULL){ 
                it = it->parent;
                level--;
            }
            it = it != NULL ? it->rightb : NULL; // Si it == NULL ya se ha recorrido el árbol.               
        }                        
    }
    else{
        it = root; // El recorrido es cíclico.
    }

    return *this;
}

/*___________________________________________________________________________________________ */
