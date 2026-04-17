#include "velocity.h"
#include <math.h>
#include <stdio.h>
#include <stdint.h>

float h[]={
			    0.000000000000000000,
			    -0.000011844292948183,
			    0.000050244411517520,
			    -0.000120485190509224,
			    0.000229223739602564,
			    -0.000384448993585519,
			    0.000595292842150171,
			    -0.000871691271513459,
			    0.001223905207615704,
			    -0.001661921859156350,
			    0.002194767533346004,
			    -0.002829771396343266,
			    0.003571825827701867,
			    -0.004422692369527055,
			    0.005380402471678830,
			    -0.006438799164859160,
			    0.007587259551943955,
			    -0.008810628907751042,
			    0.010089385729850237,
			    -0.011400043966472680,
			    0.012715784665125985,
			    -0.014007295313287454,
			    0.015243782072614585,
			    -0.016394108789631746,
			    0.017428007848485052,
			    -0.018317302214658084,
			    0.019037075811004531,
			    -0.019566730857893264,
			    0.019890875952507658,
			    0.979999861845983866,
			    0.019890875952507662,
			    -0.019566730857893264,
			    0.019037075811004531,
			    -0.018317302214658084,
			    0.017428007848485048,
			    -0.016394108789631753,
			    0.015243782072614594,
			    -0.014007295313287453,
			    0.012715784665125986,
			    -0.011400043966472687,
			    0.010089385729850240,
			    -0.008810628907751047,
			    0.007587259551943955,
			    -0.006438799164859167,
			    0.005380402471678838,
			    -0.004422692369527057,
			    0.003571825827701872,
			    -0.002829771396343269,
			    0.002194767533346003,
			    -0.001661921859156350,
			    0.001223905207615703,
			    -0.000871691271513459,
			    0.000595292842150170,
			    -0.000384448993585519,
			    0.000229223739602564,
			    -0.000120485190509224,
			    0.000050244411517520,
			    -0.000011844292948184,
			    0.000000000000000000,
			    };
int Nh=61;

int max_array_int(int buffer[], int size) {
    int max_val = buffer[0];


    for(int i = 1; i < size; i++) {
        if(buffer[i] > max_val) {
            max_val = buffer[i];
        }
    }

    return max_val;
}

float mean(uint16_t buffer[],int size){
    float sum = 0.0f;

    for(int i = 0; i < size; i++) {
        sum += buffer[i];
    }

    return sum / size;
}

float std_dev(uint16_t buffer[], int size) {
    float m = mean(buffer, size);
    float sum = 0.0f;

    for(int i = 0; i < size; i++) {
        float diff = buffer[i] - m;
        sum += diff * diff;
    }

    return sqrt(sum / size); // 
}

int threshold(uint16_t buffer[],int size){



    float mean_val=mean(buffer,size);
    float std_dev_val=std_dev(buffer,size);


    for(int i=0; i< size; i++){
        float z_score= (buffer[i]-mean_val)/std_dev_val;

        if(z_score>=90.0 ){
            return 1;
        }
    }

    return 0;

}

int threshold_k(uint16_t *buffer, int size) {

	int anomalie = 0;

	for (int i = 0; i < size; i++) {
		if (buffer[i] < 5000) {
			anomalie++;
		}
	}

	if (anomalie > 100) {
		return 1;
	}
	return 0;
}

void fir_filter(float *x, int Nx, float *fir_data) {
    int Ny = Nx - Nh + 1;

    for (int n = 0; n < Ny; n++) {
        float acc = 0.0f;

        for (int k = 0; k < Nh; k++) {
            acc += h[k] * x[n + k];
        }

        fir_data[n] = acc;
    }
}


