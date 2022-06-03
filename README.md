# webserver

## Usage
* `python webserver.py [port] [/path/to/web/root]`
* 在Linux下部署可将*webserver.service*（注意更改第十行运行指令）放入/etc/systemd/system/，之后`sudo systemctl daemon-reload`并且`sudo systemctl start webserver.service`即可运行。`sudo systemctl enable webserver.service`设置开机自启动。
* *ls_site.py*用于生成*index.html*，可在`crontab -e`中添加定时执行任务自动更新*index.html*。（本人不太会前端，可自行更改*ls_site.py*的内容）

## Notes
* ~~包含中文的内容需使用gbk编码，否则会出现乱码~~。
* html文件新增一行自动解析编码，更新为utf-8编码。
