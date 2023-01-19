#ifndef EVENT_EMITTER_HPP_
#define EVENT_EMITTER_HPP_

#include <iostream>
#include <stdint.h>
#include <vector>

using namespace std;


namespace Event {
    /*
        This struct and function lambda_cast to convert from capturing lambda function to function pointer
        if you want to apply or change variables out of lambda function scope you'll suppose to use if
    */
    template<typename... T>
    struct Lambda {
        template<typename LambdaPtr>
        static void lambda_expression(T... params) {
            return (void)(*(LambdaPtr*)func_address())(params...);
        }

        template<typename CallbackType = void(*)(T...), typename FunctionType>
        static CallbackType lambda_cast(FunctionType& _type) {
            func_address(&_type); // holder the address of lambda function thround void pointer
            return (CallbackType)lambda_expression<FunctionType>;
        }
        
        static void* func_address(void* address = nullptr) {
            void* _func_ptr;
            if(address != nullptr) {
                _func_ptr = address;
            }
            return _func_ptr;
        }
    };

    class EventEmitter {
        public:
            EventEmitter() = default;
            ~EventEmitter() = default;

        private:
            EventEmitter(EventEmitter const&) = delete;
            void operator=(EventEmitter const&) = delete;

        private:
            static EventEmitter *_inst;

            struct Register {
                std::vector<void*> _register;
            };

            struct Events {
                const char* eventName;
                Register _registry;
            };

        public:
            static EventEmitter *inst(void);
            std::vector<Events> _eventRegister;

            /*
                the generic function might return wrong type def so if you want to make sure to use correctly
                please give an explicit type in between 2 curly brackets
                @example void on<const char*, float, int, uint8_t, char>()
                @attention !!!
                    this generic function is supposed to be defined before calling emit function below
                    and this must be happened first
            */
            template<typename... T> uint8_t on(const char* eventName, void (*&callback)(T...));

            /*
                the generic function might return wrong type def so if you want to make sure to use correctly
                please give an explicit type in between 2 curly brackets
                @example void emit<const char*, float, int, uint8_t, char>()
            */
            template<typename... T> void emit(const char* eventName, T... params);

            void off(const char* eventName, uint8_t eventID);

            void dismiss(const char* eventName);
    };
};

#include "EventEmitter.tpp"

#endif //EVENT_EMITTER_HPP_