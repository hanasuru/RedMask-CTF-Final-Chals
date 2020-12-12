## Judul Soal
Bizarre Image

## Deskripsi Soal

>It's Winter now, well nothing special about it. But, for some reason I got a bizarre stuff last night. No wonder thou 
---

## Penjelasan Penyelesaian Soal
- Diberikan `network packet` bernama `ble.pcap`, yang memuat `btchi_acl` dari RFCOMM ke OBEX dan `bthid` yang memuat HID keystroke dari Bluetooth keyboard.
- Kurang lebih user melakukan device scanning, pairing device, connecting device, dan file encryption terhadap `flag.png` menggunakan `vimcrypt`. Dari sini, diketahui pula bahwa passphrase yang benar adalah `a_long_long_long_password`
- Dengan melakukan stripping 6 bytes pada data `bhthci_acl` diperoleh `encrypted_data` dari `flag.png`
- Setelah melakukan dekripsi file, diperoleh hierarchy `APNG file` namun dengan `frame block` yang teracak
- Dilakukan proses sorting pada frame block sehingga diperoleh `APNG file` yang valid
- Dilakukan ekstraksi `APNG file` sehingga diperoleh `811 frame image`
- Terakhir dilakukan QR-decode untuk setiap `frame image` yang diperoleh dari proses sebelumnya

## Solver
On-progress

<br>

## Flag
redmask{f1le_transf3rs_0ver_bl3_ar3_k1nda_fun_but_tr1cky_3nough_e23df14f}