#include <vector>
#include <iostream>
#include <fstream>
#include <chrono>
using namespace std;
using namespace chrono;
//parameters
const int numOfWords = 20000;
const int hashSize = 24000;
// Advantages of using a function
//Code Reusability
//You can call the function multiple times if needed.
//You avoid repeating file reading logic in multiple places.
//Readability
//Makes your main() cleaner and easier to follow.
//Separates the concerns : file reading logic stays in one place.
//Debugging and Testing
//Easier to test the file reading part independently if it’s in a function.
//You can print, log, or inspect data returned from the function.
//Maintainability
//If the file format changes(e.g., you now have to skip lines or trim whitespace), you only update the function.

vector<string> ReadInput(string fileName) {
	ifstream inputFile(fileName);
	if (!inputFile.is_open()) { cout << "file failed to open!"; }
	string word;
	vector<string> words;
	while (inputFile >> word) {
		words.push_back(word);
	}
	inputFile.close();
	return words;

}

// hashfunction
int HashFucntion(string s) {
//ana 3ayza cases 3ala el Key size 
	int keyLen = s.length();
	switch (keyLen) {
	case 1 :
		return(int(39 * int(s[0])));
	case 2 :
		return(int(39 * int(s[0]) + 392 * int(s[1])));
	case 3:
		return(39 * int(s[0]) + 392 * int(s[1]) + 393 * int(s[2]));
	default:
		return(39 * int(s[0]) + 392 * int(s[1]) + 393 * int(s[2]) + 394 * int(s[3]));
	}
	
}
//function 3ashan a insert
bool insert(vector<string> &hash, string key, int &currentLen) {
	if (hashSize == currentLen) return false; // el table etmala
	int indexAssign = HashFucntion(key) % hashSize; 
	//handel el collision low 7asal
	while (hash[indexAssign] != "" && hash[indexAssign] != "-1") {
		indexAssign = (indexAssign+1) % hashSize;
	}
	hash[indexAssign] = key;
	currentLen += 1;
	return true;
}
bool delet(vector<string>& hash, string key, int& prob) {
	int index = HashFucntion(key) % hashSize;
	while (hash[index] != key) {
		index = (index + 1) % hashSize;
		prob++;
		if (hash[index] == "") return false;
		
	}
	hash[index] = "-1";
	return true;
}

int main() {
	//containers
	vector<string> A = ReadInput("words20K.txt");
	vector <string> hashTable(hashSize, "");
	int vecSize = 0;
	int packets = 20000 / 500;
	for (int i = 0; i < packets; ++i){
		auto start = high_resolution_clock::now();
		string word;
		for (int j = 0; j < 500; j++) {
			word = A[i * 500 + j];
			insert(hashTable, word, vecSize);
		}
		auto stop = high_resolution_clock::now();
		auto duration = duration_cast<microseconds>(stop - start);
		cout << "average time for packet number " << i + 1 << " is " << duration.count() / 500 << endl;
	}
	
	int minProb = INT_MAX;
	int maxProb = INT_MIN;
	int sum = 0;
	for (int i = 14000; i < 14999; i++) {
		string word = A[i];
		int probNum = 0;
		bool exist = delet(hashTable, word, probNum);
		if (exist) {
			if (minProb > probNum)
				minProb = probNum;
			if (maxProb < probNum)
				maxProb = probNum;
			sum += probNum;
		}
	}
	cout << "min : " << minProb << " max : " << maxProb << " average : " << float(sum / 1000);
	return 0;
}


