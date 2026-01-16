#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;
int N;
vector<int> deadline(N);
vector<int> penaltie(N);
struct assignment {
    int deadline;
    int penalty;
    int index;
};


bool compare(const assignment &a, const assignment &b) {
    return a.penalty > b.penalty; // sort penalties descendingly
}


int main() {
    cin >> N;

    deadline.resize(N);
    penaltie.resize(N);

    for (int i = 0; i < N; ++i) {
        cin >> deadline[i];
    }
    for (int i = 0; i < N; ++i){ 
        
        cin >> penaltie[i];
    }
    vector<assignment> tasks(N);
    for (int i = 0; i < N; ++i) {
        tasks[i] = {deadline[i], penaltie[i], i};
    }

    sort(tasks.begin(), tasks.end(), compare); // take heightest penalty first

    vector<bool> timeSlots(N, false); 
    int totalPenalty = 0;

    for (int i = 0; i < N; ++i) {
        int d = tasks[i].deadline;
        int p = tasks[i].penalty;

       
        int start = min(d, N) - 1; // cap starting slot to valid range
        for (int j = start; j >= 0; --j) {
            if (!timeSlots[j]) {
                timeSlots[j] = true;
                p = -1; // mark as scheduled
                break;
            }
        }

    if (p != -1) {
                totalPenalty += p; // can not schedule before deadline
            }
        }

        cout << totalPenalty << endl;
        return 0;
}