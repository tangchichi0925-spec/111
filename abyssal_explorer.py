import random


def show_status(oxygen, treasures):
    print(f"\n氧气：{oxygen} | 宝藏：{treasures}")


def explore(oxygen, treasures):
    event = random.choice(["treasure", "oxygen", "danger", "quiet"])

    if event == "treasure":
        found = random.randint(10, 30)
        treasures += found
        print(f"你发现了一只沉船宝箱，获得 {found} 分！")
    elif event == "oxygen":
        gained = random.randint(8, 18)
        oxygen += gained
        print(f"你找到了一处气泡泉，恢复了 {gained} 点氧气！")
    elif event == "danger":
        lost = random.randint(8, 20)
        oxygen -= lost
        print(f"一群蝠鲼从你身边掠过，你慌忙躲避，损失了 {lost} 点氧气！")
    else:
        oxygen -= 5
        print("这里很安静，你看到阳光穿过海水，但消耗了 5 点氧气。")

    return oxygen, treasures


def show_result(treasures):
    if treasures >= 100:
        title = "海底传奇"
    elif treasures >= 50:
        title = "深海猎人"
    else:
        title = "新手探险家"

    print(f"你的最终称号：{title}！")


def main():
    oxygen = 60
    treasures = 0

    print("=== 深海探险 ===")
    print("找到尽可能多的宝藏，然后在氧气耗尽前返回。")

    while oxygen > 0:
        show_status(oxygen, treasures)
        choice = input("选择：1 探索，2 返回基地：").strip()

        if choice == "1":
            oxygen -= 3
            oxygen, treasures = explore(oxygen, treasures)
        elif choice == "2":
            print(f"\n你安全返回基地！最终获得 {treasures} 分。")
            show_result(treasures)
            break
        else:
            print("请输入 1 或 2。")
    else:
        print(f"\n氧气耗尽！你找到 {treasures} 分的宝藏。")
        show_result(treasures)

    print("谢谢游玩！")


if __name__ == "__main__":
    main()
