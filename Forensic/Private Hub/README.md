## Judul Soal
Private Hub

## Deskripsi Soal

>I deployed my own docker hub the other day. After a while, I started to push some webservices. But then something fishy happened <br><br>https://drive.google.com/file/d/10IF7-T42ZgzjN5kJwLaXu1VLawFmX8Hq/view?usp=sharing
---

## Penjelasan Penyelesaian Soal
- Diberikan dua buah `network packet`, yakni `blob.pcap` & `log.pcap`
- Pada `blob.pcap` diperoleh manifest data beserta `rootfs` dari Docker Images yang memuat flask app, binary `_`, dan private key `key`.
- Selain itu pada `manifest file`, diperoleh `Layer command` yang memuat perintah `wget -Oz.go https://cutt.ly/lhOaBpk` yang mana mengunduh source code dari binary `_`
- Sesaat setelah melakukan sedikit pengecekan terhadap source code , diketahui bahwa binary merupakan `custom dns server` yang menerima input berupa URL. Kemudian memberikan response data berupa `dnscrypt` + `size of data` + `encrypted data` + `crc32 of data`. Diketahui pula bahwa encrypted data memuat block byte yang dienkripsi menggunakan private key `key`
- Dengan acuan `private key`, dilakukan dekripsi `encrypted data`. Dengan demikian, diketahui bahwa data memuat `response` dari `Blind SSTI` dari `app.py`
- Berbekal acuan tersebut, dilakukan seleksi untuk setiap `HTTP 200` response & `text` value yang memuat string `int`
- Hasilnya, diperoleh `flag.zip` & `password` yang memuat informasi dari `flag`

## Solver
On-progress

<br>

## Flag
redmask{http_api_reque5t_0ver_quer1ed_txt_d0main_n4me_5erv3r} 
