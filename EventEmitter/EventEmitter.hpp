#ifndef EVENT_EMITTER_HPP_
#define EVENT_EMITTER_HPP_

#include <iostream>
#include <stdint.h>
#include <vector>
#include <functional>

template<typename... T>
struct Lambda {
    template<typename FunctionType>
    static std::function<void(T...)> cast(FunctionType& _function) {
        return static_cast<std::function<void(T...)>>(_function);
    }
};

class EventEmitter {
    public: 
        EventEmitter() {};
        ~EventEmitter() = default;

    private:
        EventEmitter(EventEmitter const&) = delete;
        void operator =(EventEmitter const&) = delete;

    private:
        static EventEmitter *_inst;
        struct Register {
            std::vector<void*> _register;
        };

        struct Events {
            const char* eventName;
            Register _registry;
        };

        std::vector<Events> _eventRegister;
        void *holder;
        
    public:
        static EventEmitter *inst(void);

        template<typename... T>
        uint8_t on(const char* eventName, std::function<void(T...)> callback) {
            holder = &callback;

            if(_eventRegister.size() != 0) {
                for(uint8_t i = 0; i < _eventRegister.size(); i++) {
                    if(_eventRegister[i].eventName == eventName) {
                        _eventRegister[i]._registry._register.push_back(holder);
                        uint8_t eventID = 0;
                        for(uint8_t j = 0; j < _eventRegister[i]._registry._register.size(); j++) {
                            eventID++;
                        }
                        return eventID - 1;
                    }
                }
            }

            Events _events;
            _events.eventName = eventName;
            _events._registry._register.push_back(holder);
            _eventRegister.push_back(_events);

            return 0;
        }
        
        template<typename... T>
        void emit(const char* eventName, T... params) {
            std::function<void(T...)>* callback;
        
            for(uint8_t i = 0; i < _eventRegister.size(); i++) {
                if(_eventRegister[i].eventName == eventName) {
                    for(uint8_t j = 0; j < _eventRegister[i]._registry._register.size(); j++) {
                        callback = (std::function<void(T...)>*)((_eventRegister[i]._registry._register[j]));
                        (*callback)(params...);
                    }
                }
            }
        }

        void off(const char* eventName, uint8_t eventID);

        void dismiss(const char* eventName);

}; //EventEmitter

#endif //EVENT_EMITTER_HPP_