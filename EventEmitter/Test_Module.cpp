#include "Test_Module.hpp"


Test_Module::Test_Module() {
    test_case();
}

Test_Module::~Test_Module() {

}

void Test_Module::test_case(void) {
    
    auto callback = [&](int age) {
        cout << age << endl;
    };

    EventEmitter::inst()->on<int>("hoang", Lambda<int>::cast(callback));
}