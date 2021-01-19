from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from selenium import webdriver

from .serializers import SaleSerializer
from .models import Sale

import time, bs4 as bs, random

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


def order_bot(request):
    PROXY_LIST = [
        "203.198.94.132:80", "163.172.125.147:8080", "163.172.47.182:3128", "58.152.94.83:8080", "41.73.15.130:8080",
        "188.113.190.7:80", "119.28.155.202:9999", "136.243.254.196:80", "192.109.165.139:80", "49.156.35.22:8080",
    ]
    PROXY = random.choice(PROXY_LIST)

    driver_path = BASE_DIR / 'chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXY)
    # options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    try:
        user_email = 'stephendonald@icloud.com'
        user_password = 'Fivertest123@'
        driver.get('https://accounts.stockx.com/login')
        time.sleep(2)

        driver.find_element_by_id('email-login').send_keys(user_email)
        driver.find_element_by_id('password-login').send_keys(user_password)
        driver.find_element_by_id('btn-login').click()
        time.sleep(10)
        driver.find_element_by_class_name('et9rxoe2').click()

        products = Sale.objects.all()
        for product in products:
            purchase = product.minimum
            url = product.url
            edit_url = product.edit_url
            print(url)
            print(edit_url)

            driver.get(url)
            time.sleep(5)
            site_lower_ask= int(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/a/div[1]/div').text.replace('$',''))
            if site_lower_ask > purchase:
                driver.get(edit_url)
                time.sleep(5)
                driver.find_element_by_xpath('/html/body/div[2]/div/div/button[2]').click()
                print('I understand')
                time.sleep(10)
                amount = driver.find_element_by_class_name('amount')
                my_old_ask =int(amount.get_attribute('value'))
                print('get ask from product')

                if my_old_ask > site_lower_ask:
                    amount.clear()
                    my_new_lower_ask = site_lower_ask - 1
                    amount.send_keys(my_new_lower_ask)
                    print('set ask of product')
                    time.sleep(10)

                    driver.find_element_by_xpath('/html/body/div[2]/div/div/button[2]').click()
                    print('click ask update')
                    time.sleep(10)
                    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[7]/div[1]/label').click()
                    print('click ask checkbox t c')
                    time.sleep(5)
                    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[7]/div[2]/label').click()
                    print('click ask checkbox t c')
                    time.sleep(5)
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/button[2]').click()
                    print('click confirm')
                    time.sleep(5)
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/button').click()
                    print('click finish')
                    time.sleep(5)
                else:
                    print('my old ask is equal or less')
            else:
                print('sorry')
        driver.close()

    except:
        print('error in excution')
        driver.close()

    return JsonResponse({'succes':True})