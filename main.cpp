#include <iostream>
#include <stdio.h>
#include "EventEmitter/EventEmitter.hpp"

using namespace std;

int main(void) {
    int _age = 23;

    auto _callback = [&](int age) {
        _age = age;
    };

    void (*callback)(int) = Event::Lambda<int>::lambda_cast(_callback);

    Event::EventEmitter::inst()->on<int>("hoangprodn", callback);

    cout << _age << endl;

    return 0;
}