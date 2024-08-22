import requests
from bs4 import BeautifulSoup
import mysql.connector

# URL dari file HTML lokal
# url = "https://dashboard-lldikti6.kemdikbud.go.id/?791c9464d7028b0a6ba3be88194eb13e"  # jawa tengah
url = "https://direktori.lldikti4.id/perguruantinggi/listsatuanpendidikan/" # jabar banten

# Membuka file HTML lokal
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Menemukan tabel dalam file HTML
table = soup.find('table')
rows = table.find_all('tr')

# Koneksi ke database
mydb = mysql.connector.connect(
    host="localhost",  # Host harus hanya localhost tanpa http:// dan port 3306
    user="root",
    password="",
    database="bd_perguruant"
)

mycursor = mydb.cursor()

for row in rows[1:]:  # Lewati baris header
    cols = row.find_all('td')
    
    # Cek jumlah kolom sebelum mengaksesnya
    if len(cols) >= 9:
        col1 = cols[1].text.strip()
        col2 = cols[2].text.strip()
        col3 = cols[7].text.strip()
        col4 = cols[8].text.strip()

        # Masukkan data ke database
        mycursor.execute(
            "INSERT INTO perguruan_tinggi (KodePerguruanT, NamaPerguruanT, Kota, Provinsi) VALUES (%s, %s, %s, %s)", 
            (col1, col2, col3, col4)
        )
    else:
        print("Baris ini tidak memiliki cukup kolom:", row)

# Commit dan tutup koneksi
mydb.commit()
mycursor.close()
mydb.close()
