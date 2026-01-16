//An ancient civilization encoded the structure of their sacred trees into two mysterious sequences.Each sequence was written by a different scribe, using a unique but consistent rule for walking through the tree and recording its nodes.
//
//Your task is to decipher these scrolls and reconstruct the original tree.
//
//You are given two lists of distinct integers of equal length, each representing a walk through the same binary tree :
//
//The first list follows a "root-before-branches" strategy.
//
//The second list follows a "left-root-right" approach.
//
//Using this information, rebuild the exact structure of the binary tree as it originally stood.
//
//Input Format
//
//The first line contains a single integer n — the number of nodes in the binary tree.
//The second line contains n space - separated integers — the node labels written by the first scribe.
//The third line contains n space - separated integers — the node labels written by the second scribe.
//Constraints
//
//1 ≤ n ≤ 3000
//All node values are distinct.
//Each node value is an integer between - 3000 and 3000, inclusive.
//Output Format
//
//Print a single line containing the breadth - first traversal(level - order) of the reconstructed tree.
//
//Separate the node values with spaces.Do not include null or markers for missing children — only the actual node values visited level by level from left to right.
//
//Sample Input 0
//
//5
//12 19 31 - 18 34
//31 19 - 18 12 34
//Sample Output 0
//
//12 19 34 31 - 18
//Sample Input 1
//
//4
//16 - 21 37 34
//37 - 21 16 34
//Sample Output 1
//
//16 - 21 34 37
#include <vector>
#include <iostream>
#include <algorithm>
#include <queue>
#include <cmath>
#include <cstdio>
#include <unordered_map>
using namespace std;
struct treeNode {
	int val;
	treeNode* left;
	treeNode* right;
	treeNode() : val(0), left(NULL), right(NULL) {}
	treeNode(int VAL) : val(VAL), left(NULL), right(NULL){}

};

unordered_map<int,int> inorderIndex;
int preorderIndex = 0;

treeNode* builder(vector<int>& preorder, int left, int right) {
	//base case
	if (left>right) return NULL;
	//build left tree and then nebny right tree
	int rootval = preorder[preorderIndex];
	preorderIndex++;
	treeNode* root = new treeNode(rootval);
	//negyb el midpoint 
	int midPoint = inorderIndex[rootval];
	root->left = builder(preorder, left , midPoint-1);
	root->right = builder(preorder, midPoint + 1, right);
	return root;

}
treeNode* buildTree(vector<int>& inorder, vector<int>& preorder) {
	for (int i = 0; i < inorder.size(); i++) {
		inorderIndex[inorder[i]] = i; //value, position
	}
	return builder(preorder, 0, inorder.size() - 1);
}
void printBFS(treeNode* root) {
	queue<treeNode* > frontier;
	if (!root) return;
	frontier.push(root);
	while (!frontier.empty()) {
		treeNode* currentNode = frontier.front();
		frontier.pop();
		cout << currentNode->val<< " ";
		if (currentNode->left)
			frontier.push(currentNode->left);
		if (currentNode->right)
			frontier.push(currentNode->right);
	}

}


int main() {
	int N;
	vector<int> inorder;
	vector<int> preorder;
	cin >> N;
	int val;
	for (int i = 0; i < N; ++i) {
		cin >> val;
		preorder.push_back(val);
	}
	for (int i = 0; i < N; ++i) {
		cin >> val;
		inorder.push_back(val);
	}
	

	treeNode* root1 = new treeNode();
	root1 = buildTree(inorder, preorder);
	printBFS(root1);
	return 0;
}