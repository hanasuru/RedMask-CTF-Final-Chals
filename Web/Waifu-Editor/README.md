## Judul Soal
Waifu Editor

## Deskripsi Soal
Saya sedang membuat web untuk merubah gambar menjadi grayscale menggunakan imagemagick dengan versi yang cukup baru. <br>
Tolong carilah sebuah bug pada web saya, sebagai bukti anda dapat menembus sistem, saya menaruh sebuah flag. <br>
Tolong berikan flagnya jika anda berhasil menembusnya. <br>


---

## Penjelasan Penyelesaian Soal
- Terdapat vuln rce pada imagemagick (https://insert-script.blogspot.com/2020/11/imagemagick-shell-injection-via-pdf.html)
- Hanya dapat mengupload jpg dan png, namun tidak bisa svg
- Sehingga untuk dapat mengeksekusi svg, kita perlu memberi nama file yang akan kita upload dengan `imageapapun.jpg svg:payloadnya.jpg` menggunakan burp suite yang nantinya nama tersebut akan diproses oleh perintah `convert` pada `process.php`