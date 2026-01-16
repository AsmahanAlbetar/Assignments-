#include <vector>
#include <iostream>
#include <algorithm>
#include <queue>
#include <cmath>
#include <cstdio>
using namespace std;
struct treeNodeID {
    int ID;
    treeNodeID* leftChild;
    treeNodeID* rightChild;
    treeNodeID(int id) : ID(id), leftChild(NULL), rightChild(NULL) {}
};
struct treeNodeBST {
    int depID;
    treeNodeID* rootID;
    treeNodeBST* leftChild;
    treeNodeBST* rightChild;
    treeNodeBST(int DEPID) : depID(DEPID), rootID(NULL), leftChild(NULL), rightChild(NULL) {}
};
treeNodeID* buildID(treeNodeID* root, int ID) {
    if (root == NULL) return new treeNodeID(ID);
    if (root->ID > ID)
        root->leftChild = buildID(root->leftChild, ID);
    if (root->ID < ID)
        root->rightChild = buildID(root->rightChild, ID);
    return root;

}

treeNodeBST* buildBST(int dep, int ID, treeNodeBST* root) {
    if (!root) {
        treeNodeBST* node = new treeNodeBST(dep);
        node->rootID = buildID(node->rootID, ID);
        return node;
    }

    if (root->depID > dep) {
        root->leftChild = buildBST(dep, ID, root->leftChild);
    }
    else if (root->depID < dep) {
        root->rightChild = buildBST(dep, ID, root->rightChild);
    }
    else
        root->rootID = buildID(root->rootID, ID);
    //if root->depID == dep
    return root;
}

void foundID(treeNodeID* startnode, int& visitedNode, int& found, int const ID) {
    if (!startnode) {
        found = 0;
        return;
    }
    ++visitedNode;
    if (startnode->ID == ID) {
        found = 1;
        return;
    }
    else if (startnode->ID > ID)
        foundID(startnode->leftChild, visitedNode, found, ID);
    else
        foundID(startnode->rightChild, visitedNode, found, ID);


}
void foundDep(treeNodeBST* startNode, int& visitedNode, int& found, const int& dep, const int& ID) {
    if (!startNode) {
        //visitedNode = 0;
        found = 0;
        return;
    }
    ++visitedNode;
    if (startNode->depID == dep)
        foundID(startNode->rootID, visitedNode, found, ID);
    else if (startNode->depID > dep)
        foundDep(startNode->leftChild, visitedNode, found, dep, ID);
    else
        foundDep(startNode->rightChild, visitedNode, found, dep, ID);



}
pair<int, bool> searchQuery(treeNodeBST* root, int depKey, int ID) {
    int visited = 0;
    int found = 0;
    foundDep(root, visited, found, depKey, ID);
    return { visited,found };
}

int main() {

    int N;
    int Q;
    cin >> N >> Q;
    vector < pair<int, int >> depIDPair;
    int depID;
    int ID;
    for (int i = 0; i < N; ++i) {

        cin >> depID >> ID;
        depIDPair.push_back({ depID, ID });
    }

    treeNodeBST* rootBST = NULL;
    for (auto& node : depIDPair) {
        rootBST = buildBST(node.first, node.second, rootBST);
    }
    for (int i = 0; i < Q; i++) {
        cin >> depID >> ID;
        auto results = searchQuery(rootBST, depID, ID);
        cout << results.first << " " << results.second << "\n";
        // if (results.second){
        //     cout << results.first << " " << "1" << "\n";
        // }
        // cout << results.first << " " << "0" << "\n";
    }
    return 0;
}