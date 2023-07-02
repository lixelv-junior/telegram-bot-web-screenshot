from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os


def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)



def find_max_numbered_file(directory_path):
    only_numbers = []
    directory_path = os.path.join(os.getcwd(),directory_path)

    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            name_without_extension = os.path.splitext(filename)[0]
            if name_without_extension.isdigit():
                only_numbers.append(int(name_without_extension))

    if not only_numbers:
        return 1
    else:
        return max(only_numbers)+1


def capture_full_page_screenshot(driver, url, path='image', width=1920):
    url = url if url[:4] in ['file', 'http'] else 'http://'+url
    start_time = time.perf_counter()
    driver.get(url)
    title = driver.title
    scroll_height = driver.execute_script('return document.documentElement.scrollHeight')
    driver.set_window_size(width, scroll_height)
    save_to = f'{path}/{find_max_numbered_file(path)}.png'
    screenshot = driver.save_screenshot(save_to)
    end_time = time.perf_counter()
    time_ = end_time - start_time
    return save_to, url, title, time_