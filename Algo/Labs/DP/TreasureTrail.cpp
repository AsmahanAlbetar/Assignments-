#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
int n;
vector<int> gold; // gold 
vector<int> trap;
vector<int> dp;
int maxGold(int i) {
  // When i == n, it means weve gone past the last chest(no more chests to consider).
    //In this case, the maximum gold you can collect from here is 0.
   if (i >= n)
       return 0;
   if (dp[i] != -1) return dp[i];
   // take 
   //So the + 1 accounts for skipping the destroyed chests plus the current chest itself.
   //Without + 1, you'd wrongly consider the first destroyed chest as available.
   int taken = gold[i]+maxGold(i + trap[i]+1);
   // skip
   int skipped = maxGold(i + 1);
   return dp[i] = max(taken, skipped);
}
int main() {
   /* Enter your code here. Read input from STDIN. Print output to STDOUT */
   cin >> n;
   gold.resize(n);
   trap.resize(n);
   dp.assign(n, -1);
   for (int i = 0; i < n; i++) {
       cin >> gold[i] >> trap[i];
   }
  
   cout << maxGold(0)<<endl;
   return 0;
}
