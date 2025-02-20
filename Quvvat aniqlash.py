# import psutil
# import time
#
#
# def check_battery():
#     while True:
#         # Batareya holatini olish
#         battery = psutil.sensors_battery()
#
#         # Batareya foizini olish
#         percent = battery.percent
#
#         # Quvvatga ulanganligini tekshirish
#         plugged = battery.power_plugged
#
#         # Batareya foizini chiqarish
#         print(f"Batareya foizi: {percent}%")
#
#         # Agar quvvatga ulangan bo'lsa va foiz 80% ga yetgan bo'lsa, xabar berish
#         if plugged and percent >= 80:
#             print("Quvvat darajasi 80% ga yetdi!")
#             break
#
#         # Har 4 soniyada qayta tekshirish
#         time.sleep(4)
#
#
# if __name__ == "__main__":
#     check_battery()




import psutil
import time

def check_battery():
    last_plugged = None  # Avvalgi quvvat holatini saqlash
    last_change_time = None  # Quvvat uzgarishi vaqtini saqlash

    while True:
        # Batareya holatini olish
        battery = psutil.sensors_battery()

        # Batareya foizini olish
        percent = battery.percent

        # Quvvatga ulanganligini tekshirish
        plugged = battery.power_plugged

        # Quvvat uzgarishini tekshirish
        if last_plugged is None:
            last_plugged = plugged
            last_change_time = time.time()  # Dastlabki vaqtni saqlash
        elif last_plugged != plugged:  # Agar quvvat holati o'zgarsa
            current_time = time.time()
            elapsed_time = current_time - last_change_time

            if plugged:
                print(f"Qurilma quvvatga ulandi. Quvvat uzilganidan beri {elapsed_time:.2f} soniya o'tdi.")
            else:
                print(f"Qurilma quvvatdan uzildi. Quvvatga ulanganidan beri {elapsed_time:.2f} soniya o'tdi.")

            # Holatni va vaqtni yangilash
            last_plugged = plugged
            last_change_time = current_time

        # Har 1 soniyada qayta tekshirish
        time.sleep(1)

if __name__ == "__main__":
    check_battery()
