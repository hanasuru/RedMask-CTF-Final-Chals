# poggers

Reverse go binary.

## Deskripsi Soal

<img src="https://emoji.gg/assets/emoji/Poggers.png" width="64px" height="64px" alt="Poggers">

## Hint Soal

- [Gray code](https://en.wikipedia.org/wiki/Gray_code)

## Penjelasan Soal

Probset berasumsi peserta bisa ngereverse binary go sehingga tidak perlu dijelaskan di sini <img src="https://emoji.gg/assets/emoji/6158_PepeLaugh.png" width="32px" height="32px" alt="PepeLaugh">

Tiga bagian penting:

1. Fungsi sus hanya ngeshuffle posisi karakter. Reverse sus:

```python
def revSus(s):
    v0 = s[len(s) / 2:][::-1]
    v1 = s[:len(s) / 2][::-1]
    return ''.join([i + j for i, j in zip(v0, v1)])
```

2. Gray code `x xor (x >> 1)`. Reverse gray code tinggal pakai `libnum.rev_grey_code`.

3. RotateLeft64 -> RotateRight64.
