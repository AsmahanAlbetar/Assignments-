#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <queue>
#include <unordered_map>
using namespace std;

struct treeNode {
    int val;
    treeNode* left;
    treeNode* right;
    treeNode() : val(0), left(NULL), right(NULL) {}
    treeNode(int VAL) : val(VAL), left(NULL), right(NULL) {}

};

void print(treeNode* root) {
    queue<treeNode* > q;
    if (!root) return;
    q.push(root);
    while (!q.empty()) {
        treeNode* currentNode = q.front();
        q.pop();
        cout << currentNode->val << " ";
        if (currentNode->left)
            q.push(currentNode->left);
        if (currentNode->right)
            q.push(currentNode->right);
    }
}
treeNode* builder(vector<int>& inorder, int start, int end) {
    //base case
    if (start > end) return NULL;
    int midpoint = start + (end - start) / 2;
    treeNode* root = new treeNode(inorder[midpoint]);
    root->left = builder(inorder, start, midpoint - 1);
    root->right = builder(inorder, midpoint + 1, end);
    return root;

}

int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    int n;
    int val;
    cin >> n;
    vector<int> inorder;
    for (int i = 0; i < n; i++) {
        cin >> val;
        inorder.push_back(val);
    }
    treeNode* root = builder(inorder, 0, n - 1);
    print(root);
    return 0;
}
