#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import glob
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

# Konfigurasi lebar tampilan
LEBAR = 56

# Path database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATHS = [
    "database/denpasar/database2_denpasar1.json",
    "database/denpasar/database2_denpasar2.json",
    "database/jambi/database1_jambi.json",
    "database/jambi/database1_jambi2.json"
]

def tampilkan_header():
    """ASCII Art ELANG dengan warna biru"""
    ascii_art = f"""
{Fore.BLUE}███████╗██╗      █████╗ ███╗   ██╗ ██████╗ 
{Fore.BLUE}██╔════╝██║     ██╔══██╗████╗  ██║██╔════╝ 
{Fore.BLUE}█████╗  ██║     ███████║██╔██╗ ██║██║  ███╗
{Fore.BLUE}██╔══╝  ██║     ██╔══██║██║╚██╗██║██║   ██║
{Fore.BLUE}███████╗███████╗██║  ██║██║ ╚████║╚██████╔╝
{Fore.BLUE}╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝{Style.RESET_ALL}
    """
    print(ascii_art)
    print(f"{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}")
    print(f"{Fore.RED}developed by : @alzzdevmaret{Style.RESET_ALL}".center(LEBAR))
    print(f"{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}\n")

def muat_semua_data():
    """Memuat data dari semua file JSON dalam konfigurasi"""
    semua_data = []
    total_file = 0
    
    print(f"{Fore.CYAN}Memuat database...{Style.RESET_ALL}")
    
    for path in DB_PATHS:
        full_path = os.path.join(BASE_DIR, path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ambil array data_penduduk
                    penduduk = data.get("data_penduduk", [])
                    
                    # Tambahkan info asal database ke setiap record
                    for orang in penduduk:
                        orang['_sumber_db'] = path
                        # Parse kota dari path atau dari data
                        if 'denpasar' in path.lower():
                            if 'kota' not in orang or not orang.get('kota'):
                                orang['kota'] = 'Denpasar'
                        elif 'jambi' in path.lower():
                            if 'kota' not in orang or not orang.get('kota'):
                                orang['kota'] = 'Jambi'
                    
                    semua_data.extend(penduduk)
                    total_file += 1
                    print(f"{Fore.GREEN}✓ {path}: {len(penduduk)} data{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}✗ Error loading {path}: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ File tidak ditemukan: {path}{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Total {len(semua_data)} data dari {total_file} database{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}\n")
    
    return semua_data

def cari_orang(data, kata_kunci):
    """Mencari orang berdasarkan nama lengkap (case-insensitive)"""
    kata_kunci = kata_kunci.lower().strip()
    hasil = []
    
    for orang in data:
        nama = orang.get("nama_lengkap", "").lower()
        if kata_kunci in nama:
            hasil.append(orang)
    
    # Urutkan berdasarkan nama
    hasil.sort(key=lambda x: x.get("nama_lengkap", ""))
    return hasil

def format_npwp(npwp):
    """Format NPWP agar lebih rapi"""
    if not npwp or npwp == "Belum memiliki" or npwp == "Tidak ditemukan":
        return f"{Fore.YELLOW}{npwp}{Style.RESET_ALL}"
    return npwp

def format_nisn(nisn):
    """Format NISN agar lebih rapi"""
    if not nisn or nisn == "Tidak ditemukan":
        return f"{Fore.YELLOW}{nisn}{Style.RESET_ALL}"
    return nisn

def tampilkan_detail(orang):
    """Menampilkan detail satu orang dengan format rapi"""
    # Info sumber database
    sumber = orang.get('_sumber_db', 'Unknown')
    kota_display = orang.get('kota', 'Unknown')
    
    print(f"\n{Fore.BLUE}{'=' * LEBAR}{Style.RESET_ALL}")
    
    # Header dengan ikon berdasarkan kota
    if 'denpasar' in sumber.lower():
        icon = "🌊"
    else:
        icon = "🌳"
    
    # Nama besar
    nama = orang.get('nama_lengkap', 'N/A').upper()
    print(f"{Fore.RED}{icon} {nama} {icon}{Style.RESET_ALL}".center(LEBAR))
    
    # Info database
    db_info = f"Database: {os.path.basename(sumber)}"
    print(f"{Fore.CYAN}{db_info}{Style.RESET_ALL}".center(LEBAR))
    print(f"{Fore.BLUE}{'-' * LEBAR}{Style.RESET_ALL}")

    # Fungsi bantu cetak field
    def cetak(label, nilai, warna_nilai=Fore.WHITE):
        if nilai and str(nilai).strip() and str(nilai) not in ["N/A", "Tidak ditemukan", "Belum memiliki"]:
            print(f"  {Fore.BLUE}{label:<14}{Style.RESET_ALL} {warna_nilai}{nilai}{Style.RESET_ALL}")

    # Data inti
    cetak("Nama", orang.get('nama_lengkap', 'N/A'))
    
    if orang.get('nik'):
        cetak("NIK", orang.get('nik'))
    
    if orang.get('nisn'):
        cetak("NISN", format_nisn(orang.get('nisn')))
    
    # Tempat/tanggal lahir
    ttl = ""
    if orang.get('tempat_lahir'):
        ttl += orang.get('tempat_lahir')
    if orang.get('tanggal_lahir'):
        if ttl:
            ttl += ", "
        # Format tanggal jika perlu
        tgl = orang.get('tanggal_lahir')
        try:
            if len(tgl) == 10:
                tgl_obj = datetime.strptime(tgl, "%Y-%m-%d")
                ttl += tgl_obj.strftime("%d-%m-%Y")
            else:
                ttl += tgl
        except:
            ttl += tgl
    if ttl:
        cetak("TTL", ttl)
    
    if orang.get('umur'):
        cetak("Umur", f"{orang.get('umur')} tahun")
    
    if orang.get('agama'):
        # Tambah icon agama
        agama = orang.get('agama')
        if "Hindu" in agama:
            agama = "🕉️ " + agama
        elif "Islam" in agama:
            agama = "☪️ " + agama
        elif "Kristen" in agama or "Katolik" in agama:
            agama = "✝️ " + agama
        elif "Buddha" in agama:
            agama = "☸️ " + agama
        elif "Konghucu" in agama:
            agama = "☯️ " + agama
        cetak("Agama", agama, Fore.CYAN)
    
    if orang.get('suku'):
        cetak("Suku", orang.get('suku'))
    
    if orang.get('kota'):
        cetak("Kota", orang.get('kota'))
    
    if orang.get('npwp'):
        cetak("NPWP", format_npwp(orang.get('npwp')))
    
    print(f"{Fore.BLUE}{'=' * LEBAR}{Style.RESET_ALL}")

def tampilkan_statistik(data):
    """Menampilkan statistik database"""
    if not data:
        return
    
    # Hitung statistik
    total = len(data)
    kota_counts = {}
    agama_counts = {}
    suku_counts = {}
    
    for orang in data:
        kota = orang.get('kota', 'Unknown')
        agama = orang.get('agama', 'Unknown')
        suku = orang.get('suku', 'Unknown')
        
        kota_counts[kota] = kota_counts.get(kota, 0) + 1
        agama_counts[agama] = agama_counts.get(agama, 0) + 1
        suku_counts[suku] = suku_counts.get(suku, 0) + 1
    
    print(f"\n{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📊 STATISTIK DATABASE{Style.RESET_ALL}".center(LEBAR))
    print(f"{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}Total Data: {total}{Style.RESET_ALL}")
    
    # Kota
    print(f"\n{Fore.YELLOW}Kota:{Style.RESET_ALL}")
    for kota, count in sorted(kota_counts.items()):
        if kota and kota != "Unknown":
            persen = (count / total) * 100
            bar = "█" * int(persen / 5)
            print(f"  {kota:<12} {count:3d} data {Fore.GREEN}{bar}{Style.RESET_ALL}")
    
    # Agama
    print(f"\n{Fore.YELLOW}Agama:{Style.RESET_ALL}")
    for agama, count in sorted(agama_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        if agama and agama != "Unknown":
            persen = (count / total) * 100
            print(f"  {agama:<12} {count:3d} data ({persen:.1f}%)")
    
    print(f"{Fore.BLUE}{'─' * LEBAR}{Style.RESET_ALL}")

def main():
    tampilkan_header()
    
    # Muat semua data
    semua_data = muat_semua_data()
    if not semua_data:
        print(f"{Fore.RED}✗ Tidak ada database yang ditemukan!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Pastikan struktur folder:{Style.RESET_ALL}")
        print("  database/")
        print("  ├── denpasar/")
        print("  │   ├── database2_denpasar1.json")
        print("  │   └── database2_denpasar2.json")
        print("  └── jambi/")
        print("      ├── database1_jambi.json")
        print("      └── database1_jambi2.json")
        return
    
    # Tampilkan statistik
    tampilkan_statistik(semua_data)
    
    # Mode pencarian
    while True:
        print()
        keyword = input(f"{Fore.RED}→{Style.RESET_ALL} Cari nama {Fore.BLUE}(atau 'exit'){Style.RESET_ALL}: ").strip()
        
        if keyword.lower() == 'exit':
            print(f"\n{Fore.GREEN}Terima kasih telah menggunakan ELANG!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}© @alzzdevmaret{Style.RESET_ALL}")
            break
        
        if not keyword:
            continue
        
        # Cari data
        hasil = cari_orang(semua_data, keyword)
        
        if not hasil:
            print(f"{Fore.RED}✗ Tidak ditemukan '{keyword}'{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✓ Ditemukan {len(hasil)} orang:{Style.RESET_ALL}")
            
            # Tampilkan daftar dengan nomor
            for idx, orang in enumerate(hasil, 1):
                # Tandai asal kota
                kota = orang.get('kota', '')
                if kota:
                    print(f"  {Fore.BLUE}[{idx:2d}]{Style.RESET_ALL} {orang.get('nama_lengkap', 'N/A')} {Fore.CYAN}({kota}){Style.RESET_ALL}")
                else:
                    print(f"  {Fore.BLUE}[{idx:2d}]{Style.RESET_ALL} {orang.get('nama_lengkap', 'N/A')}")
            
            # Jika hanya 1 hasil, langsung tampilkan detail
            if len(hasil) == 1:
                tampilkan_detail(hasil[0])
            else:
                print()
                pilihan = input(f"{Fore.RED}→{Style.RESET_ALL} Lihat nomor (atau 'all', '0' kembali): ").strip()
                
                if pilihan.lower() == 'all':
                    for orang in hasil:
                        tampilkan_detail(orang)
                        if orang != hasil[-1]:
                            input(f"{Fore.CYAN}Tekan Enter untuk lanjut...{Style.RESET_ALL}")
                elif pilihan.isdigit():
                    idx = int(pilihan) - 1
                    if 0 <= idx < len(hasil):
                        tampilkan_detail(hasil[idx])
                    elif int(pilihan) == 0:
                        continue
                    else:
                        print(f"{Fore.RED}✗ Nomor tidak valid{Style.RESET_ALL}")
                elif pilihan:
                    print(f"{Fore.RED}✗ Pilihan tidak dikenali{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program dihentikan...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Sampai jumpa!{Style.RESET_ALL}")
