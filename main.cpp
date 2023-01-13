#include <iostream>
#include "EventEmitter/EventEmitter.hpp"

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


    void (*callback)(char*,int) = Event::Lambda<char*, int>::lambda_cast(_callback);

    // callback("hoangprodn", 2023);

    Event::EventEmitter::inst()->on<char*, int>("hoang", callback);
    Event::EventEmitter::inst()->emit<char*, int>("hoang", "hoangprodn", 2024);

    cout << _name << endl;
    cout << _age << endl;
    
    return 0;
}