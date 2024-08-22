import requests
from bs4 import BeautifulSoup
import mysql.connector

# URL dari file HTML lokal
url = "https://dashboard-lldikti6.kemdikbud.go.id/?791c9464d7028b0a6ba3be88194eb13e"  # Ganti dengan URL atau path file HTML lokal

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

# Loop melalui baris tabel, melewatkan header
for row in rows[1:]:  # Lewati baris header
    cols = row.find_all('td')
    KodePerguruanT = cols[1].text.strip()
    NamaPerguruanT = cols[2].text.strip()
    Kota = cols[3].text.strip()

    # Masukkan data ke database
    mycursor.execute(
        "INSERT INTO perguruan_tinggi (KodePerguruanT, NamaPerguruanT, Kota) VALUES (%s, %s, %s)", 
        (KodePerguruanT, NamaPerguruanT, Kota)
    )

# Commit dan tutup koneksi
mydb.commit()
mycursor.close()
mydb.close()
