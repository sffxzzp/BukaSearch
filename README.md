# BukaSearch

一个用来搜索布卡漫画的 Python 脚本。

搜索结果会导出到 `output.html`，建议手机上用浏览器打开，这样可以直接点「用App打开」然后收藏了。

当然直接用 `sqlite` 搜索也是可以的。

已经用 Travis 部署了每周自动更新。

文件中 `db.py` 是给用来给 Travis 自动更新数据库的，当然你要本地自己更新也行。

`buka.py` 才是用来搜索的。
