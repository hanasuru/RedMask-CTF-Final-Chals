<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>

    <style>
        body, html {
            height: 100%;
        }

        .center {
            text-align: center;
        }

        .bg {
            background-image: url("assets/genshinbg.jpg");

            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
    </style>
</head>
<body class="center bg">
    <h1 style="color: white;">Calculator</h1>
    <form action="/index.php" method="GET">
        <input type="text" name="calc">
        <input type="submit" value="Hitung">
    </form>
    <?php
        if (isset($_GET['calc'])):
            $calc = $_GET['calc'];
    ?>
        <div style="color: white; font-weight: bold; text-shadow: 2px 2px #000000;">
            <?php 
                eval("echo '<h3>Hasil: ' . ($calc) . '</h3>';");
            ?>
        </div>
    <?php endif; ?>
</body>
</html>