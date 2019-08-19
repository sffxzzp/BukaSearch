<?php
	function geturl($url){
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		$output = curl_exec($ch);
		curl_close($ch);
		return $output;
	}

	require('Medoo.php');
	$title = '布卡搜索';
	use Medoo\Medoo;
	$database = new Medoo([
		'database_type'	=>	'sqlite',
		'database_file'	=>	'buka.db'
	]);
	$dbTime = $database->query('select des from info where id = 0;')->fetch()["des"];
	$startId = (int)$database->query('select id from info order by id desc limit 1;')->fetch()["id"];
	preg_match('/\/detail\/(\d*).html/i', geturl('http://www.buka.cn/category/12084/%E6%9C%80%E8%BF%91%E4%B8%8A%E6%96%B0.html'), $newestId);
	$newestId = (int)$newestId[1];
	if ($_POST) {
		$searchKey = $_POST['searchKey'];
		$searchRes = $database->query('select * from info where name like "%'.$searchKey.'%" or author like "%'.$searchKey.'%";')->fetchAll();
		$output = '';
		for ($i=0;$i<count($searchRes);$i++) {
			$output .= '<div class="dispanel"><table border="1"cellspacing="0"><tr><td rowspan="3" style="width:140px;"><img class="img"src="'.urldecode($searchRes[$i]['img']).'"/></td><td><span class="title"><a target="_blank" href="http://www.buka.cn/detail/'.$searchRes[$i]['id'].'.html">'.$searchRes[$i]['name'].'</a></span><span class="app"><a target="_blank" href="buka://detail/manga/'.$searchRes[$i]['id'].'">在App中打开</a></span></td></tr><tr><td><span class="author">作者：'.$searchRes[$i]['author'].'</span></td></tr><tr><td><span class="description">'.$searchRes[$i]['des'].'</span></td></tr></table></div>'; 
		}
	}
?>
<html>
	<head>
		<title><?php echo isset($searchKey)?$searchKey.' - '.$title:$title;?></title>
		<style>
			input {float: left;}
			a:link{text-decoration:none}
			.dispanel{margin:2% 0}
			.dispanel>table{width:100%}
			.app{float:right}
			.img{width:140px}
		</style>
	</head>
	<body style="width: 80%; margin: auto; text-align: center;">
		<h1>布卡搜索</h1>
		<pre>数据库更新日期：<?php echo $dbTime;?>    数据库最新id：<?php echo $startId;?>    网站最新id：<?php echo $newestId;?></pre>
		<div>
			<form action="" method="post">
				<input type="text" name="searchKey" placeholder="输入要搜索的 作品名称 或 作者名称" id="searchInput" style="width: 95%;">
				<input type="submit" value="提交" style="width: 5%;">
			</form>
		</div>
		<div class="result">
			<?php echo isset($output)?$output:''; ?>
		</div>
	</body>
</html>
