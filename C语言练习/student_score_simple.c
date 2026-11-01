#include <stdio.h>

/*
    学生信息结构体：
    每个学生包含学号、姓名和成绩
*/
typedef struct {
    int id;
    char name[20];
    float score;
} Student;

int main(void) {
    // s 用来保存学生信息，temp 用于排序时临时交换学生
    Student s[50], temp;

    // n 表示当前学生数量，choice 表示菜单选择，i 和 j 用作循环变量
    int n = 0, choice, i, j;

    // sum 用来计算所有学生的成绩总和
    float sum;

    /*
        菜单循环：
        每次完成一个功能后重新显示菜单。
        当用户输入 0 时，使用 break 退出循环。
    */
    while (1) {
        printf("\n1. Add  2. Show  3. Average  4. Sort  0. Exit\n");
        printf("Choose: ");
        scanf("%d", &choice);

        // 用户输入 0，结束程序
        if (choice == 0) {
            break;
        }

        // 添加学生
        if (choice == 1) {
            // 数组最多保存 50 个学生，防止数组越界
            if (n >= 50) {
                printf("Student list is full.\n");
                continue;
            }

            printf("ID Name Score: ");
            scanf("%d %19s %f", &s[n].id, s[n].name, &s[n].score);

            // 添加成功后，学生数量加 1
            n++;
            printf("Added successfully.\n");

        // 显示所有学生
        } else if (choice == 2) {
            // 没有学生时，提示用户先添加数据
            if (n == 0) {
                printf("No student data. Please add a student first.\n");
                continue;
            }

            for (i = 0; i < n; i++) {
                printf("%d  %s  %.1f\n",
                       s[i].id,
                       s[i].name,
                       s[i].score);
            }

        // 计算平均分
        } else if (choice == 3) {
            // 没有学生时不能计算平均分
            if (n == 0) {
                printf("No score data. Please add a student first.\n");
                continue;
            }

            sum = 0;

            // 累加所有学生的成绩
            for (i = 0; i < n; i++) {
                sum += s[i].score;
            }

            // 总成绩除以学生人数，得到平均分
            printf("Average: %.1f\n", sum / n);

        // 按成绩从高到低排序
        } else if (choice == 4) {
            // 没有学生时不需要排序
            if (n == 0) {
                printf("No student data. Please add a student first.\n");
                continue;
            }

            /*
                冒泡排序：
                比较相邻两个学生的成绩。
                如果前面的成绩较低，就交换两个学生。
                每完成一轮，较小的成绩会逐渐移动到后面。
            */
            for (i = 0; i < n - 1; i++) {
                for (j = 0; j < n - 1 - i; j++) {
                    if (s[j].score < s[j + 1].score) {
                        // 交换两个完整的 Student 结构体
                        temp = s[j];
                        s[j] = s[j + 1];
                        s[j + 1] = temp;
                    }
                }
            }

            printf("Sorted successfully.\n");

        } else {
            // 用户输入了菜单中不存在的选项
            printf("Wrong choice.\n");
        }
    }

    return 0;
}
