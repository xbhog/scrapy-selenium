# -*- coding: utf-8 -*-
import sys
sys.path.append('..')

import webhook
import logging
import company

class TztalentPipeline(object):
    def process_item(self, item, spider):
        # webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=27d525c0827d39eb79b10ce287e02ed4b2613ddb32ad18dce07f8855e10571d4'
        # webhook_url = item["webhook_url"]
        webhook_url = spider.webhook_url
        # mydb = db.MydbOperator(table_name)
        # mydb.create_table()
        # isInitialize = mydb.is_empty_table()
        # print(isInitialize)
        webhook_service = webhook.WebHook(webhook_url)

        job_title = item["title"]
        company_name = item["company_name"]
        company_url = item["company_url"]
        location = item['site']
        company_in_db = spider.mydb.get_by_company_name_and_job(company_name, job_title)
        if company_in_db is None:
            company_obj = company.company(job_title, company_name, company_url, location)
            spider.mydb.save_company(company_obj)
            if not spider.isInitialize:
                # 添加 webhook发送器，不为空发送
                if not spider.isInitialize:
                    formatted_context = webhook_service.format_with_template(company_obj)
                    print(formatted_context)
                    # 设置发送的数据格式----markdown
                    # self.webhook_service.send_markdown(company_name, formatted_context, True)
                    webhook_service.send_markdown(company_name, formatted_context, False)
        else:
            # 打印错误提示信息
            # Quit as reaching existing data records
            logging.info("没有新数据.")
