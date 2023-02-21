#include <iostream>
#include "EventEmitter.hpp"

using namespace std;

class Module {
    public:
        Module() {
            test();
        }

        ~Module() {

        }

    private:
        void test(void) {
            auto callback = [&](int age) {
                cout << age << endl;
            };

            EventEmitter::inst()->on<int>("hoangprodn", Lambda<int>::cast(callback));
        }
};

int main(void) {
    Module _module;
    EventEmitter::inst()->emit<int>("hoangprodn", 1999);

    return 0;
}