# C 语言学习实验室（C Learning Lab）

这是我的 C 语言学习仓库，用来整理课程笔记、练习代码和专题案例。

## 目录结构

```text
111/
├── README.md
├── C语言练习/
│   └── bubble_sort.c
├── C语言专题/
│   └── student_score_simple.c
└── 学习笔记/
    └── progress.md
```

## 如何运行

以 GCC 为例，在仓库根目录打开终端：

```bash
gcc "C语言练习/bubble_sort.c" -o bubble_sort
./bubble_sort
```

运行学生成绩示例：

```bash
gcc "C语言专题/student_score_simple.c" -o student_score
./student_score
```

Windows 下可将最后一行替换为：

```bash
bubble_sort.exe
student_score.exe
```

## 学习建议

1. 先阅读代码注释，理解每一步在做什么。
2. 自己运行程序，观察输出。
3. 尝试修改数组、学生人数或成绩。
4. 完成修改后，将遇到的问题和收获记录到 `学习笔记/progress.md`。

> 本仓库以学习和练习为目的，代码尽量保持简单，适合 C 语言初学阶段阅读。
