from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Navigate to the dashboard and take a screenshot
    page.goto('http://127.0.0.1:5000/')
    page.screenshot(path='verification_dashboard.png')

    # Navigate to the transactions page and take a screenshot
    page.goto('http://127.0.0.1:5000/transactions')
    page.screenshot(path='verification_transactions.png')

    # Navigate to the budgets page and take a screenshot
    page.goto('http://127.0.0.1:5000/budgets')
    page.screenshot(path='verification_budgets.png')

    # Navigate to the reports page and take a screenshot
    page.goto('http://127.0.0.1:5000/reports')
    page.screenshot(path='verification_reports.png')

    # Navigate to the settings page and take a screenshot
    page.goto('http://127.0.0.1:5000/settings')
    page.screenshot(path='verification_settings.png')

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
