#include "CmpString.hpp"

CmpString::CmpString(void) {

}

CmpString::~CmpString(void) {

}

void CmpString::mainFunction(void) {
    const char *name = "abcdxyzddzyzcabm";
    uint8_t length = 0;

    while(name[length] != '\0') {
        length++;
    }

    printf("%d\n", length);

    for(uint8_t i = 0, j = length - 1; i < length / 2; i++) {
        if(name[i] == name[j]) {
            cout << name[i] << endl;
            cout << name[j] << endl;
            printf("position left : %d\n", i);
            printf("position right : %d\n", j);
        }
        j--;
    }
}