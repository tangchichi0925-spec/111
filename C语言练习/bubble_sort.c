#include <stdio.h>

// 冒泡排序：每一轮把当前范围内最大的数移动到最后
int main(void)
{
    int arr[] = {5, 2, 9, 1, 6, 3};
    int length = sizeof(arr) / sizeof(arr[0]);

    printf("排序前：");
    for (int i = 0; i < length; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // 外层循环控制排序轮数
    for (int i = 0; i < length - 1; i++)
    {
        // 内层循环比较相邻元素
        for (int j = 0; j < length - 1 - i; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                // 交换两个元素
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    printf("排序后：");
    for (int i = 0; i < length; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
