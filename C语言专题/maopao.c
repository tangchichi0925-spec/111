#include <stdio.h>

int main(void) {
    int a[10] = {5, 2, 9, 1, 7, 3, 10, 6, 4, 8};
    int i, j, temp;

    printf("排序前：\n");
    for (i = 0; i < 10; i++) {
        printf("%d ", a[i]);
    }

    // 冒泡排序：从小到大
    for (i = 0; i < 9; i++) { // 数组从0开始，进行9轮比较
        for (j = 0; j < 10 - 1 - i; j++) { // 每轮比较次数逐渐减少
            if (a[j] > a[j + 1]) {
                temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }

    printf("\n排序后：\n");
    for (i = 0; i < 10; i++) {
        printf("%d ", a[i]);
    }

    return 0;
}
