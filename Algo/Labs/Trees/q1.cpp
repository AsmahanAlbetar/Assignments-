#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <unordered_map>
using namespace std;

struct treeNode {
	int val;
	treeNode* left;
	treeNode* right;
	treeNode() : val(0), left(NULL), right(NULL) {}
	treeNode(int VAL) : val(VAL), left(NULL), right(NULL) {}

};
unordered_map <int,int >leftnodes; //root , child 
unordered_map <int, int >rightnodes; //root , child 

void buildTree(treeNode* root) {
	if (!root) return;
	if (leftnodes.find(root->val) != leftnodes.end()) {
		int leftval = leftnodes[root->val];
		root->left = new treeNode(leftval);
		buildTree(root->left);
	}
	if (rightnodes.find(root->val) != rightnodes.end()) {
		int rightval = rightnodes[root->val];
		root->right = new treeNode(rightval);
		buildTree(root->right);
	}

}
int subTrees = 0;

bool findTree(treeNode* root, int& v1, int& v2) {
	if (!root) return true;
	//if (root && root->val > v1 && root->val < v2) return true;
	bool leftsub = findTree(root->left, v1, v2);
	bool rightsub = findTree(root->right, v1, v2);

	if (root->val > v1 && root->val < v2 && leftsub && rightsub) {
		subTrees++;
		return true;	
	}
	return false;
}
int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */

	int v1, v2, numofedges,root,givenchild,numofleftnode=0,numofrightnode=0;
	treeNode* mainroot = new treeNode;
	char child;
	cin >> v1 >> v2 >> root>>numofedges;
	mainroot->val = root;
	for (int i = 0; i < numofedges; i++) {
		cin >> child>>root>>givenchild;
		if (child == 'L')
		{
			numofleftnode += 1;
			leftnodes[root] = givenchild;
		}
		if (child == 'R') {
			numofrightnode += 1;
			rightnodes[root] = givenchild;
		}
	}
	buildTree(mainroot);
	bool found = findTree(mainroot, v1, v2);
	cout << subTrees;
}