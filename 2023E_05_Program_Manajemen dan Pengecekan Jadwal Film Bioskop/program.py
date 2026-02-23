import json
from datetime import datetime, time, timezone, timedelta, date

class JadwalFilm:
    def __init__(self, judul, jam: time):
        self.judul = judul
        self.jam = jam
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, judul, jam: time):
        new_node = JadwalFilm(judul, jam)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def to_array(self):
        data = []
        current = self.head
        while current:
            data.append((current.judul, current.jam))
            current = current.next
        return data

    def from_array(self, data):
        self.head = None
        for item in data:
            self.insert(item[0], item[1])

    def sort_by(self, key='judul'):
        data = self.to_array()
        # Insertion Sort
        for i in range(1, len(data)):
            key_item = data[i]
            j = i - 1
            while j >= 0 and (
                (key == 'judul' and data[j][0].lower() > key_item[0].lower()) or
                (key != 'judul' and data[j][1] > key_item[1])
            ):
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key_item
        self.from_array(data)

    def hapus_by_index_sorted_judul(self, index):
        data = self.to_array()
        data.sort(key=lambda x: x[0].lower())
        while not (0 < index <= len(data)):
            print("⚠️  Tolong masukkan nomor yang valid.")
            print("---------------------------------------")
            index = int(input("Masukkan nomor film yang ingin dihapus: "))
        else:
            target = data[index - 1]
            tanggal_input = date.today().isoformat()
            new_data = [item for item in self.to_array() if not (item[0] == target[0] and item[1] == target[1])]
            self.from_array(new_data)
            simpan_ke_history("history_jadwal_bioskop.json", [(target[0], target[1], tanggal_input)])
            print(f"Film nomor {index} berhasil dihapus.")
            return new_data

    def tampilkan_dengan_nomor(self, by='judul'):
        current = self.head
        if not current:
            print("Daftar kosong.")
            return
        i = 1
        while current:
            if by == 'judul':
                print(f" {i}. {current.judul} - {current.jam.strftime('%H:%M')} WIB")
            else:
                print(f" {i}. {current.jam.strftime('%H:%M')} WIB - {current.judul}")
            current = current.next
            i += 1

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, judul, jam: time):
        tanggal_input = date.today().isoformat()
        self.items.append((judul, jam, tanggal_input))

    def dequeue_expired(self, current_time: time):
        new_expired = []
        remaining = []
        try:
            with open("history_jadwal_bioskop.json", "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            history = {}

        for judul, jam, tgl in self.items:
            jam_str = jam.strftime('%H:%M')
            # Jangan masukkan jika sudah ada dalam history tanggal itu
            if jam <= current_time:
                if tgl not in history or (judul, jam_str) not in history[tgl]:
                    new_expired.append((judul, jam, tgl))
            else:
                remaining.append((judul, jam, tgl))

        self.items = remaining
        if new_expired:
            simpan_ke_history("history_jadwal_bioskop.json", new_expired)
        return new_expired

    def from_array(self, data):
        self.items = []
        for judul, jam in data:
            self.enqueue(judul, jam)

# === File JSON ===
def simpan_ke_json(nama_file, data):
    data_json = [(judul, jam.strftime('%H:%M')) for judul, jam in data]
    with open(nama_file, 'w') as f:
        json.dump(data_json, f)

def baca_dari_json(nama_file):
    try:
        with open(nama_file, 'r') as f:
            data = json.load(f)
            return [(judul, datetime.strptime(jam, '%H:%M').time()) for judul, jam in data]
    except FileNotFoundError:
        return []

def simpan_ke_history(nama_file, data_baru):
    try:
        with open(nama_file, 'r') as f:
            data_lama = json.load(f)
    except FileNotFoundError:
        data_lama = {}

    for j, t, tanggal_input in data_baru:
        if tanggal_input not in data_lama:
            data_lama[tanggal_input] = []

        jam_str = t.strftime('%H:%M')
        if (j, jam_str) not in data_lama[tanggal_input]:
            data_lama[tanggal_input].append((j, jam_str))

    with open(nama_file, 'w') as f:
        json.dump(data_lama, f)

def update_history():
    waktu_sekarang = datetime.now(timezone(timedelta(hours=7))).time()
    expired_data = antrian.dequeue_expired(waktu_sekarang)
    # Buat linked list hanya dari data yang masih valid
    linkedlist.from_array([(j, t) for j, t, _ in antrian.items])
    simpan_ke_json("jadwal_bioskop.json", linkedlist.to_array())

def baca_history_dengan_tanggal(nama_file):
    try:
        with open(nama_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def validasi_waktu(jam):
    try:
        h, m = map(int, jam.split(':'))
        if 0 <= h < 24 and 0 <= m < 60:
            return True
        return False
    except:
        return False


# === Main Program ===
linkedlist = LinkedList()
antrian = Queue()

data_awal = baca_dari_json("jadwal_bioskop.json")
for judul, jam in data_awal:
    linkedlist.insert(judul, jam)

linkedlist.sort_by('jam')
data_sorted = linkedlist.to_array()
linkedlist.from_array(data_sorted)
antrian.from_array(data_sorted)

waktu_sekarang = datetime.now(timezone(timedelta(hours=7))).time()
antrian.dequeue_expired(waktu_sekarang)
linkedlist.from_array([(j, t) for j, t, _ in antrian.items])
simpan_ke_json("jadwal_bioskop.json", linkedlist.to_array())

def menu():
    print("\n\n=======================================")
    waktu_sekarang = datetime.now(timezone(timedelta(hours=7))).time()
    print(f"||     Waktu Saat Ini: {waktu_sekarang.strftime('%H:%M')} WIB     ||")
    print("=======================================")
    print("||           MENU  BIOSKOP           ||")
    print("=======================================")
    print("1. Daftar Film 📝")
    print("2. Cari Jadwal Film")
    print("3. Tambah Jadwal Film")
    print("4. Edit Film ✍")
    print("5. Hapus Jadwal Film")
    print("6. Lihat History Film Lewat")
    print("0. Keluar")
    print("---------------------------------------")

while True:
    menu()
    pilih = input("Pilih menu: ")
    update_history()
    
    if pilih == '1':
        print("\n=======================================")
        print("||         Lihat Jadwal Film         ||")
        print("=======================================")
        print("1. Lihat daftar berdasarkan Judul")
        print("2. Lihat daftar berdasarkan Jam Tayang")
        
        opsi = input("Pilih opsi (1/2): ")
        while (opsi != '1' and opsi != '2'): 
            # kalau opsi bukan 1/2, masukkan opsi lain 
            print("⚠️  Pilihan tidak valid.")
            print("---------------------------------------")
            print("1. Lihat daftar berdasarkan Judul")
            print("2. Lihat daftar berdasarkan Jam Tayang")
            opsi = input("Pilih opsi (1/2): ")
        
        if opsi == '1':
            print("=======================================")
            print("||  Daftar Film (Berdasarkan Judul)  ||")
            print("=======================================")
            linkedlist.sort_by('judul')
            linkedlist.tampilkan_dengan_nomor('judul')
        elif opsi == '2':
            print("============================================")
            print("||  Daftar Film (Berdasarkan Jam Tayang)  ||")
            print("============================================")
            linkedlist.sort_by('jam')
            linkedlist.tampilkan_dengan_nomor('jam')
        print("============================================")

    elif pilih == '2':
        print("\n=======================================")
        print("||         Cari Jadwal Film          ||")
        print("=======================================")
        print("1. Cari berdasarkan Judul")
        print("2. Cari berdasarkan Jam Tayang")
        opsi = input("Pilih jenis pencarian (1/2): ")
        while (opsi != '1' and opsi != '2'):
            # kalau opsi bukan 1/2, masukkan opsi lain
            print("⚠️  Pilihan tidak valid.")
            print("---------------------------------------")
            print("1. Cari berdasarkan Judul")
            print("2. Cari berdasarkan Jam Tayang")
            opsi = input("Pilih jenis pencarian (1/2): ")
        found = False
        data = linkedlist.to_array()
        
        if opsi == '1': #judul
            keyword = input("✍  Masukkan kata kunci judul film: ")
            for judul, jam in data: # untuk mengecek aja
                if keyword.lower() in judul.lower():
                    found = True
            if found: # kalau ditemukan, beri pesan ini
                print("---------------------------------------")
                print(f"👍 Ditemukan film dengan kata kunci {keyword}")
            i=1
            for judul, jam in data: # munculkan data filmnya, dengan nomer
                if keyword.lower() in judul.lower():
                    print(f" {i}. {judul} - {jam.strftime('%H:%M')} WIB")
                    i = i+1
                    found = True
        elif opsi == '2': #jam
            keyword = input("✍  Masukkan kata kunci jam tayang (HH:MM): ")
            try:
                jam_dicari = datetime.strptime(keyword, '%H:%M').time()
                for judul, jam in data: # mengecek aja
                    if jam_dicari == jam:
                        found = True
                if found:
                    print("---------------------------------------")
                    print(f"👍 Ditemukan film dengan jam tayang {keyword} WIB")
                i=1
                for judul, jam in data:
                    if jam_dicari == jam:
                        print(f" {i}. {judul} - {jam.strftime('%H:%M')} WIB")
                        found = True
            except:
                print("Format jam tidak valid.")
        if not found:
            print("---------------------------------------")
            print("😖 Film tidak ditemukan.")
        print("=======================================") # penutup
    
    elif pilih == '3':
        print("\n=======================================")
        print("||       Tambahkan Jadwal Film       ||")
        print("=======================================")
        judul = input("Judul Film: ")
        jam_input = input("Jam Tayang (HH:MM): ")
        while not validasi_waktu(jam_input): # mengecek kevalidan waktu
            print("⚠️  Tolong masukkan waktu yang valid.")
            print("---------------------------------------")
            jam_input = input("Jam Tayang (HH:MM): ")
        
        jam = datetime.strptime(jam_input, '%H:%M').time()
        waktu_sekarang = datetime.now(timezone(timedelta(hours=7))).time()
        if jam <= waktu_sekarang:
            print("😖 Jadwal tidak bisa ditambahkan karena waktu sudah terlewat.")
            print("=======================================")
            continue # langsung keluar
        
        linkedlist.insert(judul, jam)
        linkedlist.sort_by('jam')
        data = linkedlist.to_array()
        antrian.from_array(data)
        simpan_ke_json("jadwal_bioskop.json", data)
        print("😄 Jadwal berhasil ditambahkan!")
        print("=======================================")

    elif pilih == '4':
        linkedlist.sort_by('judul')
        print("\n=======================================")
        print("||         Daftar Film - Edit        ||")
        print("=======================================")
        data = linkedlist.to_array()
        for idx, (judul, jam) in enumerate(data, 1):
            print(f" {idx}. {judul} - {jam.strftime('%H:%M')} WIB")
        try:
            print("---------------------------------------")
            index = int(input("Masukkan nomor film yang ingin diedit: "))
            while not (1 <= index <= len(data)):
                print("⚠️  Tolong masukkan nomor yang valid.")
                print("---------------------------------------")
                index = int(input("Masukkan nomor film yang ingin diedit: "))
            
            judul_baru = input("Judul Film Baru: ")
            jam_baru_input = input("Jam Tayang Baru (HH:MM): ")
            while not validasi_waktu(jam_baru_input): # mengecek kevalidan waktu
                print("⚠️  Tolong masukkan waktu yang valid.")
                print("---------------------------------------")
                jam_baru_input = input("Jam Tayang Baru (HH:MM): ")
            
            jam_baru = datetime.strptime(jam_baru_input, '%H:%M').time()
            waktu_sekarang = datetime.now(timezone(timedelta(hours=7))).time()
            if jam_baru <= waktu_sekarang: # jika input-an waktu baru, sudah terlewat
                print("Tidak dapat mengganti dengan jam yang sudah terlewat.")
                continue
                
            data[index - 1] = (judul_baru, jam_baru)
            linkedlist.from_array(data)
            linkedlist.sort_by('jam')
            antrian.from_array(linkedlist.to_array())
            simpan_ke_json("jadwal_bioskop.json", linkedlist.to_array())
            print("Jadwal berhasil diedit!")
        except ValueError:
            print("Input tidak valid.")
        print("=======================================")

    elif pilih == '5':
        linkedlist.sort_by('judul')
        print("\n=======================================")
        print("||     Daftar Film yang Tersedia     ||")
        print("=======================================")
        data = linkedlist.to_array()
        for idx, (judul, jam) in enumerate(data, 1):
            print(f" {idx}. {judul} - {jam.strftime('%H:%M')} WIB")
        try:
            print("---------------------------------------")
            index = int(input("Masukkan nomor film yang ingin dihapus: "))
            new_data = linkedlist.hapus_by_index_sorted_judul(index)
            linkedlist.from_array(new_data)
            linkedlist.sort_by('jam')
            antrian.from_array(new_data)
            simpan_ke_json("jadwal_bioskop.json", new_data)
        except ValueError:
            print("Input tidak valid.")
        print("=======================================")

    elif pilih == '6':
        print("\n=======================================")
        print("||            Riwayat Film           ||")
        print("=======================================")
        history = baca_history_dengan_tanggal("history_jadwal_bioskop.json")
        if not history:
            print("Belum ada history.")
        else:
            for tgl, daftar in sorted(history.items(), reverse=True):
                print(f"Tanggal: {tgl}")
                print("Riwayat Film:")
                for idx, (judul, jam) in enumerate(daftar, 1):
                    print(f" {idx}. {judul} - {jam} WIB")
                print("=======================================")

    elif pilih == '0':
        print("\n==================================================")
        print("||  Terima kasih telah menggunakan program ini. ||")
        print("==================================================\n")
        break
    
    else:
        print("⚠️  PILIHAN TIDAK VALID")
        print("=======================================")
    
    print("- Admin 🤍")


