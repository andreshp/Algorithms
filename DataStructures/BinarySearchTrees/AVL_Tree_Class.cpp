///////////////////////////////////
//      AVL Tree Simple Class
// Author: Andrés Herrera Poyatos
////////////////////////////////////

# include <iostream>
# include <cstdio>
# include <sstream>
# include <algorithm>
# include <queue>
# include <string>

using namespace std;

/*
 * Node Declaration
 */
struct Node{
    int key, height;
    struct Node *left;
    struct Node *right;
    Node() : key(0), height(0), left(NULL), right(NULL)
    {}
};

/*
 * Class Declaration
 */
class AVLTree{
    private:
        // Pointer to the tree root
        Node* root;
        // Insertion recursive method
        Node* insert(Node *, int );
        void destroyTree(Node *);
        // Rotation methods:
        Node *rrRotation(Node *);
        Node *llRotation(Node *);
        Node *lrRotation(Node *);
        Node *rlRotation(Node *);
        Node* balance(Node *);
        // Display methods:
        void display(Node *, int);
        void inorder(Node *);
        void preorder(Node *);
        void postorder(Node *);
        // Save and Load methods:
        void printStructure(ostream &, Node *);
        void readTree(istream &, Node* &);
        void readStructure(istream &, Node* &);
        void buildStructure(Node* &, vector<unsigned int>&, int );
        void readKeys(istream &, Node* );

    public:
        AVLTree()
        {
            root = NULL;
        }
        ~AVLTree()
        {
            destroyTree(root);
        }
        inline void destroyTree(){
            if (root != NULL){
                destroyTree(root);
                root = NULL;            
            }
        }
        // Height of an AVL Tree node:
        inline int height(Node *n)
        {
            if (n != NULL)
                return n->height;
            else
                return 0;
        }
        // Difference between the n children heights:
        inline int heightDiff(Node *n)
        {
            return height(n->left) - height(n->right);
        }
        inline bool isEmpty()
        {
            return (root == NULL);
        } 
        // Public Insertion Method:
        inline Node* insert(int key)
        {
            root = insert(root, key);
        }
        // Min and Max values in the tree:
        int minValue();
        int maxValue();
        // Public Display Methods:
        inline void display()
        {
            display(root, 1);
        }
        inline void inorder()
        {
            inorder(root);
        }
        inline void preorder()
        {
            preorder(root);
        }
        inline void postorder()
        {
            postorder(root);
        }
        // Save structure:
        inline void printStructure(ostream &out)
        {
            printStructure(out, root);
        }
        // Read Tree:
        inline void readTree(istream &in){
            readTree(in, root);
        }
};

// Destroying the tree
void AVLTree::destroyTree(Node *n)
{
    if(n != NULL)
    {
        destroyTree(n->left);
        destroyTree(n->right);
        delete n;
    }
}  
 
// Right- Right Rotation
Node *AVLTree::rrRotation(Node *parent)
{
    Node *temp = parent->right;
    
    parent->right = temp->left;
    temp->left = parent;
    
    //  Update heights
    parent->height = max(height(parent->left), height(parent->right))+1;
    temp->height = max(height(temp->left), height(temp->right))+1;

    return temp;
}

// Left- Left Rotation
Node *AVLTree::llRotation(Node *parent)
{
    Node *temp = parent->left;
    
    parent->left = temp->right;
    temp->right = parent;
    
    //  Update heights
    parent->height = max(height(parent->left), height(parent->right))+1;
    temp->height = max(height(temp->left), height(temp->right))+1;

    return temp;
}
 
// Left - Right Rotation
Node *AVLTree::lrRotation(Node *parent)
{
    Node *temp;
    temp = parent->left;
    parent->left = rrRotation (temp);
    return llRotation (parent);
}
 
// Right- Left Rotation
Node *AVLTree::rlRotation(Node *parent)
{
    Node *temp;
    temp = parent->right;
    parent->right = llRotation (temp);
    return rrRotation (parent);
}
 
// Balancing AVL Tree
Node *AVLTree::balance(Node *temp)
{
    int bal_factor = heightDiff (temp);
    if (bal_factor > 1)
    {
        if (heightDiff(temp->left) > 0)
            temp = llRotation (temp);
        else
            temp = lrRotation (temp);
    }
    else if (bal_factor < -1)
    {
        if (heightDiff(temp->right) > 0)
            temp = rlRotation (temp);
        else
            temp = rrRotation (temp);
    }
    return temp;
}
 
// Insert Element into the tree
Node *AVLTree::insert(Node *n, int value)
{
    if (n == NULL)
    {
        n = new Node;
        n->key = value;
        n->height = 1;
        return n;
    }
    else if (value < n->key)
    {
        n->left = insert(n->left, value);
        n->height = max(height(n->left), height(n->right))+1;
        n = balance (n);
    }
    else if (value >= n->key)
    {
        n->right = insert(n->right, value);
        n->height = max(height(n->left), height(n->right))+1;
        n = balance (n);
    }
    return n;
}

// Min and Max values in the tree:
int AVLTree::minValue()
{
    if (isEmpty())
        return 0;
    else
    {
        Node* n = root;
        while(n->left != NULL)
        {
            n = n->left;
        }
        return n->key;
    }
}
int AVLTree::maxValue()
{
    if (isEmpty())
        return 0;
    else
    {
        Node* n = root;
        while(n->right != NULL)
        {
            n = n->right;
        }
        return n->key;
    }
}


// Display AVL Tree
void AVLTree::display(Node *ptr, int level)
{
    int i;
    if (ptr!=NULL)
    {
        display(ptr->right, level + 1);
        printf("\n");
        if (ptr == root)
            cout<<"Root -> ";
        for (i = 0; i < level && ptr != root; i++)
            cout<<"        ";
        cout<<ptr->key;
        display(ptr->left, level + 1);
    }
}
 
// Inorder Traversal of AVL Tree
void AVLTree::inorder(Node *n)
{
    if (n != NULL)
    {
        inorder (n->left);
        cout<<n->key<<"  ";
        inorder (n->right);
    }
    
}

//Preorder Traversal of AVL Tree
void AVLTree::preorder(Node *n)
{
    if (n != NULL)
    {
        cout<<n->key<<"  ";
        preorder (n->left);
        preorder (n->right);
    } 
}
 
// Postorder Traversal of AVL Tree
void AVLTree::postorder(Node *n)
{
    if (n == NULL)
    {
        postorder ( n ->left );
        postorder ( n ->right );
        cout<<n->key<<"  ";
    }
}

// Structure of the AVL Tree. Blocks of 32 bits are printed.
void AVLTree::printStructure(ostream &out, Node* root){
    queue<Node*> q;
    Node *temp_node = root; 
    int num_nodes = 0, total_nodes =  (1 << (height(root))) - 1;
    int bits_number = 0;
    unsigned int bits32 = 0;
    while(num_nodes <= total_nodes){
        bits32 += (temp_node != NULL? 1 : 0) << bits_number;
        bits_number++; num_nodes++;

        if (bits_number == 32){ // Se imprimen bits de 32 en 32
            out << bits32 << " ";
            bits32 = 0; bits_number = 0;          
        }

        if(temp_node != NULL){
            q.push(temp_node->left); q.push(temp_node->right);
        }
        else if (num_nodes <= total_nodes / 2){
            q.push(NULL); q.push(NULL);
        }
        
        temp_node = q.front(); q.pop();
    }
    out << (bits32 == 0? : bits32) << " " << 'x' << " ";
}

// A tree is read in root:
void AVLTree::readTree(istream &in, Node* &root){
    readStructure(in, root); // First structure is read
    if (root != NULL)
        readKeys(in, root); // Last keys are read
}

// A structure is read in root:
void AVLTree::readStructure(istream &in, Node* &root){
    vector<unsigned int> structure;
    string word;
    in >> word;
    while(word[0] != 'x'){
        structure.push_back(atoi(word.c_str()));
        in >> word;
    }
    buildStructure(root, structure, 0);
}

// A structure given by the vector is built recursively:
void AVLTree::buildStructure(Node* &n, vector<unsigned int> &structure, int pos){
    int index = pos / 32, bit = pos % 32;
    if (structure[index] & (1<<bit)){
        n = new Node;
        buildStructure(n->left, structure, 2*pos+1);
        buildStructure(n->right, structure, 2*pos+2);
    }
}

// Keys are read in preorden and asigned to the tree:
void AVLTree::readKeys(istream &in, Node* n){
    in >> n->key;
    if (n->left != NULL)
        readKeys(in, n->left);
    if (n->right != NULL)
        readKeys(in, n->right);
}

/*
 * Main Program. Works with a menu.
 */
int main(){
    int choice, item;
    AVLTree avl;
    while (1)
    {
        cout << "\n--------------------------" << endl;
        cout << "Ejemplo de un AVL Tree" << endl;
        cout << "---------------------------" << endl;
        cout << "1. Inserta un elemento en el árbol" << endl;
        cout << "2. Ver AVL Tree " << endl;
        cout << "3. Inorden del árbol" << endl;
        cout << "4. Preorden del árbol" << endl;
        cout << "5. Postorden del árbol" << endl;
        cout << "6. Obtener código de guardado" << endl;
        cout << "7. Leer mediante un código de la opción 6" << endl;
        cout << "8. Salir" << endl;
        cout << "Introduzca la opción deseada: ";
        cin >> choice;
        switch(choice)
        {
        case 1:
            cout << "Introduzca un entero positivo a insertar: ";
            cin >> item;
            avl.insert(item);
            break;
        case 2:
            if (avl.isEmpty())
            {
                cout<<"El árbol está vacío" << endl;
            }
            else
            {
                cout<<"AVL Tree:" << endl;
                avl.display();
            }
            break;
        case 3:
            cout<<"Inorden del árbol:" << endl;
            avl.inorder();
            cout << endl;
            break;
        case 4:
            cout<<"Preorden del árbol:" << endl;
            avl.preorder();
            cout << endl;
            break;
        case 5:
            cout<<"Postorden del árbol:" << endl;
            avl.postorder();    
            cout << endl;
            break;
        case 6:
            cout<<"Código que representa al árbol: ";
            avl.printStructure(cout);
            avl.preorder();
            cout << endl;
            break;
        case 7:
            cout<<"Introduzca su código: ";
            avl.destroyTree();
            avl.readTree(cin);
            break;
        case 8:
            exit(1);    
            break;
        default:
            cout<<"Opción errónea" << endl;
        }
    }
    return 0;
}