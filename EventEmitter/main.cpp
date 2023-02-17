#include <iostream>
#include "EventEmitter.hpp"

using namespace std;

int main(void) {
    int test = 0;
    int value = 9;
    cout << value << endl;

    auto callback = [&](int _value) {
        value = _value;
    };

    EventEmitter::inst()->on<int>("hoangprodn", Lambda<int>::lambda_cast(callback));

    EventEmitter::inst()->emit<int>("hoangprodn", 34);

    auto va = [&](int _value) {
        test = _value;
    };

    EventEmitter::inst()->on<int>("hoangprodn", Lambda<int>::lambda_cast(va));


    cout << value << endl;
    cout << test << endl;

    return 0;

}