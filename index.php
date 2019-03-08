<?php

$root = $_SERVER['SCRIPT_NAME'];
$request = $_SERVER['REQUEST_URI'];
$URI = array();
//获得index.php 后面的地址
$url = trim(str_replace($root, '', $request), '/');
if (empty($url)) {
    //默认控制器和默认方法
    $class = 'index';
    $func = 'welcome';
} else {
    $URI = explode('/', $url);
    //如果function为空 则默认访问index
    if (count($URI) < 2) {
        $class = $URI[0];
        $func = 'index';
    } else {
        $class = $URI[0];
        $func = $URI[1];
    }
}

$obj = new $class();
$obj->$func($class);
class Stand{
    public function upload_a_png(){
        if ($_FILES){
            if ((($_FILES["a"]["type"] == "image/png")))
        {
            if ($_FILES["a"]["error"] > 0)
            {
                echo "Return Code: " . $_FILES["a"]["error"] . "<br />";
            }
            else
            {
                move_uploaded_file($_FILES["a"]["tmp_name"], "images/a.png");
            }
        }
        else
        {
            echo "没传png图片！";
        }
        }
    }
    public function upload_ab_png(){
        if ($_FILES){
            if ((($_FILES["ab"]["type"] == "image/png")))
        {
            if ($_FILES["ab"]["error"] > 0)
            {
                echo "Return Code: " . $_FILES["ab"]["error"] . "<br />";
            }
            else
            {
                move_uploaded_file($_FILES["ab"]["tmp_name"], "images/ab.png");
            }
        }
        else
        {
            echo "没传png图片！";
        }
    }
    }
}
class Encode extends Stand {

    public function index($class){
        $b_words='';
        $password = '';

        Encode::upload_a_png();

        if ($_FILES){
            if ((($_FILES["b"]["type"] == "image/png")))
            {
                if ($_FILES["b"]["error"] > 0)
                {
                    echo "Return Code: " . $_FILES["ab"]["error"] . "<br />";
                }
                else
                {
                    move_uploaded_file($_FILES["ab"]["tmp_name"], "images/b.png");
                }
            }
            else
            {
                echo " ";
            }
        }


        if($_POST['b_words']){
            $b_words= $_POST['b_words'];
        }

        if($_POST['password']){
            $password= $_POST['password'];
        }

	if(strlen($b_words)>1){
		$flag = 0;
		$exe = 'python3 /var/www/html/encoder.py /var/www/html/images/a.png '.$flag.'  '.$b_words.' /var/www/html/images/ab.png '.$password;
		system($exe);
	}else{
		$flag = 1;
		$exe = 'python3 /var/www/html/encoder.py /var/www/html/images/a.png '.$flag.' /var/www/html/images/b.png   /var/www/html/images/ab.png '.$password;
		system($exe);
	}

        if (file_exists('./images/ab.png')) {
           echo "<a href='../images/ab.png'>点此下载加水印之后的图片</a>";
         }
    }

    

}
class Decode extends Stand{

    public function index($class){
        $password = '';
        system('rm -rf /var/www/html/images/a.png /var/www/html/images/ab.png /var/www/html/images/b.png /var/www/html/1.txt');
 
        Decode::upload_a_png();
        Decode::upload_ab_png();
        if($_POST['password']){
            $password= $_POST['password'];
        }

       
       system('python3 /var/www/html/decoder.py /var/www/html/images/a.png /var/www/html/images/ab.png /var/www/html/images/b.png '.$password);
     
        include('./view/theme.php');
        
    }

}
class Index {
    public function welcome($class){
	system('rm /var/www/html/images/a.png /var/www/html/images/ab.png /var/www/html/images/b.png');
        include('./view/theme.php');
    }
}
?>
