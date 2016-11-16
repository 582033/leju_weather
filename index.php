<?php
class pm{
    public $content;
    public function __construct(){
        exec('cat ./json.data', $result);
        $this->content = count($result) > 0 ? $result[0] : "get data error";
    }

    public function show(){
        echo $this->content;
    }
}
?>

<?php
if($_SERVER['REQUEST_METHOD'] == 'POST'){
    $pm = new pm();
    $pm->show();
}else{
?>
<html>
    <head>
        <script src="http://libs.baidu.com/jquery/1.9.0/jquery.js"></script>
    </head>
    <title>乐居气象监测站</title>
    <link rel="icon" href="favicon.ico">
    <style>
        div {font-size:15px; line-height:20px;}
        #time {margin-top:20px;}
    </style>
    <body>
        <h3>室内:</h3>
        <div id="pm">Reading...</div>
        <div id="t"></div>
        <div id="h"></div>
        <h3>室外:</h3>
        <div id="weather">Reading...</div>
        <div id="outdoor_pm"></div>
        <div id="time"></div>
    </body>
<script>
    setInterval(function(){
        $.ajax({
            url     : './',
            type    : 'post',
            dataType : 'json',
            success: function(result){
                console.log(result);
                var quality = get_quality(result.dustdensity);
                $('#pm').text("PM2.5: " + result.dustdensity + " ug/m3 (" + quality + ")");
                $('#t').text("温度: " + result.temperature + " ℃");
                $('#h').text("湿度: " + result.humidity + "% RH");
                $('#weather').text(result.weather);
                $('#outdoor_pm').text(result.outdoor_pm);
                $('#time').text("数据最后更新时间: " + result.time);
            }
        });
    }, 2000);
    function get_quality(val){
        val = parseInt(val);
        var _color, _str;
        if(val<35){                     //优
            _str = "空气质量优";
        }
        else if(val>35 && val<75){    //良
            _str = "空气质量良";
        }
        else if(val>75 && val<115){   //轻度污染
            _str = "轻度污染";
        }
        else if(val>115 && val<150){   //中度污染
            _str = "中度污染";
        }
        else if(val>150 && val<250){   //重度污染
            _str = "重度污染";
        }
        else if(val>250){                    //严重污染
            _str = "严重污染";
        }
        else{
            _str = "未知错误";
        }
        return _str;
    }

</script>
</html>
<?php }?>
