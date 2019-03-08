<html lang="zh">
<head>
	<title>水印魔术师 | 把水印藏进图片</title>
    <?php
    if ($class == 'index'){
        echo '<link rel="stylesheet" type="text/css" href="./view/semantic.min.css">
<script src="./view/jquery-3.1.1.min.js"></script>
<script src="./view/semantic.min.js"></script>';
    }else{
        echo '<link rel="stylesheet" type="text/css" href="../../view/semantic.min.css">';
        echo '<script src="../../view/jquery-3.1.1.min.js"></script>';
        echo '<script src="../../view/semantic.min.js"></script>';
    }
    ?>

</head>
<body>
<div class="ui container">

    <div class="ui relaxed  grid">
        <div class="one column row" style="height: 150px"></div>
        <div class="three column row">
            <div class="column">
                <div class="ui left fixed vertical menu ">
                    <div class="item ">
                        <?php
                        if ($class == 'index'){echo '<img src="./images/logo.jpg" height="80px">';}else{ echo '<img src="../../images/logo.jpg" height="80px">';}
                        ?>
                    </div>
                    <?php
                    if ($class == 'index'){echo ' <a class="item"  href="./index.php">加水印</a>
                    <a class="item" href="./index.php/decode/">去水印</a>';}else{echo ' <a class="item"  href="../../index.php">加水印</a>
                    <a class="item" href="../../index.php/decode/">去水印</a>';}
                    ?>

                </div>
            </div>
            <div class="column">
                <?php  if ($class == 'index'){
                    echo ' <form id="encode" class="ui form" method="post" enctype="multipart/form-data" action="./index.php/encode">
                    <div class="field">
                        <label>输入文字作为水印</label>
                        <input type="text" name="b_words" placeholder="输入文字作为水印">
                        
	
			<div class="ui horizontal divider">或者</div>
			<label>选择一张图片作为水印</label>
                        <input type="file" name="b">
			<div class="ui divider"></div>

			<label>上传原图</label>
                        <input type="file" name="a">
			<label>密码</label>
			<input type="password" name="password">
                        <label> </label>
                        <label> </label>
                        <button  class="ui primary basic fluid button " >提交</button>
                        
                    </div>
                </form>';
                }
                ?>
               <?php if ($class == 'decode'){
                    if (file_exists('./images/b.png')) {
                        echo "<img src='../../images/b.png'><br >";

                        $myfile = fopen("./1.txt", "r") or die("Unable to open file!");
                        echo fread($myfile,filesize("./1.txt"));
                        fclose($myfile);
                    }else{
                        echo ' <form id=decode" class="ui form" method="post" enctype="multipart/form-data" action="../../index.php/decode">
                    <div class="field">
                        <label>上传有水印的图</label>
                        <input type="file" name="ab">
                        <label>上传原图</label>
                        <input type="file" name="a">
			<label>密码</label>
                        <input type="password" name="password">
                        <label> </label>
                        <button  class="ui primary basic fluid button " >提交</button>
                 
                    </div>
                </form>';
                    }
                }
                ?>
            </div>
            <div class="column"></div>
        </div>

    </div>
</div>

</body>
</html>
