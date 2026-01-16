#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
using namespace std::chrono;
using namespace std;

void SelectionSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        std::swap(arr[minIndex], arr[i]);
    }
}

void Insertion_Sort(std::vector<int>& arr) {
    int key, j;
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void Merge(std::vector<int>& arr, int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;
    int* L = new int[n1], * R = new int[n2];
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
    delete R, L;
}

void Merge_Sort(std::vector<int>& arr, int l, int r) {
    if (l < r) {
        int m = l + (r - 1) / 2;
        Merge_Sort(arr, l, m);
        Merge_Sort(arr, m + 1, r);
        Merge(arr, l, m, r);
    }
}

int partition(std::vector<int>& arr, int low, int high) {
    int pivotIndex = low + rand() % (high - low + 1);
    std::swap(arr[pivotIndex], arr[high]);
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void merge(std::vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int* L = new int[n1], * R = new int[n2];
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSortIterative(std::vector<int>& arr) {
    int n = arr.size();
    for (int size = 1; size < n; size = 2 * size) {
        for (int left = 0; left < n - 1; left += 2 * size) {
            int mid = std::min(left + size - 1, n - 1);
            int right = std::min(left + 2 * size - 1, n - 1);
            merge(arr, left, mid, right);
        }
    }
}

void heapify(std::vector<int>& arr, int i, int n = -2) {
    if (n == -2)
        n = arr.size();
    int l = 2 * i + 1;
    int r = 2 * i + 2;
    int max = i;
    if (l < n && arr[l] > arr[max])
        max = l;
    if (r < n && arr[r] > arr[max])
        max = r;

    if (max != i) {
        std::swap(arr[i], arr[max]);
        heapify(arr, max);
    }
}

void buildHeap(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, i);
}

void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    buildHeap(arr);
    for (int i = n - 1; i >= 0; i--) {
        std::swap(arr[0], arr[i]);
        heapify(arr, 0, i);
    }
}

int main(int argc, char* argv[]) {
    int algorithm_number = std::stoi(argv[1]);
    std::string input_file = argv[2];
    std::string output_file = argv[3];
    std::string time_file = argv[4];
    std::ifstream file(argv[2]);

    if (!file.is_open()) {
        std::cerr << "Error opening file!" << std::endl;
        return 1;
    }

    std::vector<int> data;
    std::vector<int> dataSorted;
    int num, i = 0;
    while (file >> num) {
        data.push_back(num);
        dataSorted.push_back(i);
        i++;
    }
    file.close();

    auto start = high_resolution_clock::now();

    switch (algorithm_number) {
    case 0:
        SelectionSort(data);
        break;
    case 1:
        Insertion_Sort(data);
        break;
    case 2:
        mergeSortIterative(data);
        break;
    case 3:
        quickSort(data, 0, data.size() - 1);
        break;
    case 4:
        heapSort(data);
        break;
    default:
        std::cout << "You need to pick an algorithm number between 0-4!\n";
        return 0;
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    std::cout << "Time taken for unsorted data:" << duration.count() / 500 << "ms\n";

    auto start2 = high_resolution_clock::now();

    switch (algorithm_number) {
    case 0:
        SelectionSort(dataSorted);
        break;
    case 1:
        Insertion_Sort(dataSorted);
        break;
    case 2:
        mergeSortIterative(dataSorted);
        break;
    case 3:
        quickSort(dataSorted, 0, dataSorted.size() - 1);
        break;
    case 4:
        heapSort(dataSorted);
        break;
    default:
        std::cout << "You need to pick an algorithm number between 0-4!\n";
        return 0;
    }

    auto stop2 = high_resolution_clock::now();
    auto durationSorted = duration_cast<microseconds>(stop2 - start2);
    std::cout << "Time taken for sorted data:" << durationSorted.count() / 500 << "ms\n";

    std::ofstream outputFile(output_file);

    if (outputFile.is_open()) {
        for (int num : data) {
            outputFile << num << std::endl;
        }
        outputFile.close();
        std::cout << "Sorted data exported to output.txt" << std::endl;
    }
    else {
        std::cerr << "Error opening output file." << std::endl;
    }

    std::ofstream outputTimeFile(time_file);

    if (outputTimeFile.is_open()) {
        outputTimeFile << "Time taken for unsorted data:" << duration.count() / 500 << "ms\n";
        outputTimeFile << "Time taken for sorted data:" << durationSorted.count() / 500 << "ms\n";
        outputTimeFile.close();
        std::cout << "Time of sorting exported to outputTime.txt" << std::endl;
    }
    else {
        std::cerr << "Error opening time output file." << std::endl;
    }



