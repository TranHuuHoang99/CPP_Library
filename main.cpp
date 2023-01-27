#include <iostream>
#include <stdio.h>
#include "EventEmitter/EventEmitter.hpp"
#include <functional>

using namespace std;

int main(void) {
    char* _name = "hoang";
    int _age = 1999;

    cout << _name << endl;
    cout << _age << endl;

    auto _callback = [&](char* name, int age) {
        _name = name;
        _age = age;
    };

    EventEmitter::inst()->on<char*,int>("hoangprodn", Lambda<char*,int>::lambda_cast(_callback));
    EventEmitter::inst()->emit<char*,int>("hoangprodn", "hoangprodn", 9991);

    cout << _name << endl;
    cout << _age << endl;

    return 0;
}