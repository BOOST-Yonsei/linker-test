#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>

void init_rand() {
    struct timeval tval;

    gettimeofday(&tval, NULL);
    srand(tval.tv_sec * 1000 + tval.tv_usec);
}

int rand_int(int lo, int hi) {
    if(lo > hi) return rand_int(hi, lo);

    int range = hi - lo;
    int offset = rand() % range;
    return lo + offset;
}

// Make an array of size len filled with random elements in the interval [lo,hi)
int* make_arr(size_t len, int lo, int hi) {
    int *result = malloc(len * sizeof(int));

    for(int i = 0; i < len; ++i) {
        result[i] = rand_int(lo, hi);
    }

    return result;
}

int* clone_arr(int *arr, size_t len) {
    int *result = malloc(len * sizeof(int));
    memcpy(result, arr, len * sizeof(int));
    return result;
}

// Print array where each element is printed with $width chars
void print_arr(int *arr, size_t len, int width) {
    if(len == 0) {
        printf("[]\n");
        return;
    }

    printf("[%*d", width, arr[0]);
    for(int i = 1; i < len; ++i) {
        printf(", %*d", width, arr[i]);
    }
    printf("]\n");
}

void sort_insert(int *arr, size_t len) {
    for(int i = 1; i < len; ++i) {
        int tmp = arr[i];
        int j;
        for(j = i - 1; j >= 0 && arr[j] > tmp; --j) {
            arr[j + 1] = arr[j];
        }
        arr[j + 1] = tmp;
    }
}

int main() {
    init_rand();

    size_t len = 10;
    size_t print_width = 2;

    int *arr = make_arr(len, 0, 100);
    print_arr(arr, len, print_width);

    sort_insert(arr, len);
    print_arr(arr, len, print_width);
}
