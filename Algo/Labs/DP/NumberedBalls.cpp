#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
using ll = long long;

int v, b;
vector<ll> values;
vector<ll> dp;

ll getSolutio(ll rem) {
    if (rem == 0) return 0;
    if (rem < 0) return 1000000;        // impossible path

    if (dp[rem] != -1) return dp[rem];

    ll best = 1000000;   // start with the impossible path

    for (ll val : values) {
        ll result = getSolutio(rem - val) + 1;
        best = min(best, result);
    }

    dp[rem] = best;
    return dp[rem];
}

int main() {
    cin >> v >> b;
    values.resize(b);
    for (int i = 0; i < b; ++i) {
        cin >> values[i];
    }

    dp.assign(v + 1, -1);

    ll solution = getSolutio(v);

    //if not possible 
    if (solution >= 1000000) cout << "no solution";
    //if possible
    else cout << solution;

    return 0;
}
