#ifndef EVENT_EMITTER_HPP_
#define EVENT_EMITTER_HPP_

#include <iostream>
#include <stdint.h>
#include <vector>
#include <functional>

template<typename... T> using Function = std::function<void(T...)>;

template<typename... T>
struct Lambda {
    template<typename FunctionType>
    static Function<T...> lambda_cast(FunctionType& _function) {
        return static_cast<Function<T...>>(_function);
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
        
    public:
        static EventEmitter *inst(void);
        template<typename... T>
        uint8_t on(const char* eventName, std::function<void(T...)> callback);
        
        template<typename... T>
        void emit(const char* eventName, T... params);

        void off(const char* eventName, uint8_t eventID);

        void dismiss(const char* eventName);

};

#include "EventEmitter.tpp"

#endif //EVENT_EMITTER_HPP_