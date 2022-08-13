import urllib
import urllib.request
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
import time
import re


def get_src1(img, link_set):
    img_str = str(img)
    #print(img_str+"///////////////////")
    if re.findall('src="https://preview.redd.it/', img_str):
        #print("Found")
        x = re.split("\s", img_str)
        #print(x)
        for item in x:
            if re.search('^src="https://preview.redd.it/', item):
                img_src = item.replace('src"', '')
                img_src_nosrc = img_src[5:]
                print(str(img_src))
                if re.search("^https://preview.redd.it/", str(img_src_nosrc)):
                    link_set.add(img_src_nosrc)
                    print(img_src_nosrc)


def get_src2(img, link_set):
    if re.search('^https://preview.redd.it/', img['src']):
        link_set.add(img['src'])


def get_src_video(video, link_set):
    if re.search('^https://', video['src']):
        link_set.add(video['src'])


def select_operation_mode():
    print("Choose An Operation Mode\n 1- User Controlled Saving\n 2- Time Controlled Saving\n "
          "3- Exit\n ---------------")
    while True:
        answer = input("Choose: ")
        if answer == "3":
            print("See you soon...")
            time.sleep(2)
            exit()
        elif answer == "1":
            answer = "User Controlled"
            return answer
        elif answer == "2":
            answer = "Time Controlled"
            return answer
        else:
            pass


def select_saving_context():
    print("\n------------\nChoose File Type To Save\n 1- Only Images\n 2- Only Videos\n 3- Images and Videos"
          "\n 4- Exit\n-------------")
    while True:
        answer = input("Choose: ")
        if answer == "4":
            try:
                driver.close()
            except BaseException:
                pass
            print("See you soon...")
            time.sleep(2)
            exit()
        elif answer == "1":
            answer = "Only Images"
            return answer
        elif answer == "2":
            answer = "Only Videos"
            return answer

        elif answer == "3":
            answer = "Images and Videos"
            return answer
        else:
            pass


def open_in_current_mode(given_operation_mode):
    if given_operation_mode == "User Controlled":
        #Run User Controlled Function
        pass

    if given_operation_mode == "Time Controlled":
        pass


def download_image(url, file_path, file_name, failed_file):
    try:
        full_path = str(file_path)+ "/" + str(file_name)
        urllib.request.urlretrieve(url, full_path)
    except():
        failed_file = failed_file + 1


# address = input("Enter image URL: ")
operation_mode = select_operation_mode()
while operation_mode == "Time Controlled":
    print("\nThis operation mode will be added soon.\nFor now you can only use User Controlled Mode\n")
    operation_mode = select_operation_mode()



#----------------------------------------------Getting A Reddit URL---------------------------------------------
while True:
    address = input("Enter Your Operation URL: ")
    if address == "exit":
        print("See you soon...")
        time.sleep(2)
        exit()
    try:
        if not address.startswith("https://www.reddit.com/r/"):
            print("\nCorrect URL must be in this format:\n'https://www.reddit.com/r/topicname/'")
        else:
            response = requests.get(address)
            if response.ok:
                try:
                    file_name = address.replace("https://www.reddit.com/r/", "").replace("/", "")
                    break
                except():
                    print("Wrong Url Type - Correct Example 'https://www.reddit.com/r/topicname/'")

    except BaseException:
        print("Wrong URL Given\n")
#-----------------------------------------------End Of Getting A Reddit URL-------------------------------------


#-----------------------------------------------Web Driver Setup------------------------------------------------
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge('msedgedriver', options=options)
driver.get(address)
#----------------------------------------------End Of Web Driver Setup-------------------------------------------


if operation_mode == "User Controlled":
    while True:
        saving_context = select_saving_context()
        if not saving_context == None:
            print(f"{saving_context} Selected")
        try:
            if saving_context == "Only Images":
                myLink_set_uc = set()
                soup1 = BeautifulSoup(driver.page_source, 'lxml')
                img_a_list = soup1.find_all('img', {'src': True})
                time.sleep(1)
                for img in img_a_list:
                    try:
                        img_src = str(get_src1(img, link_set=myLink_set_uc))  # Elle Yazdığım Fonksiyon
                        # get_src2(img, link_set=myLink_set_uc) #bs4 Kütüphanesi Fonksiyonu

                    except():
                        print("Failed")
                with open(f'{file_name} image.txt', 'w', encoding='utf-8') as links:
                    splitted_urls = (myUrl1.split("?") for myUrl1 in myLink_set_uc)
                    splitted_urls_depreview = (myUrl2[0].replace('preview', "i") for myUrl2 in splitted_urls)
                    remained_file_count = len(myLink_set_uc)
                    print(remained_file_count)
                    #print("Started to write /////////////////////////////////////\n")
                    for item in splitted_urls_depreview:
                        links.write(item + "\n")
                    links.write("///////////////////////////\n")
                    links.close()
                with open('foundimg.txt', 'w', encoding='utf-8') as fndimg:
                    fndimg.write(str(img_a_list))
                fndimg.close()

                #Creating Save Location
                file_count = 0
                print("Creating File")
                download_location = f"Operations/{file_name}"
                while os.path.exists(download_location):
                    file_count = file_count + 1
                    download_location = f"Operations/{file_name} ({file_count})"

                if file_count == 0:
                    os.makedirs(f"Operations/{file_name}")
                    download_location = f"Operations/{file_name}"
                else:
                    os.makedirs(f"Operations/{file_name} ({file_count})")
                    download_location = f"Operations/{file_name} ({file_count})"
                #End of creation of the save location
                input("To start downloading press enter")
                #Getting All Saved Links
                with open(f'{file_name} image.txt', 'r') as saved_urls:
                    saved_urls_list = saved_urls.readlines()
                saved_urls.close()


                #Downloading to download location
                failed_file = 0
                print("Remained File(s):")
                for link_item in saved_urls_list:
                    if link_item == "///////////////////////////\n":
                        break
                    saved_file_name = str(link_item).replace("https://i.redd.it/", "").replace("\n", "")
                    if not "/" in saved_file_name:
                        download_image(link_item, download_location, saved_file_name, failed_file)
                        remained_file_count = remained_file_count - 1
                        if remained_file_count == 1:
                            remained_file_count="\nDownload Complete"
                        print("\r ", end=str(remained_file_count))
                if not failed_file == 0:
                    print(f"{failed_file}'s failed to download.")

            elif saving_context == "Only Videos":
                print("\nOnly Videos mode will be added soon.\nFor now you can only use Only Images mode")
                saving_context = select_saving_context()

            elif saving_context == "Images and Videos":
                print("\nImages and Videos mode will be added soon.\nFor now you can only use Only Images mode")
                saving_context = select_saving_context()

        except BaseException as error:
            print('An exception occurred: {}'.format(error))
            print("May be you closed the browser on progress")
            print("See you soon, you can restart the app...")
            try:
                driver.close()
            except BaseException:
                pass
            time.sleep(2)
            exit()



