#include "EventEmitter.hpp"

EventEmitter *EventEmitter::_inst = NULL;
static EventEmitter instance;

template<typename... T> std::function<void(T...)> local_callback;
void* holder;

EventEmitter *EventEmitter::inst(void) {
    if(EventEmitter::_inst == NULL) {
        EventEmitter::_inst = &instance;
    }
    return EventEmitter::_inst;
}

template<typename... T>
uint8_t EventEmitter::on(const char* eventName, std::function<void(T...)> callback) {
    local_callback<T...> = callback;

    holder = &local_callback<T...>;

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

    Events _events;
    _events.eventName = eventName;
    _events._registry._register.push_back(holder);
    _eventRegister.push_back(_events);
    return 0;
}

template<typename... T>
void EventEmitter::emit(const char* eventName, T... params) {
    Function<T...>* callback = (Function<T...>*)(holder);
    
    for(uint8_t i = 0; i < _eventRegister.size(); i++) {
        if(_eventRegister[i].eventName == eventName) {
            for(uint8_t j = 0; j < _eventRegister[i]._registry._register.size(); j++) {
                callback = (Function<T...>*)(_eventRegister[i]._registry._register[j]);
                (*callback)(params...);
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