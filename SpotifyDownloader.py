#!/usr/local/bin/python3
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import threading
import os
import eyed3

# Global variable to signal the thread to stop
stop_thread = False
file_path = os.path.expanduser("~/Downloads")

def remove_special_characters(input_string):
    return ''.join(char if char.isalnum() or char.isspace() or char in '()-,' else '_' for char in input_string)

def process_file(file_path, dest_file):
    try:
        audiofile = eyed3.load(file_path)
        artist = audiofile.tag.artist or ""
        title = audiofile.tag.title or ""
        
        track_name = f"{remove_special_characters(artist)} - {remove_special_characters(title)}"

        dest_file = os.path.join(os.path.dirname(file_path), f"{track_name}.mp3")
        os.rename(file_path, dest_file)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def download_task(url):
    global stop_thread

    # URL of the initial page
    initial_url = 'https://spotifydown.com/'

    # Input URL for testing
    input_url = url

    # Set up Firefox options for headless mode
    firefox_options = Options()
    firefox_options.add_argument('--headless')

    # Start the Firefox browser using Selenium
    driver = webdriver.Firefox(options=firefox_options)

    # Open the initial page
    driver.get(initial_url)

    # Find the search input element using its class name
    search_input = driver.find_element(By.CLASS_NAME, 'searchInput')

    # Input the URL into the search field
    search_input.send_keys(input_url)

    # Find the "Download" button and click on it using XPath
    download_button = driver.find_element(By.XPATH, '//button[text()="Download"]')
    download_button.click()

    time.sleep(2)

    # Wait for the dynamic changes after clicking the "Download" button
    download_buttons = driver.find_elements(By.XPATH, '//button[text()="Download"]')

    song_count = len(download_buttons)
    multiples = 0
    err_num = []

    while True:
        try:
            # Wait for the "Load More" button to be clickable
            wait = WebDriverWait(driver, 10)
            loadmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Load More"]')))
            loadmore_link.click()

            # Wait for dynamic changes after clicking the "Load More" button
            download_buttons = driver.find_elements(By.XPATH, '//button[text()="Download"]')

            # Increment the song_count variable by the number of "Download" buttons found
            song_count += len(download_buttons)
        except Exception as e:
            break

    for i in range(song_count):
        # Check the flag to see if the thread should stop
        if stop_thread:
            break

        # Open the initial page
        driver.get(initial_url)

        # Find the search input element using its class name
        search_input = driver.find_element(By.CLASS_NAME, 'searchInput')

        # Input the URL into the search field
        search_input.send_keys(input_url)

        # Find the "Download" button and click on it using XPath
        download_button = driver.find_element(By.XPATH, '//button[text()="Download"]')
        download_button.click()

        time.sleep(1)

        if i < 100:
            # Wait for the dynamic changes after clicking the "Download" button
            download_buttons = driver.find_elements(By.XPATH, '//button[text()="Download"]')
            download_buttons[i].click()
        else:
            if i % 100 == 0 and i != 0:
                multiples += 1
            
            for x in range(multiples):
                wait = WebDriverWait(driver, 10)
                loadmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Load More"]')))
                loadmore_link.click()

            time.sleep(1)

            download_buttons = driver.find_elements(By.XPATH, '//button[text()="Download"]')
            download_buttons[i - 100*multiples].click()

        # Wait for the dynamic changes after clicking the "Download" button
        try:
            wait = WebDriverWait(driver, 20)
            download_mp3_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'transition')))
            download_mp3_link.click()
        except Exception as e:
            err_num.append(i)

        # Add a delay if needed to allow time for the download to start
        time.sleep(1)

    # Close the browser window
    driver.quit()

    for root, dirs, files in os.walk(file_path):
        for file in files:
            path_file = os.path.join(root, file)
            process_file(path_file, file_path)

    # Re-enable the "Download" button after completion
    gui_download_button.config(state=tk.NORMAL)

def on_button_click():
    global stop_thread

    # Disable the "Download" button to prevent further clicks
    gui_download_button.config(state=tk.DISABLED)

    # Enable the "Download" button to prevent further clicks
    stop_button.config(state=tk.NORMAL)

    # Get the input value
    url = entry.get()

    # Clear the text in the Entry widget
    entry.delete(0, tk.END)

    # Reset the stop_thread flag
    stop_thread = False

    # Create a new thread for the download task
    download_thread = threading.Thread(target=download_task, args=(url,))
    download_thread.start()

def on_stop_click():
    global stop_thread

    # Disable the "Download" button to prevent further clicks
    stop_button.config(state=tk.DISABLED)

    # Set the stop_thread flag to True
    stop_thread = True

# Create the main window
root = tk.Tk()
root.title("SpotifyDownloader")

# Set the size of the window
root.geometry("400x200")

# Create and pack widgets
label = tk.Label(root, text="Enter playlist/song URL:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

# Download button
gui_download_button = tk.Button(root, text="Download", command=on_button_click)
gui_download_button.pack(padx=5, pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=on_stop_click)
stop_button.pack(padx=5, pady=10)

# Start the main event loop
root.mainloop()
