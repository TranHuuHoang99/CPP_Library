#include <iostream>
#include <stdint.h>
#include "EventEmitter/EventEmitter.hpp"


using namespace std;


int main(void) {
    uint8_t value1 = Event::EventEmitter::inst()->on<const char*>("hoang", *[](const char* name) {
        cout << "lele " << name << endl;
    });

    uint8_t value2 = Event::EventEmitter::inst()->on<const char*>("hoang", *[](const char* name) {
        cout << name << endl;
    });

    Event::EventEmitter::inst()->on<const char*>("as", *[](const char* name) {
        cout <<"sdfa "<< name << endl;
    });

    // Event::EventEmitter::inst()->off("hoang", value1);
    // Event::EventEmitter::inst()->off("hoang", value2);


    Event::EventEmitter::inst()->emit<const char*>("hoang", "dzasdf"); 

    return 0;
}