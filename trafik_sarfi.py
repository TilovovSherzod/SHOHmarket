import psutil
import time
import signal
import sys

# Odatda qabul qilgan va yuborgan baytlar
total_bytes_sent = 0
total_bytes_recv = 0


# Tarmoqni kuzatish funksiyasi
def track_network_usage(interval=1):
    global total_bytes_sent, total_bytes_recv

    # Eski statistika olish
    old_stats = psutil.net_io_counters()

    while True:
        try:
            time.sleep(interval)

            # Yangi statistikani olish
            new_stats = psutil.net_io_counters()

            # Yuborilgan va qabul qilingan baytlarni hisoblash
            bytes_sent = new_stats.bytes_sent - old_stats.bytes_sent
            bytes_recv = new_stats.bytes_recv - old_stats.bytes_recv

            # Baytlarda yuborilgan va qabul qilingan trafikni ekranga chiqarish
            print(f"Sent: {bytes_sent / 1024:.2f} KB, Received: {bytes_recv / 1024:.2f} KB")

            # Jami yuborilgan va qabul qilingan baytlarni yangilash
            total_bytes_sent += bytes_sent
            total_bytes_recv += bytes_recv

            # Eski statistikalarni yangilash
            old_stats = new_stats
        except KeyboardInterrupt:
            # Dastur to'xtatilganda jami ishlatilgan internetni chiqarish
            print(f"\nTotal Sent: {total_bytes_sent / 1024 / 1024:.2f} MB")
            print(f"Total Received: {total_bytes_recv / 1024 / 1024:.2f} MB")
            sys.exit(0)


# Asosiy dastur
if __name__ == "__main__":
    print("Internet foydalanishini kuzatib borilmoqda... (Ctrl+C bilan to'xtatish)")
    track_network_usage()
