## Judul Soal
Bizarre Image

## Deskripsi Soal

>It's Winter now, well nothing special about it. But, for some reason I got a bizarre stuff last night. No wonder thou 
---

## Hint
- When I checked it, there were a log of BLE File transfer & Keystrokes from a Bluetooth Keyboard
- Short story, I got an Animated PNG file. But somehow, I couldn't load the image properly on my Browser

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

```bash
❯ tshark -r ble.pcap -Y 'btrfcomm.cr eq 1 && data.len > 50' -Tfields -e data > data

❯ tshark -r ble.pcap -Y 'btrfcomm.cr eq 1 && data.len > 50' -Tfields -e data.len > length

❯ python2 rfcomm.py

# Open vim, enter passphrase
# Type ":set key=", then save
❯ vim fixed.png

❯ file fixed.png
fixed.png: PNG image data, 580 x 580, 8-bit colormap, non-interlaced

❯ mkdir frames && cp fixed.png frames/
❯ cd frames && apngdis fixed.png

APNG Disassembler 2.9

Reading 'fixed.png'...
extracting frame 1 of 811
extracting frame 2 of 811
extracting frame 3 of 811
extracting frame 4 of 811
extracting frame 5 of 811

..
..
extracting frame 807 of 811
extracting frame 808 of 811
extracting frame 809 of 811
extracting frame 810 of 811
extracting frame 811 of 811
all done

❯ zbarimg apng*.png | cut -c9- | tr -d '\n' 

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean quis dui purus. Praesent porttitor neque nec nunc scelerisque, convallis rutrum elit euismod. Maecenas laoreet euismod posuere. Sed tincidunt mauris ut neque cursus, id laoreet odio lobortis. Vivamus nec volutpat neque, auctor aliquet purus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec sit amet enim ullamcorper, ultrices arcu sit amet, commodo nibh. Morbi non lorem et quam tempor mollis ut et enim. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla ante mauris, tempor at volutpat ut, imperdiet id eros. In consequat lacinia dui eget tristique.Finally, the flag is redmask{f1le_transf3rs_0ver_bl3_ar3_k1nda_fun_but_tr1cky_3nough_e23df14f}

```

<br>

## Flag
redmask{f1le_transf3rs_0ver_bl3_ar3_k1nda_fun_but_tr1cky_3nough_e23df14f}