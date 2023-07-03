import datetime

def generate_unique_number():
    current_date = datetime.datetime.now()
    year = current_date.year
    month = current_date.month

    # Baca nomor urut dari file
    try:
        with open("nomor_urut.txt", "r") as file:
            nomor_urut = int(file.read())
    except FileNotFoundError:
        nomor_urut = 1

    # Format nomor urut dengan 3 digit angka
    nomor_urut_formatted = str(nomor_urut).zfill(3)

    # Tingkatkan nomor urut untuk penggunaan selanjutnya
    nomor_urut += 1

    # Simpan nomor urut ke file
    with open("nomor_urut.txt", "w") as file:
        file.write(str(nomor_urut))

    # Gabungkan tahun, bulan, dan nomor urut
    unique_number = f"{year}.{month:02d}.{nomor_urut_formatted}"
    return unique_number

# Contoh penggunaan
nomor_unik = generate_unique_number()
print(nomor_unik)
 