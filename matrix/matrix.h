#ifndef MATRIX_H_
#define MATRIX_H_

#include <stdint.h>

typedef struct {
    uint32_t width;
    uint32_t height;
    uint8_t *red;
    uint8_t *green;
    uint8_t *blue;
} Image;


#endif // MATRIX_H_