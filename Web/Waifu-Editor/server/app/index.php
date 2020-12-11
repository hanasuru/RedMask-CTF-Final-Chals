<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Waifu Editor</title>
</head>
<body>
    <h1>Upload waifu anda</h1>
    <form action="/process.php" method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" name="upload" value="Upload">
    </form>
    <p>*Hanya bisa mengupload file .jpg dan .png</p>
</body>
</html>