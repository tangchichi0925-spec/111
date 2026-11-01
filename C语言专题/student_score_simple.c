#include <stdio.h>

#define STUDENT_COUNT 3

// 简单学生成绩统计：输入成绩，计算平均分并找出最高分
int main(void)
{
    float scores[STUDENT_COUNT];
    float sum = 0.0f;
    float max_score;

    // 输入成绩
    for (int i = 0; i < STUDENT_COUNT; i++)
    {
        printf("请输入第 %d 位学生的成绩（0-100）：", i + 1);

        if (scanf("%f", &scores[i]) != 1 || scores[i] < 0 || scores[i] > 100)
        {
            printf("输入无效，请输入 0 到 100 之间的数字。\n");
            return 1;
        }

        sum += scores[i];
    }

    // 统计最高分
    max_score = scores[0];
    for (int i = 1; i < STUDENT_COUNT; i++)
    {
        if (scores[i] > max_score)
        {
            max_score = scores[i];
        }
    }

    printf("\n--- 成绩统计 ---\n");
    for (int i = 0; i < STUDENT_COUNT; i++)
    {
        printf("第 %d 位学生：%.1f 分\n", i + 1, scores[i]);
    }

    printf("平均分：%.2f\n", sum / STUDENT_COUNT);
    printf("最高分：%.1f\n", max_score);

    return 0;
}
