#ifndef EVENT_EMITTER_HPP_
#define EVENT_EMITTER_HPP_

#include <iostream>
#include <stdint.h>
#include <vector>

using namespace std;

template<typename... T> void (*callbackReference)(T...);

namespace Event {
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
            template<typename... T> void on(const char* eventName, void (*callback)(T...)) {
                callbackReference<T...> = callback;

                for(uint8_t i = 0; i < _eventRegister.size(); i++) {
                    if(_eventRegister[i].eventName == eventName) {
                        _eventRegister[i]._registry._register.push_back(reinterpret_cast<void*>(callbackReference<T...>));
                        return;
                    }
                }

                Events _events;
                _events.eventName = eventName;
                _events._registry._register.push_back(reinterpret_cast<void*>(callbackReference<T...>));
                _eventRegister.push_back(_events);
            }

            /*
                the generic function might return wrong type def so if you want to make sure to use correctly
                please give an explicit type in between 2 curly brackets
                @example void emit<const char*, float, int, uint8_t, char>()
            */
            template<typename... T> void emit(const char* eventName, T... params) {
                void (*_callbackFunc)(T...);
                for(uint8_t i = 0; i < _eventRegister.size(); i++) {
                    if(_eventRegister[i].eventName == eventName) {
                        for(uint8_t j = 0; j < _eventRegister[i]._registry._register.size(); j++) {
                            _callbackFunc = reinterpret_cast<void(*)(T...)>(_eventRegister[i]._registry._register[j]);
                            _callbackFunc(params...);
                        }
                    }
                }
            }
    };
};

#endif //EVENT_EMITTER_HPP_