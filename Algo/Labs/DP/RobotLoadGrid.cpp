#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
using ll = long long;
ll N , M;

ll goldMaxSum(const vector<vector<ll>> &gold, int i , int j, vector<vector<ll>>& DP){
	if (i >= N || j >= M) return -1000000;
	
	if (DP[i][j] == -1000000) {
		if (i == N - 1 && j == M - 1) DP[i][j] = gold[i][j];
		else {
			//right
			ll p1 = goldMaxSum(gold, i, j + 1, DP);
			//down
			ll p2 = goldMaxSum(gold, i + 1, j, DP);
			//right-down
			ll p3 = goldMaxSum(gold, i + 1, j + 1, DP);
			ll best = max(p1, max(p2, p3));
			DP[i][j] = best + gold[i][j];
			
		}
	}
	return DP[i][j];
}


int main() {
	cin >> N >> M;
	vector<vector<ll>> grid(N, vector<ll>(M));
	for (int i = 0; i < N; ++i) {
		for (int j = 0; j < M; ++j) {
			cin >> grid[i][j];
		}
	}
	vector<vector<ll>> DP(N + 1, vector<ll>(M + 1, -1000000));
	cout << goldMaxSum(grid, 0, 0, DP) << endl;

	return 0;
}