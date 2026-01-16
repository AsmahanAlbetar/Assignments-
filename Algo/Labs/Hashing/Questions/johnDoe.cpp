#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <sstream>

using namespace std;

void preprocess(string & str)
{
   // Removing punctuation 
   for (int i = 0, len = str.size(); i < len; i++)
   {
       // Check whether parsing character is punctuation or not 
       if (ispunct(str[i]))
       {
           str.erase(i--, 1);
           len = str.size();
       }
   }

   // Converting to lower case 
   transform(str.begin(), str.end(), str.begin(), ::tolower);
}

// Helper function 
vector<string> readFile()
{
   ifstream f("two-cities.txt"); // taking file as inputstream 

   string file;

   if (f)
   {
       ostringstream ss;
       ss << f.rdbuf(); // reading data 
       file = ss.str();

       // Removes punctuation and converts to lower case 
       preprocess(file);

       // Split into tokens on space 
       istringstream iss(file);
       vector<string> tokens{ istream_iterator<string>{iss},
                             istream_iterator<string>{} };

       return tokens;
   }

   vector<string> empty;
   return empty;
}

string findSecret(vector<string> tokens) {
   unordered_map<string, int> table;
   vector<pair<string, int>> frequencyOfWord;
   int order[] = { 11, 23, 22, 43, 3, 47 };
   for (const auto& word : tokens) {
       table[word]++; //assign the word and count it's frequency
   }
       for (const auto& wordInTable : table) {
           frequencyOfWord.push_back({ wordInTable.first, wordInTable.second });
           const auto sortingBased = [](const auto& a, const auto& b)
               {return a.second > b.second; };
           //sort in the array using DESC order
           sort(frequencyOfWord.begin(), frequencyOfWord.end(), sortingBased);
           //start printing results
           string results = "";
           for (const int index : order) {
               results += frequencyOfWord[index - 1].first + "";

           }
           return results;
       }
       
}
int main()
{

   vector<string> tokens = readFile();

   cout << findSecret(tokens) << endl;
   return 0;
}