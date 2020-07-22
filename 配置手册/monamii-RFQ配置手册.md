#### 一、获取关键字：

经邓可韦（产品经理）发来的关键字表格进行创建。

#### 二、拉取线上RFQ代码段+配置：

1. 打开：https://bitbucket.org/monamii-cn1/monamii-rfq/src/develop/

2. 打开pycharm+添加GIT

3. pycharm中clone :https://Xbhog@bitbucket.org/monamii-cn1/monamii-rfq.git

4. 创建.sh文件（RFQ）----具体命名规范参照代码段中进行

5. ```sh
   scrapy runspider ../rfq.py -a keyword="关键字" -a table_name=yoga_mat -a webhook_url="地址" --logfile ${log_file}
   ```

6. 根据所给关键字创建群中的机器人名字，自定义关键字（monamii-RFQ）

7. 将关键字以及获取到的webhook添加到（5、）中的“关键字”、“地址”中，进行一一对应

8. “table_name”  ---->设置为该关键字命名 ；如：【办公文教用品（Office_Supplies）】

9. 文件格式：

   ```sh
   #电动汽车的充电器vv
   
   #ev charger
   #portable ev charger
   #ev wallbox
   #ev charging box
   #ev charging station
   
   scrapy runspider ../rfq.py -a keyword="ev charger" -a table_name=charger -a webhook_url="https://oapi.dingtalk.com/robot/send?access_token=9b1f3f8ee8b16cc4e5044f22d3aa35f77e910eda410cac698674131794d21d7e" --logfile ${log_file}
   scrapy runspider ../rfq.py -a keyword="portable ev charger" -a table_name=charger -a webhook_url="https://oapi.dingtalk.com/robot/send?access_token=d88934a6707e8877caacf23ca63139b04348d8b6c716c2a92c248e0b018646a7" --logfile ${log_file}
   scrapy runspider ../rfq.py -a keyword="ev charging box" -a table_name=charger -a webhook_url="https://oapi.dingtalk.com/robot/send?access_token=5561d60d226ccfb3f3184a7c0e3bb9f189ab407ac9ed2b6ecccde3a3f21038a9" --logfile ${log_file}
   scrapy runspider ../rfq.py -a keyword="ev wallbox" -a table_name=charger -a webhook_url="https://oapi.dingtalk.com/robot/send?access_token=f9c1d1ffb4238a1a75cefa617a35aca50cd661cc9f80739de1438636a57b4d21" --logfile ${log_file}
   scrapy runspider ../rfq.py -a keyword="ev charging station" -a table_name=charger -a webhook_url="https://oapi.dingtalk.com/robot/send?access_token=c3a4de58b57bb4c486a4aebc36acda60d50f127db49b9ac63c3d4b6f9a541e7a" --logfile ${log_file}
   
   #-----------------------------------------------------------------------------------------------------
   ```

#### 三、线上操作：

1. 打开xshell

2. cd  /usr/local/monamii-rfq/bin；下面是RFQ脚本文件

3. 根据所写的table_name进行创建.sh脚本

4. 文件规范：

   ```sh
   log_path="/var/log/monamii-rfq/"	---日志路径
   log_file_name="marine" 				---日志名
   ext=".log"							---后缀名
   DATE=$(date +%Y-%m-%d)				---日期
   log_file=${log_path}${log_file_name}.${DATE}${ext}	---拼接字符串
   cd /usr/local/monamii-rfq/bin/		---切换路径
   source ../python_venv/bin/activate	---打开虚拟环境
   
   #下面是创建的具体的机器人脚本:
   -----------------------------
   #电动汽车的充电器vv
   
   #ev charger
   #portable ev charger
   #ev wallbox
   #ev charging box
   #ev charging station
   
   scrapy runspider ../rfq.py -a keyword="ev charger" -a table_name=charger -a webhook_url="https://oapi.dingtalk.com/robot/send?access_token=9b1f3f8ee8b16cc4e5044f22d3aa35f77e910eda410cac698674131794d21d7e" --logfile ${log_file}
   ```

5. 根据关键字进行循环创建

#### 四、创建定时任务：

1. crontab -e	-----进入定时器中

   ```sh
   */3 * * * * /usr/local/monamii-rfq/bin/rfq_duct_machine.sh
   */3 * * * * /usr/local/monamii-rfq/bin/rfq_mouse_pad.sh
   */3 * * * * /usr/local/monamii-rfq/bin/rfq_press_brake.sh
   */3 * * * * /usr/local/monamii-rfq/bin/rfq_wheelchair.sh
   */3 * * * * /usr/local/monamii-rfq/bin/rfq_bike.sh
   
   #模板 */min * * * * /usr/local/monamii-rfq/bin/脚本名
   #wq----保存并退出
   ```

2. 最后重启定时器：systemctl restart crond

#### 五、上传代码段:

1. 进入分支
2. 提交本地
3. 远程上传

