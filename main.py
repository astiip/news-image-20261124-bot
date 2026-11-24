"""Menyalin gambar entri ke folder keluaran make.fun.

Skrip kecil ini cuma punya satu tugas: mengambil berkas gambar yang
sudah jadi di samping skrip ini, lalu menaruh salinannya di direktori
yang ditunjuk lewat variabel lingkungan.
"""

import os
import sys
from pathlib import Path


NAMA_GAMBAR = "entry.png"
NAMA_VAR_TUJUAN = "MAKEFUN_OUTPUT_DIR"


def cari_folder_tujuan() -> Path:
    """Ambil direktori tujuan dari variabel lingkungan.

    Kalau variabelnya belum diisi, beri tahu pengguna lewat pesan
    kesalahan dan hentikan program dengan kode keluar gagal.
    """
    nilai = os.environ.get(NAMA_VAR_TUJUAN, "").strip()
    if not nilai:
        print(
            f"Gagal: variabel lingkungan {NAMA_VAR_TUJUAN} belum diisi.",
            file=sys.stderr,
        )
        print(
            "Isi dulu variabel itu dengan folder tujuan sebelum menjalankan skrip ini.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return Path(nilai)


def salin_gambar_entri(folder_tujuan: Path) -> Path:
    """Pindahkan isi gambar entri ke dalam folder tujuan.

    Folder tujuan dibuat dulu kalau belum ada, lalu isi berkas
    gambar dibaca dan ditulis ulang ke lokasi barunya.
    """
    folder_tujuan.mkdir(parents=True, exist_ok=True)
    asal = Path(__file__).resolve().parent / NAMA_GAMBAR
    tujuan = folder_tujuan / NAMA_GAMBAR
    tujuan.write_bytes(asal.read_bytes())
    return tujuan


def jalankan() -> int:
    """Jalankan alur utama dan laporkan hasilnya."""
    folder_tujuan = cari_folder_tujuan()
    hasil = salin_gambar_entri(folder_tujuan)
    print(f"Berhasil: gambar entri tersalin ke {hasil}")
    return 0


if __name__ == "__main__":
    raise SystemExit(jalankan())
