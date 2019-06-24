# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time


class GuaziSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GuaziDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.timeout = timeout
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument("--proxy-server=%s" % request.meta["proxy"])

        self.browser = webdriver.Chrome(chrome_options=chromeOptions)
        self.browser.set_window_size(1400, 700)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def sleep(self):
        time.sleep(random.randint(0,3))

    def process_request(self, request, spider):
        """
        抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        # page = request.meta.get('page', 1)


        try:
            # print(request.meta["proxy"])


            self.browser.get(request.url)
            for i in range(0,9):
                self.browser.execute_script('window.scrollTo(0, {} * document.body.scrollHeight / 8)'.format(i))
                self.sleep()

            # self.sleep()
            # self.browser.execute_script('window.scrollTo(0, 2 * document.body.scrollHeight / 8)')
            # self.sleep()
            #
            # self.browser.execute_script('window.scrollTo(0, 3 * document.body.scrollHeight / 8)')
            # self.sleep()
            #
            # self.browser.execute_script('window.scrollTo(0, 4 * document.body.scrollHeight / 8)')
            # self.sleep()
            #
            # self.browser.execute_script('window.scrollTo(0, 5 * document.body.scrollHeight / 8)')
            # self.sleep()
            #
            # self.browser.execute_script('window.scrollTo(0, 6 * document.body.scrollHeight / 8)')
            # self.sleep()
            #
            # self.browser.execute_script('window.scrollTo(0, 7 * document.body.scrollHeight / 8)')
            # self.sleep()
            # self.browser.execute_script('window.scrollTo(0, 8 * document.body.scrollHeight / 8)')

            # if page > 1:
            #     input = self.wait.until(
            #         EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage .input-txt')))
            #     submit = self.wait.until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage a.btn-default')))
            #     input.clear()
            #     input.send_keys(page)
            #     submit.click()
            # self.wait.until(
            #     EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_topPage b'), str(page)))

            # self.wait.until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage .input-txt')))
            # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
