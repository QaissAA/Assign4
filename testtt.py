import os
import time

# Путь для тестовых файлов
TEST_DIR = "/tmp/disk_io_test"
NUM_FILES = 5
FILE_SIZE_MB = 50  # размер каждого файла
DURATION = 60  # длительность нагрузки в секундах

os.makedirs(TEST_DIR, exist_ok=True)

# Создание тестовых файлов, если их нет
for i in range(NUM_FILES):
    file_path = os.path.join(TEST_DIR, f"test_file_{i}.bin")
    if not os.path.exists(file_path):
        print(f"Создаю файл {file_path} ({FILE_SIZE_MB}MB)...")
        with open(file_path, "wb") as f:
            f.write(os.urandom(FILE_SIZE_MB * 1024 * 1024))

print(f"Запускаем симуляцию чтения с диска на {DURATION} секунд...")

end_time = time.time() + DURATION
while time.time() < end_time:
    for i in range(NUM_FILES):
        file_path = os.path.join(TEST_DIR, f"test_file_{i}.bin")
        with open(file_path, "rb") as f:
            # Читаем файл по блокам 4 МБ
            while True:
                data = f.read(4 * 1024 * 1024)
                if not data:
                    break
        # Небольшая пауза, чтобы не перегружать полностью диск
        time.sleep(0.1)

print("Симуляция чтения завершена. Disk I/O должен вернуться к норме.")
