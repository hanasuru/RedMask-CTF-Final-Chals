<?php

if($_POST['upload']){
    $ekstensi_diperbolehkan	= array('png','jpg');
    $filename = $_FILES['file']['name'];
    $x = explode('.', $filename);
    $ekstensi = strtolower(end($x));
    $ukuran	= $_FILES['file']['size'];
    $file_tmp = $_FILES['file']['tmp_name'];
    $outfilename = md5($filename . time() . 'out');
    $path = 'uploads/'.$filename;
    $outpath = 'uploads/'.$outfilename.'.jpg';

    if(in_array($ekstensi, $ekstensi_diperbolehkan) === true){
        if($ukuran < 1044070){			
            $antiHeker = [
                '$', '\\', '-', '(', ')', '{', '}', ';', '#', '?', '<', '>',
                '|', '&', '%', '^', '@', '!', '=', '+', ',', '[', ']',
                '\'', '"', '/', '*', '`', '~'
            ]; // karena ngehek sangat tidak baik ^_^

            // Musnahkeun, karungkeun, amankeun hal yang berbahaya
            foreach ($antiHeker as $value) {
                $filename = str_replace($value, '', $filename);
            }

            move_uploaded_file($file_tmp, $path);

            // Biar makin aman xixixi
            $cmd = escapeshellcmd("convert $filename -set colorspace Gray -separate -average $outfilename".'.jpg');
            shell_exec('cd /var/www/html/uploads && ' . $cmd);

            header('Content-Type: image/jpeg');
            echo file_get_contents($outpath);
        }else{
            echo 'UKURAN FILE TERLALU BESAR';
        }
    }else{
        echo 'EKSTENSI FILE YANG DI UPLOAD TIDAK DI PERBOLEHKAN';
    }
}