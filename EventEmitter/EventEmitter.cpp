#include "EventEmitter.hpp"

EventEmitter *EventEmitter::_inst = NULL;
static EventEmitter instance;

EventEmitter *EventEmitter::inst(void) {
    if(EventEmitter::_inst == NULL) {
        EventEmitter::_inst = &instance;
    }
    return EventEmitter::_inst;
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