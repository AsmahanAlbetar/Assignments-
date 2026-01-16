#include <cmath>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
int n;
string name1, name2;
string suspect;
vector<vector<int>> dp;

bool isSuspect( int i , int j , int k){ // i is current position in name1, j is current pos in name2 and k is the suspect
    //base case 
    if(k == (int)suspect.size())
        return (i == (int)name1.size() && j== (int)name2.size());
    
    if (dp[i][j] != -1) 
        return dp[i][j];    

    if(i< (int)name1.size() && name1[i] == suspect[k]){
         if(isSuspect(i+1,j,k+1)){
            return (dp[i][j] = true);
         }
    }

    if (j< (int)name2.size() && name2[j] == suspect[k]){
        if(isSuspect(i, j+1, k+1)){
            return (dp[i][j] = true);
        }
    }
    
    return (dp[i][j] = false);
}
int main(){
 cin >> n >> name1 >> name2;
 for (int i =0; i< n ; ++i){
    cin>> suspect;
    dp.assign(name1.size()+1, vector<int>(name2.size()+1, -1)); //dp vector initialization
    cout<< (isSuspect(0,0,0) ? 1: 0) << "\n";
 }
 return 0;
}