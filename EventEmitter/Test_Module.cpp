#include "Test_Module.hpp"


Test_Module::Test_Module() : age(24) {
    printf("initialized\n");
    test_case();
}

Test_Module::~Test_Module() {

}


void Test_Module::callback(int _age) {
    age = _age;
}

void Test_Module::test_case(void) {

    EventEmitter::inst()->on<int>("hoangprodn", (void(*)(int))&callback);
}