import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup and teardown methods
@pytest.fixture(scope="module")
def driver():
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://localhost:5173")  # Adjust the path to your local HTML file
    driver.maximize_window()
    yield driver
    # Teardown WebDriver
    driver.quit()

# Test that the calculator buttons work correctly
def test_calculator_operations(driver):
    # Clear the display
    driver.find_element(By.CSS_SELECTOR, '[data-all-clear]').click()
    
    # Test number input
    driver.find_element(By.CSS_SELECTOR, '[data-number="1"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="2"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="3"]').click()
    
    # Verify the current operand is "123"
    current_operand = driver.find_element(By.CSS_SELECTOR, '[data-current-operand]').text
    assert current_operand == "123", f"Expected '123', but got {current_operand}"
    
    # Test operations
    driver.find_element(By.CSS_SELECTOR, '[data-operation="+"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="4"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-equals]').click()
    
    # Verify the result of the operation
    current_operand = driver.find_element(By.CSS_SELECTOR, '[data-current-operand]').text
    assert current_operand == "127", f"Expected '127', but got {current_operand}"

    # Test delete functionality
    driver.find_element(By.CSS_SELECTOR, '[data-delete="DEL"]').click()
    current_operand = driver.find_element(By.CSS_SELECTOR, '[data-current-operand]').text
    assert current_operand == "12", f"Expected '12', but got {current_operand}"

    # Test clear functionality
    driver.find_element(By.CSS_SELECTOR, '[data-all-clear]').click()
    current_operand = driver.find_element(By.CSS_SELECTOR, '[data-current-operand]').text
    assert current_operand == "", f"Expected '', but got {current_operand}"

# Test invalid operation (e.g., divide by zero)
def test_divide_by_zero(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-all-clear]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="1"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-operation="÷"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="0"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-equals]').click()
    
    # Verify that the result is 'Infinity' or similar error message
    current_operand = driver.find_element(By.CSS_SELECTOR, '[data-current-operand]').text
    assert current_operand == "∞", f"Expected '∞', but got {current_operand}"

# Test decimal point functionality
def test_decimal_point(driver):
    driver.find_element(By.CSS_SELECTOR, '[data-all-clear]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="1"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="."]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-number="5"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-equals]').click()
    
    # Verify that the result is "1.5"
    current_operand = driver.find_element(By.CSS_SELECTOR, '[data-current-operand]').text
    assert current_operand == "1.5", f"Expected '1.5', but got {current_operand}"