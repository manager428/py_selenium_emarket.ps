from selenium import webdriver  
import time  
from selenium.webdriver.common.keys import Keys
import urllib.request
from random import randint
import random
import tkinter as tk
from tkinter import simpledialog
import mysql.connector
import datetime
import requests;
import math
import sys

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
def main():
    
    sku_value = simpledialog.askstring(title="SKU",
                                    prompt="Please enter your SKU value:")
                             
    if sku_value != None:

        driver = webdriver.Chrome()  
        #navigate to the url
        driver.get("https://ru.shein.com")
        # firstmodal = driver.find_element_by_class_name("c-ip-pop-up")
        # firstmodal.find_element_by_css_selector("i.iconfont.icon-close").click()
        driver.find_element_by_css_selector("i.svgicon.svgicon-close").click()
        

        driver.find_element_by_class_name("j-header-search-input").send_keys(sku_value)

        time.sleep(3)
        driver.find_element_by_class_name("j-search-btn").click()
        time.sleep(3)
        
        try:
            sku_values = driver.find_element_by_css_selector("section.j-expose__product-item.product-list__item")
            sku_name = sku_values.find_element_by_css_selector("a.S-product-item__link.S-product-item__link_jump").text
            sku_price = sku_values.find_element_by_css_selector("span.S-product-item__retail-price").text
            main_page = driver.find_element_by_css_selector("section.j-expose__product-item.product-list__item")
            time.sleep(2)
            main_page.find_element_by_css_selector("div.S-product-item__wrapper").click()
            sku_product_image_div_name = driver.find_elements_by_css_selector("div.swiper-slide.product-intro__main-item")
            sku_size_array = driver.find_element_by_class_name("product-intro__size-choose")
            
            time.sleep(1)
            sku_product_image = ''
            button_next_click = driver.find_element_by_css_selector("div.common-swiperv2__next")
            button_mext_icon = button_next_click.find_element_by_css_selector("i.svgicon.svgicon-arrownew-left")
            print('------->', sku_name)
            print('------->', sku_price.replace(" ", ""))
            sku_really_prices = sku_price.replace(" ", "")
            sku_really_price = sku_really_prices.replace("₪","")
            sku_id = insert_mysql_data(sku_name, sku_really_price, sku_value)
            
            print('------------>id', sku_id)
            
            # product_names = driver.find_elements_by_css_selector("span.bread-crumb__item-link")
            # product_name = product_names[2].text
            product_name = "Size"
            print('product_name---------->', product_name)
            
            insert_sku_size_option_function(sku_id, product_name)
            sku_position = -1
            for sku_size_names in sku_size_array.find_elements_by_css_selector("span.inner"):
                sku_size_name = sku_size_names.text
                print(sku_size_name)
                sku_position = sku_position+1
                insert_sku_size_function(sku_id, sku_position, sku_size_name )
                print('skupositoin---->', sku_position)
            x = 0
            y = ''
            for i in sku_product_image_div_name:
                
                button_mext_icon.click()
                time.sleep(1)
                sku_product_image = i.find_element_by_tag_name("img").get_attribute("src")
                print("sku_product_image---------->", sku_product_image)
                x = x+1
                y = str(x)
                
                urllib.request.urlretrieve(sku_product_image, sku_value + y + ".jpg")
                print('-----------downloading------->sku_image', sku_product_image, sku_value + y)
            
    
            if sku_id != -1:
                for j in range(len(sku_product_image_div_name)):
                    upload_oneimage(sku_id, sku_value + str(j+1))
        except Exception as e:
            sku_value_none(sku_value)
        # driver.close()

def insert_mysql_data(sku_name, sku_really_price, sku_value):
    sku_id = -1
    
    try:
        connection = mysql.connector.connect(
            host="host ip",
            user="host user",
            password="database password",
            database="database"
        )
        currenttime = datetime.datetime.now()
        mySql_insert_query = "INSERT INTO products (brand_id, slug, special_price, special_price_type, selling_price, sku, in_stock, is_active, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(1, sku_name, sku_really_price, 'fixed', sku_really_price, sku_value, 1, 1, currenttime, currenttime)
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.execute("SELECT * FROM products WHERE slug = %s", (sku_name,))
        myresult = cursor.fetchall()
        sku_id = myresult[0][0]
        mySql_insert_query = "INSERT INTO product_translations (product_id, locale, `name`, `description`) VALUES ('{}', '{}', '{}', '{}')".format(sku_id, 'en', sku_name, sku_name)
        cursor.execute(mySql_insert_query)
        connection.commit()        
        print(cursor.rowcount, "OKKKKKKKKKKKKKKKK")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))
    return sku_id

def upload_oneimage(sku_id, filename) :
    url = 'https://dwaik.xyz/single-upload.php'
    item = {"skuid": sku_id}
    file = {'myfile': open(filename + '.jpg','rb')}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.post(url, headers=headers, data=item, files=file)
    # r = requests.post(url, data=item, files=file)
    
    if r.status_code != 200:
        print(r)
        print(r.text)
        print(r.raw)
    else :
        print(r.text)

def insert_sku_size_function(sku_id, sku_position, sku_size_name):
    currenttime = datetime.datetime.now()
    connection = mysql.connector.connect(
        host="host ip",
        user="host user",
        password="database password",
        database="database"
    )
    cursor = connection.cursor()
    mySql_insert_query = "INSERT INTO option_values (`option_id`, `price_type`, `position`, `created_at`, `updated_at`) VALUES ('{}', '{}', '{}', '{}', '{}')".format(sku_id, 'fixed', sku_position, currenttime, currenttime)
   
    cursor.execute(mySql_insert_query)
    connection.commit()
    cursor.execute("SELECT * FROM option_values WHERE option_id = %s AND position = %s", (sku_id, sku_position))
    myresult = cursor.fetchall()
    myresult_id = myresult[0][0]
    print('myresult_id---------------->', myresult_id)
    mySql_insert_query = "INSERT INTO option_value_translations (`option_value_id`, `locale`, `label`) VALUES ('{}', '{}', '{}')".format(myresult_id, 'en', sku_size_name)
    cursor = connection.cursor()
    cursor.execute(mySql_insert_query)
    connection.commit()
    
    print("SKU_________SIZE_________NAME")

def insert_sku_size_option_function(sku_id, product_name):
    currenttime = datetime.datetime.now()
    connection = mysql.connector.connect(
        host="host ip",
        user="host user",
        password="database password",
        database="database"
    )
    cursor = connection.cursor()
    mySql_insert_query = "INSERT INTO options (`id`, `type`, `is_required`, `is_global`, `position`, `created_at`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(sku_id, 'radio_custom', 0, 0, 0, currenttime)
    cursor.execute(mySql_insert_query)
    connection.commit()

    mySql_insert_query = "INSERT INTO product_options (`product_id`, `option_id`) VALUES ('{}', '{}')".format(sku_id, sku_id)
    cursor.execute(mySql_insert_query)
    connection.commit()

    mySql_insert_query = "INSERT INTO option_translations (`option_id`, `locale`, `name`) VALUES ('{}', '{}', '{}')".format(sku_id, 'en', product_name)
    cursor.execute(mySql_insert_query)
    connection.commit()

   

    print('_________________________________>okay')

def sku_value_none(sku_value):
    try:
        connection = mysql.connector.connect(
            host="host ip",
            user="host user",
            password="database password",
            database="database"
        )
        cursor = connection.cursor()
        print("------------------->", sku_value)
        currenttime = datetime.datetime.now()
        cursor.execute("SELECT * FROM products WHERE sku = '{}'".format(sku_value, ))
        print("----------------------->SELECTSELECT", "SELECT * FROM products WHERE sku = '{}'".format(sku_value, ))
        myresult = cursor.fetchall()
        data_id = myresult[0][0]
        print("cursor.executets ", data_id)
        
        if  data_id != None:
            mySql_insert_query = "UPDATE products SET in_stock = '{}', updated_at = '{}' WHERE sku = '{}'".format(0, currenttime, sku_value)
            
            cursor.execute(mySql_insert_query)
            connection.commit()
            print(cursor.rowcount, "Updated Success")
        
            connection.commit()
        else:
            print("Sorry, SKU value doesn't in Site. Please try again ...")
            
    except Exception as e:
        print("Sorry, Scrapping error. Please try again ...", e)

if __name__ == "__main__":
    main()
