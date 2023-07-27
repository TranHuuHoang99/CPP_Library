#include <iostream>
#include "EventEmitter.hpp"
#include "Test_Module.hpp"

using namespace std;

int main(void) {

    Test_Module _test;

    EventEmitter::inst()->emit<int>("hoangprodn",_test.age, 1999);
    return 0;
}


//hoangprodn