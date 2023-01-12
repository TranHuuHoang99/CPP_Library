#include "EventEmitter.hpp"

template<typename... T> void (*callbackReference)(T...);

namespace Event {
    EventEmitter *EventEmitter::_inst = NULL;
    EventEmitter _eventEmitter;

    EventEmitter *EventEmitter::inst(void) {
        if(EventEmitter::_inst == NULL) {
            EventEmitter::_inst = &_eventEmitter;
        }

        return EventEmitter::_inst; 
    }

    template<typename... T> uint8_t EventEmitter::on(const char* eventName, void (*callback)(T...)) {
        callbackReference<T...> = callback;

        for(uint8_t i = 0; i < _eventRegister.size(); i++) {
            if(_eventRegister[i].eventName == eventName) {
                _eventRegister[i]._registry._register.push_back(reinterpret_cast<void*>(callbackReference<T...>));
                uint8_t eventID = 0;
                for(uint8_t j = 0; j < _eventRegister[i]._registry._register.size(); j++) {
                    eventID++;
                }
                return eventID - 1;
            }
        }

        Events _events;
        _events.eventName = eventName;
        _events._registry._register.push_back(reinterpret_cast<void*>(callbackReference<T...>));
        _eventRegister.push_back(_events);
        return 0;
    }

    template<typename... T> void EventEmitter::emit(const char* eventName, T... params) {
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

    void EventEmitter::off(const char* eventName, uint8_t eventID) {
        for(uint8_t i = 0; i < _eventRegister.size(); i++) {
            if(_eventRegister[i].eventName == eventName){
                _eventRegister[i]._registry._register.erase(_eventRegister[i]._registry._register.begin() + eventID);
            }
        }
    }

    void EventEmitter::dismiss(const char* eventName) {
        for(uint8_t i = 0; i < _eventRegister.size(); i++) {
            if(_eventRegister[i].eventName == eventName) {
                _eventRegister.erase(_eventRegister.begin() + i);
            }
        }
    }
}