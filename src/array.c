#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <stdbool.h>
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

void reverse_arr(int *arr, size_t len) {
	for(size_t i = 0; i < len/2; ++i){
		int tmp = arr[i];
		arr[i] = arr[len - i - 1];
		arr[len - i - 1] = tmp;
	}
}

int sum_arr(int *arr, size_t len) {
	int sum = 0;
	for(size_t i = 0; i < len; ++i) {
		sum += arr[i];
	}
	
	return sum;
}

void shuffle_arr(int *arr, size_t len) {

	for(size_t i = len - 1;i > 0; --i){
		int j = rand() % (i + 1);
		int tmp = arr[i];
		arr[i] = arr[j];
		arr[j] = tmp;
	}
}

int find_max(int *arr, size_t len) {
	int max = arr[0];
	for(size_t i = 1; i < len; ++i){
		if (arr[i] > max) max = arr[i];
	}

	return max;
}

bool is_sorted(int *arr, size_t len) {

	for(size_t i = 1; i < len; i++) {
		if (arr[i-1] > arr[i]) return false;
	}

	return true;
}

int* remove_duplicates(int *arr, size_t len, size_t *new_len) {
    int *result = malloc(len * sizeof(int));
    size_t idx = 0;
    for (size_t i = 0; i < len; ++i) {
        int found = 0;
        for (size_t j = 0; j < idx; ++j) {
            if (result[j] == arr[i]) {
                found = 1;
                break;
            }
        }
        if (!found) result[idx++] = arr[i];
    }
    *new_len = idx;
    return result;
}

int* copy_reverse(int *arr, size_t len) {
    int *result = malloc(len * sizeof(int));
    for (size_t i = 0; i < len; ++i) {
        result[i] = arr[len - 1 - i];
    }
    return result;
}

int count_occurrences(int *arr, size_t len, int target) {
    int count = 0;
    for (size_t i = 0; i < len; ++i) {
        if (arr[i] == target) count++;
    }
    return count;
}

void normalize_arr(float *dest, int *src, size_t len) {
    int max = src[0], min = src[0];
    for (size_t i = 1; i < len; ++i) {
        if (src[i] > max) max = src[i];
        if (src[i] < min) min = src[i];
    }
    float range = max - min;
    for (size_t i = 0; i < len; ++i) {
        dest[i] = range == 0 ? 0.0f : (src[i] - min) / range;
    }
}

void quicksort_recursive(int *arr, int left, int right) {
    if (left >= right) return;

    int pivot = arr[right];
    int i = left - 1;

    for (int j = left; j < right; ++j) {
        if (arr[j] <= pivot) {
            i++;
            int tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
        }
    }

    int tmp = arr[i + 1];
    arr[i + 1] = arr[right];
    arr[right] = tmp;

    quicksort_recursive(arr, left, i);
    quicksort_recursive(arr, i + 2, right);
}

void merge(int *arr, int l, int m, int r) {
    int n1 = m - l + 1, n2 = r - m;
    int *L = malloc(n1 * sizeof(int));
    int *R = malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; ++i) L[i] = arr[l + i];
    for (int j = 0; j < n2; ++j) R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L); free(R);
}

void merge_sort(int *arr, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    merge_sort(arr, l, m);
    merge_sort(arr, m + 1, r);
    merge(arr, l, m, r);
}

int sort_and_sum_unique(int *arr, size_t len) {
    sort_insert(arr, len);

    int sum = 0;
    if (len > 0) sum += arr[0];
    for (size_t i = 1; i < len; ++i) {
        if (arr[i] != arr[i - 1]) {
            sum += arr[i];
        }
    }
    return sum;
}

void rotate_arr(int *arr, size_t len, int k) {
    if (len == 0) return;
    k = k % len;
    if (k == 0) return;

    int *tmp = malloc(len * sizeof(int));
    for (size_t i = 0; i < len; ++i) {
        tmp[(i + k) % len] = arr[i];
    }
    memcpy(arr, tmp, len * sizeof(int));
    free(tmp);
}

int* filter_even_arr(int *arr, size_t len, size_t *new_len) {
    int *tmp = malloc(len * sizeof(int));
    size_t idx = 0;
    for (size_t i = 0; i < len; ++i) {
        if (arr[i] % 2 == 0) {
            tmp[idx++] = arr[i];
        }
    }
    *new_len = idx;
    return realloc(tmp, idx * sizeof(int));
}

int* cumulative_sum_arr(int *arr, size_t len) {
    int *result = malloc(len * sizeof(int));
    result[0] = arr[0];
    for (size_t i = 1; i < len; ++i) {
        result[i] = result[i - 1] + arr[i];
    }
    return result;
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
