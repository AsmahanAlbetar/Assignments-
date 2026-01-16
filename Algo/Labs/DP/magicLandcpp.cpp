#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
using ll = long long;
int m, n;

ll maxLostBoys(const vector<vector<ll>>& lostboys, int i, int j, vector<vector<ll>>& dp) {
    if (i >= m || j >= n) return -1000000;
    if (dp[i][j] == -1000000) {

        if (i == m - 1 && j == n - 1) {
            dp[i][j] = lostboys[i][j];
        }
        else {
            //go right

            ll lost1 = maxLostBoys(lostboys, i, j + 1, dp);

            // go down 
            ll lost2 = maxLostBoys(lostboys, i + 1, j, dp);

            // go diagonal
            ll lost3 = maxLostBoys(lostboys, i + 1, j + 1, dp); 

            ll mostlostboys = max(lost1, max(lost2, lost3));
            dp[i][j] = mostlostboys + lostboys[i][j];
        }
    }
    return dp[i][j];
}

int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    cin >> m >> n;
    vector<vector<ll>> lostBoys(m , vector<ll>(n)); 
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> lostBoys[i][j];
        }
    }
    vector<vector<ll>> dp(n + 1, vector<ll>(m + 1, -1000000));

    ll lostboystotal = maxLostBoys(lostBoys, 0, 0, dp);
    cout << lostboystotal;
    return 0;
}
