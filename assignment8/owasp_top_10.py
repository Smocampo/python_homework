import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup Driver ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# --- Load the OWASP Page ---
url = "https://owasp.org/www-project-top-ten/"
driver.get(url)

try:
  #Step 3
  WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
  vulnerability_elements = driver.find_elements(By.XPATH, "//YOUR_XPATH_HERE")
    
    # This list will accumulate our dictionaries
  vulnerabilities_list = []
    
  for element in vulnerability_elements:
    # Extract the visible title text
    title = element.text
        
        # Extract the URL link attribute
    link = element.get_attribute("href")
        
        # Only append if we actually captured a title to avoid empty header/footer links
  if title:
    vulnerabilities_list.append({
      "Vulnerability Title": title,
      "Link": link
            })

    #Step 4
    print("\n--- Scraped Data Verification ---")
    print(vulnerabilities_list)
    
    # Convert list of dicts to a pandas DataFrame
    df = pd.DataFrame(vulnerabilities_list)
    
    # Save to your assignment8 folder
    df.to_csv("owasp_top_10.csv", index=False)
    print("\nSuccessfully saved to owasp_top_10.csv!")

except Exception as e:
  print(f"An error occurred: {e}")

finally:
    # --- Close Driver ---
  driver.quit()