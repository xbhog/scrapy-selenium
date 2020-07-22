from scrapy import cmdline
#泰州人才网
cmdline.execute("scrapy crawl tzjobpro -a table_name=tzjobsql -a keyword=外贸业务员 -a webhook=https://oapi.dingtalk.com/robot/send?access_token=27d525c0827d39eb79b10ce287e02ed4b2613ddb32ad18dce07f8855e10571d4".split())

#https://www.0523rc.cn/泰州就业人才网
# cmdline.execute("scrapy crawl tztapro -a table_name=tztasql -a keyword=外贸业务员 -a webhook=https://oapi.dingtalk.com/robot/send?access_token=27d525c0827d39eb79b10ce287e02ed4b2613ddb32ad18dce07f8855e10571d4".split())

##泰州就业人才网
# cmdline.execute("scrapy crawl tzcode -a table_name=taizhou -a keyword=外贸业务员 -a webhook=https://oapi.dingtalk.com/robot/send?access_token=27d525c0827d39eb79b10ce287e02ed4b2613ddb32ad18dce07f8855e10571d4".split())

#拉钩招聘
# cmdline.execute("scrapy crawl lagoupro -a table_name=lagousql -a keyword=外贸业务员 -a site=南京 -a webhook=https://oapi.dingtalk.com/robot/send?access_token=27d525c0827d39eb79b10ce287e02ed4b2613ddb32ad18dce07f8855e10571d4".split())

#58job
# cmdline.execute("scrapy crawl 58jobpro -a table_name=58job -a keyword=外贸业务员 -a site=常州 -a webhook=https://oapi.dingtalk.com/robot/send?access_token=27d525c0827d39eb79b10ce287e02ed4b2613ddb32ad18dce07f8855e10571d4".split())
