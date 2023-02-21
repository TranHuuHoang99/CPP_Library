#ifndef TEST_MODULE_HPP_
#define TEST_MODULE_HPP_

#include <iostream>
#include "EventEmitter.hpp"

using namespace std;

class Test_Module {
    public:
        Test_Module();
        ~Test_Module();
        
    private:
        void test_case(void);
};

#endif //TEST_MODULE_HPP_