#include "XorSort.hpp"


XorSort::XorSort(void) {

}

XorSort::~XorSort(void) {

}

void _printArr(uint8_t *arr, uint8_t length) {
    const char* comma;
    for(uint8_t i = 0; i < length; i++) {
        comma = (length - i) == 1 ? "" : ", ";
        printf("%d%s", arr[i], comma);
    }
    printf("\n");
}

void XorSort::mainFunction(void) {
    uint8_t arr[10] = {2,12,3,21,0,1,4,54,99,78};
    uint8_t length = sizeof(arr) / sizeof(arr[0]);

    _printArr(arr, length);

    for(uint8_t i = 0; i < length; i++) {
        for(uint8_t j = i + 1; j < length; j++) {
            if(arr[j] < arr[i]) {
                arr[j] ^= arr[i];
                arr[i] ^= arr[j];
                arr[j] ^= arr[i];
            }
        }
    }

    _printArr(arr, length);
}