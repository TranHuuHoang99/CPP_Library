#include <iostream>
#include "EventEmitter.hpp"

using namespace std;

int main(void) {
    int localValue = 1999;

    auto callback = [&](int value) {
        localValue = value;
    };

    EventEmitter::inst()->on<int>("hoangprodn", Lambda<int>::lambda_cast(callback));

    cout << localValue << endl;

    EventEmitter::inst()->emit<int>("hoangprodn", 1234);
 
    cout << localValue << endl;
    return 0;
}