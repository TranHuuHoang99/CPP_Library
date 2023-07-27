#include "MergeSort.hpp"


MergeSort::MergeSort(void) {

}

MergeSort::~MergeSort(void) {

}

void _merge(uint8_t *arr, uint8_t left, uint8_t mid, uint8_t right) {
    uint8_t left_length = mid - left + 1;
    uint8_t right_length = right - mid;

    uint8_t left_arr[left_length], right_arr[right_length];

    for(uint8_t i = 0; i < left_length; i++) {
        left_arr[i] = arr[left + i];
    }

    for(uint8_t i = 0; i < right_length; i++) {
        right_arr[i] = arr[mid + i + 1];
    }

    uint8_t i = 0, j = 0, k = left;
    while(i < left_length && j < right_length) {
        if(left_arr[i] <= right_arr[j]) {
            arr[k] = left_arr[i];
            i++;
        } else {
            arr[k] = right_arr[j];
            j++;
        }
        k++;
    }

    while(i < left_length) {
        arr[k] = left_arr[i];
        i++;
        k++;
    }

    while(j < right_length) {
        arr[k] = right_arr[j];
        j++;
        k++;
    }
}

void _Sort(uint8_t *arr, uint8_t left, uint8_t right) {
    if(left < right) {
        uint8_t mid = left + (right - left) / 2;
        _Sort(arr, left, mid);
        _Sort(arr, mid + 1, right);
        _merge(arr, left, mid, right);
    }
}

void _printArr(uint8_t *arr, uint8_t length) {
    const char* comma;
    for(uint8_t i = 0; i < length; i++) {
        comma = (length - i) == 1 ? "" : ", ";
        printf("%d%s", arr[i], comma);
    }
    printf("\n");
}

void MergeSort::mainFunction(void) {
    uint8_t arr[10] = {2,12,3,21,0,1,4,54,99,78};
    uint8_t length = sizeof(arr) / sizeof(arr[0]);

    _printArr(arr, length);

    _Sort(arr, 0, length - 1);

    _printArr(arr, length);

}