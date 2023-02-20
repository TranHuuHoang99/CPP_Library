#include <iostream>
#include "EventEmitter.hpp"
#include <windows.h>

using namespace std;

class A {
    public:
        A() {
            auto callback = [&](char *name, int age) {
                cout << name << endl;
                cout << age << endl;
            };

            EventEmitter::inst()->on<char*,int>("hoangprodn", Lambda<char*,int>::lambda_cast(callback));
        }

        ~A() {

        }
};

int main(void) {
    A *_a = new A();

    while(true) {
        
        EventEmitter::inst()->emit<char*,int>("hoangprodn", "hoang", 1999);
    }
    return 0;
}