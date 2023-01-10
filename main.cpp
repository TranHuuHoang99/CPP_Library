#include <iostream>
#include "EventEmitter/EventEmitter.hpp"

using namespace std;

int main(void) {
    Event::EventEmitter::inst()->on<const char*>("hoang", *[](const char* name) {
        cout << "lele " << name << endl;
    });

    Event::EventEmitter::inst()->on<const char*>("hoang", *[](const char* name) {
        cout << name << endl;
    });

    Event::EventEmitter::inst()->on<const char*>("as", *[](const char* name) {
        cout <<"sdfa "<< name << endl;
    });

    Event::EventEmitter::inst()->emit<const char*>("hoang", "dzasdf");

    return 0;
}