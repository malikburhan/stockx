from django.shortcuts import render, redirect
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from selenium import webdriver

from .serializers import SaleSerializer
from .models import Sale

import os, time, bs4 as bs, random

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.
def order_sale_list(request):
    template_name = 'order/sale_list.html'
    context = {
        'title': "Order",
    }
    return render(request, template_name, context)



@api_view(['GET'])
def api_order_sale_list(request):
    sales = Sale.objects.all().order_by('-id')
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def api_order_sale_save(request):
    serializer = SaleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def api_order_sale_obj(request, id):
    sales = Sale.objects.filter(id=id)
    serializer = SaleSerializer(sales, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_order_sale_edit(request, id):
    sale = Sale.objects.get(id=id)
    serializer = SaleSerializer(instance=sale, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def api_order_sale_delete(request, id):
    Sale.objects.filter(id=id).delete()
    serializer = SaleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def order_bot(request):


    # TRACKER_LIST = [
    #     ['https://stockx.com/timberland-6-jimmy-choo-premium-wheat-swarovski-crystal-w?size=9.5W', 'https://stockx.com/sell/13500227271409340534', 1000],
    #     ['https://stockx.com/adidas-nmd-r1-gaming-pack?size=10', 'https://stockx.com/sell/13516612311365808776', 60],
    #     ['https://stockx.com/timberland-6-bbc-bee-line-wheat-green?size=9.5','https://stockx.com/sell/13500237691380618573', 210]
    # ]


    USER_AGENT_LIST= [
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/58.0',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.59.12) Gecko/20160044 Firefox/52.59.12',
        'Mozilla/5.0 (X11;  Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20120121 Firefox/46.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0'
    ]

    PROXY_LIST = [
        "203.198.94.132:80", "163.172.125.147:8080", "163.172.47.182:3128", "58.152.94.83:8080", "41.73.15.130:8080",
        "188.113.190.7:80", "119.28.155.202:9999", "136.243.254.196:80", "192.109.165.139:80", "49.156.35.22:8080",
    ]
    PROXY = random.choice(PROXY_LIST)
    USER_AGENT = random.choice(USER_AGENT_LIST)

    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument('user-agent=%s' % USER_AGENT)
    options.add_argument('--headless')
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver_path ='/usr/lib/chromium-browser/chromedriver'
    # driver_path = 'C:/driver/geckodriver.exe'
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.get('https://accounts.stockx.com/login')
    print('open url')

    user_email = 'stephendonald@icloud.com'
    user_password = 'Fivertest123@'
    try:
        time.sleep(5)
        print('putting auth')
        email_login = driver.find_element_by_id("email-login")
        email_login.clear()
        email_login.send_keys(user_email)

        password_login = driver.find_element_by_id('password-login')
        password_login.clear()
        password_login.send_keys(user_password)


        time.sleep(2)

        btn_login = driver.find_element_by_id('btn-login')
        btn_login.click()

        time.sleep(10)
        print('closing lang')
        lang_popup = driver.find_element_by_class_name('et9rxoe2')
        lang_popup.click()

        loop = 'always'

        while loop == 'always':
            print('start loop')

            TRACKER_LIST = Sale.objects.all()
            for product in TRACKER_LIST:
                try:
                    print('doing job')
                    purchase = int(product.purchase)
                    url = product.url
                    edit_url = product.edit_url
                    time.sleep(10)

                    driver.get(url)
                    time.sleep(5)
                    view_all_ask = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div/a')
                    view_all_ask.click()
                    time.sleep(5)
                    print('getting price')
                    f_rows_all_ask = driver.find_element_by_id('400')
                    f_row_amount = int(str(f_rows_all_ask.find_elements_by_css_selector('tr')[1].text).split(' ')[1][1:].replace(' ','').replace(',','')) or 0

                    driver.get(edit_url)
                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[2]/div/div/button[2]').click()
                    print('I understand')

                    time.sleep(5)
                    amount = driver.find_element_by_class_name('amount')
                    my_old_ask = int(str(amount.get_attribute('value')).replace(',',''))

                    est_my_ask =my_old_ask

                    if f_row_amount < my_old_ask and f_row_amount > purchase:
                        est_my_ask = f_row_amount - 1


                    amount.clear()
                    amount.send_keys(str(est_my_ask))

                    print(f'site mini {f_row_amount} mymini ask {my_old_ask} new {est_my_ask} my purc {purchase}')
                    time.sleep(5)

                    driver.find_element_by_xpath('/html/body/div[2]/div/div/button[2]').click()
                    print('click ask update')

                    time.sleep(10)
                    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[7]/div[1]/label').click()
                    print('click ask checkbox t c')

                    time.sleep(5)
                    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[7]/div[2]/label').click()
                    print('click ask checkbox t c')

                    time.sleep(1)
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/button[2]').click()
                    print('click confirm')

                    time.sleep(2)
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/button').click()
                    print('click finish')
                    time.sleep(15)


                except:
                    print('faild')

    except:
        # print('error')
        driver.close()
    return JsonResponse({'success':True})