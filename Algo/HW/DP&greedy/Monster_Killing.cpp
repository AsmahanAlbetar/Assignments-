#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

int m;
vector<int> weapons;
vector<pair<int,int>> dp;     // dp[h] = {finalHealth, shots}
vector<char> visited;         // visited[h] = 1 if computed

pair<int,int> findBestHealth(int h){
    if(h == 0) return make_pair(0,0);
    if(visited[h]) return dp[h];

    
    pair<int,int> best = make_pair(h,0);

    for(int i = 0; i < m; i++){
        int w = weapons[i];
        if(w == 0) continue;
        if(w > h) continue;

        pair<int,int> child = findBestHealth(h - w);
        pair<int,int> candidate = make_pair(child.first, child.second + 1);

        if(candidate.first < best.first ||
           (candidate.first == best.first && candidate.second < best.second)){
            best = candidate;
        }
    }

    visited[h] = 1;
    dp[h] = best;
    return best;
}

int main() {
    int n;
    cin >> n;
    vector<int> healths(n);
    int maxHealth = 0;
    for(int i = 0; i < n; i++){
        cin >> healths[i];
        if(healths[i] > maxHealth) maxHealth = healths[i];
    }

    cin >> m;
    weapons.resize(m);
    for(int i = 0; i < m; i++){
        cin >> weapons[i];
    }

    dp.assign(maxHealth+1, make_pair(0,0));
    visited.assign(maxHealth+1, 0);

    for(int i = 0; i < n; i++){
        pair<int,int> res = findBestHealth(healths[i]);
        cout << res.first << " " << res.second << "\n";
    }

    return 0;
}