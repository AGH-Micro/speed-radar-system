#ifndef VELOCITY_H
#define VELOCITY_H
#include <stdint.h>

float mean(uint16_t buffer[], int size);
float std_dev(uint16_t buffer[], int size);
int threshold(uint16_t buffer[], int size);
int threshold_k(uint16_t *buffer, int size);
int max_array_int(int buffer[], int size);
void fir_filter(float *x, int Nx, float *fir_data);
#endif
