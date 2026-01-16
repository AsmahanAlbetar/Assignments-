#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
using ll = long long;
int n;
vector<int> treasure;
vector<ll> dp;
ll best(int i) {
   if (i >= n) return 0;
   if (dp[i] != -1) return dp[i];
   //skip this treasure
   ll skip = best(i + 1);
   // dp not skip 
   ll take = treasure[i] + best(i + 2);
   return dp[i] = max(skip, take);
}
ll MaxTreasureDp(int i) {
   if (i == n)
       return 0;
   if (dp[i] != -1) return dp[i];
    //skip this treasure
     ll skip = MaxTreasureDp(i + 1);
     // dp not skip 
     ll take = treasure[i] + MaxTreasureDp(i + 2);

      return dp[i] = max(skip, take);
}
int main() {
   /* Enter your code here. Read input from STDIN. Print output to STDOUT */ 

   cin >> n;
   treasure.resize(n);
   dp.assign(n, -1);
   for (int i = 0; i < n; ++i) {
       cin >> treasure[i];
   }

   ll output = MaxTreasureDp(0);
   cout << output;

   return 0;
}


