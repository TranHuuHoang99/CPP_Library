#include "EventEmitter.hpp"

namespace Event {
    EventEmitter *EventEmitter::_inst = NULL;
    EventEmitter _eventEmitter;

    EventEmitter *EventEmitter::inst(void) {
        if(EventEmitter::_inst == NULL) {
            EventEmitter::_inst = &_eventEmitter;
        }

        return EventEmitter::_inst; 
    }
}