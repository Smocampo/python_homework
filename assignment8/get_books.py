import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. ADD THESE NEW IMPORTS FOR THE WAIT (From our last step)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup Driver ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# --- Task 2 / Step 2: Load the Web Page ---
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)


print("Waiting for page content to load safely...")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, ".//span[contains(@class, 'cp-title')]"))
)


# Task 3 
book_elements = driver.find_elements(By.CLASS_NAME, "YOUR_LI_CLASS_NAME") 

results = []

for index, book in enumerate(book_elements):
  try:
    results.append({
      "Title": title,
      "Author": author,
      "Format-Year": format_year
        })
  except Exception as e:
    print(f"Error parsing book index {index}: {e}")

# --- Close Driver ---
driver.quit()

df = pd.DataFrame(results)
print(df)

# Task 4
df.to_csv("get_books.csv", index=False)