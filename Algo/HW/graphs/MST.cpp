
#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <queue>
#include <utility>
using ll = long long;
using namespace std;

int findRoot(int x, vector<int>& parentNode){
    if(parentNode[x] == x) return x;
    parentNode[x] = findRoot(parentNode[x], parentNode);
    return parentNode[x];
}

bool unionSet(int x, int y, vector<int>& parentNode, vector<int>& height){
    x = findRoot(x, parentNode);
    y = findRoot(y, parentNode);
    if(x == y) return false;
    if(height[x] < height[y]) parentNode[x] = y;
    else if(height[x] > height[y]) parentNode[y] = x;
    else {
        parentNode[y] = x;
        height[x]++;
    }
    return true;
}

int main(){

    int n, m, a;
    cin >> n >> m >> a;

    vector<int> u, v, w;
    u.reserve(m);
    v.reserve(m);
    w.reserve(m);

    for(int i = 0; i < m; i++){
        int x;  //region 1 endpoint 1
        int y;  // region 2 endpoint 2
        int c;  // cost 3ashan ne build the road
        cin >> x >> y >> c;
        if(c < a){
            u.push_back(x);
            v.push_back(y);
            w.push_back(c);
        }
    }

    vector<int> index(u.size());
    for(int i = 0; i < (int)index.size(); i++) index[i] = i;

    sort(index.begin(), index.end(), [&](int i, int j){
        return w[i] < w[j];
    });

    vector<int> parentNode(n+1), height(n+1, 0);
    for(int i = 1; i <= n; i++) parentNode[i] = i;

    ll roads = 0;
    int connectedComponents = n;

    for(int k = 0; k < (int)index.size(); k++){
        int i = index[k];
        if(unionSet(u[i], v[i], parentNode, height)){
            roads += w[i];
            connectedComponents--;
        }
    }

   ll total = roads + (ll)connectedComponents * a;
    cout << total << " " << connectedComponents;
    return 0;
}
