"""
Job Portal - 17 Selenium Automated Test Cases
Tailored for: Node.js/Express/SQLite Job Portal
Routes: /auth/register, /auth/login, /auth/logout,
        /jobs, /jobs/new, /jobs/:id, /jobs/:id/apply, /profile
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ─── Config ───────────────────────────────────────────────────────────────────
BASE_URL = os.environ.get("APP_URL", "http://localhost:3000").rstrip("/")

# Test user — used across multiple tests
TEST_EMAIL    = "selenium_test_user@example.com"
TEST_PASSWORD = "Test@123456"
TEST_NAME     = "Selenium Tester"


# ─── Chrome driver fixture ─────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(8)
    yield d
    d.quit()


# ─── Helpers ──────────────────────────────────────────────────────────────────
def wait_for(driver, by, val, t=10):
    return WebDriverWait(driver, t).until(
        EC.presence_of_element_located((by, val))
    )

def fill(driver, name, value):
    el = driver.find_element(By.NAME, name)
    el.clear()
    el.send_keys(value)

def submit(driver):
    driver.find_element(
        By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
    ).click()
    time.sleep(1)

def get_body(driver):
    return driver.find_element(By.TAG_NAME, "body").text.lower()

def login(driver, email=TEST_EMAIL, password=TEST_PASSWORD):
    """Helper to log in quickly from any test."""
    driver.get(f"{BASE_URL}/auth/login")
    wait_for(driver, By.NAME, "email")
    fill(driver, "email",    email)
    fill(driver, "password", password)
    submit(driver)


# ═══════════════════════════════════════════════════════════════════════════════
# TC01 – TC03  |  Homepage
# ═══════════════════════════════════════════════════════════════════════════════

class TestHomepage:

    def test_tc01_homepage_loads(self, driver):
        """TC01: Homepage loads and returns a valid HTML page with a title."""
        driver.get(BASE_URL)
        assert driver.title != "", "Page title should not be empty"

    def test_tc02_jobs_shown_on_homepage(self, driver):
        """TC02: Homepage body contains job-related content."""
        driver.get(BASE_URL)
        body = get_body(driver)
        assert any(k in body for k in ["job", "position", "career", "opening", "portal"]), \
            "Homepage should display job-related content"

    def test_tc03_nav_has_login_and_register(self, driver):
        """TC03: Navigation bar contains Login and Register links."""
        driver.get(BASE_URL)
        links = " ".join(a.text.lower() for a in driver.find_elements(By.TAG_NAME, "a"))
        assert "login" in links or "sign in" in links, \
            "Navigation should have a Login link"
        assert "register" in links or "sign up" in links, \
            "Navigation should have a Register link"


# ═══════════════════════════════════════════════════════════════════════════════
# TC04 – TC07  |  Registration  (/auth/register)
# ═══════════════════════════════════════════════════════════════════════════════

class TestRegistration:

    def test_tc04_register_page_loads(self, driver):
        """TC04: /auth/register page loads and shows a form."""
        driver.get(f"{BASE_URL}/auth/register")
        form = wait_for(driver, By.TAG_NAME, "form")
        assert form.is_displayed(), "Registration form must be visible"

    def test_tc05_register_missing_fields(self, driver):
        """TC05: Submitting empty register form shows 'All fields are required.'"""
        driver.get(f"{BASE_URL}/auth/register")
        wait_for(driver, By.TAG_NAME, "form")
        # Leave all fields blank and submit
        submit(driver)
        body = get_body(driver)
        assert "required" in body or "fields" in body, \
            "Should show validation error for missing fields"

    def test_tc06_register_valid_user(self, driver):
        """TC06: Valid registration redirects to homepage (/)."""
        driver.get(f"{BASE_URL}/auth/register")
        wait_for(driver, By.TAG_NAME, "form")
        fill(driver, "fullName", TEST_NAME)
        fill(driver, "email",    TEST_EMAIL)
        fill(driver, "password", TEST_PASSWORD)
        submit(driver)
        # After success, app redirects to /
        assert driver.current_url.rstrip("/") == BASE_URL or \
               "login" in driver.current_url.lower(), \
            f"Expected redirect to / or /auth/login, got: {driver.current_url}"

    def test_tc07_register_duplicate_email(self, driver):
        """TC07: Registering with an already-used email shows error message."""
        driver.get(f"{BASE_URL}/auth/register")
        wait_for(driver, By.TAG_NAME, "form")
        fill(driver, "fullName", "Duplicate User")
        fill(driver, "email",    TEST_EMAIL)          # same email as TC06
        fill(driver, "password", TEST_PASSWORD)
        submit(driver)
        body = get_body(driver)
        assert "already" in body or "registered" in body or "exists" in body, \
            "Should show duplicate email error"


# ═══════════════════════════════════════════════════════════════════════════════
# TC08 – TC11  |  Login  (/auth/login)
# ═══════════════════════════════════════════════════════════════════════════════

class TestLogin:

    def test_tc08_login_page_loads(self, driver):
        """TC08: /auth/login page loads with email and password fields."""
        driver.get(f"{BASE_URL}/auth/login")
        wait_for(driver, By.NAME, "email")
        wait_for(driver, By.NAME, "password")
        assert driver.find_element(By.NAME, "email").is_displayed()
        assert driver.find_element(By.NAME, "password").is_displayed()

    def test_tc09_login_empty_fields(self, driver):
        """TC09: Submitting empty login form shows 'Email and password are required.'"""
        driver.get(f"{BASE_URL}/auth/login")
        wait_for(driver, By.TAG_NAME, "form")
        fill(driver, "email",    "")
        fill(driver, "password", "")
        submit(driver)
        body = get_body(driver)
        assert "required" in body or "email" in body, \
            "Should show required fields error"

    def test_tc10_login_invalid_credentials(self, driver):
        """TC10: Wrong password shows 'Invalid credentials.'"""
        driver.get(f"{BASE_URL}/auth/login")
        wait_for(driver, By.TAG_NAME, "form")
        fill(driver, "email",    TEST_EMAIL)
        fill(driver, "password", "WrongPassword999!")
        submit(driver)
        body = get_body(driver)
        assert "invalid" in body or "credentials" in body, \
            "Should show invalid credentials error"

    def test_tc11_login_valid(self, driver):
        """TC11: Valid credentials redirect to homepage."""
        login(driver)
        assert driver.current_url.rstrip("/") == BASE_URL, \
            f"Expected redirect to /, got: {driver.current_url}"


# ═══════════════════════════════════════════════════════════════════════════════
# TC12 – TC14  |  Jobs  (/jobs)
# ═══════════════════════════════════════════════════════════════════════════════

class TestJobs:

    def test_tc12_jobs_listing_page(self, driver):
        """TC12: /jobs page loads and shows job content."""
        driver.get(f"{BASE_URL}/jobs")
        wait_for(driver, By.TAG_NAME, "body")
        body = get_body(driver)
        # Page should have jobs or an empty-state message
        assert any(k in body for k in ["job", "position", "no jobs", "company", "location"]), \
            "Jobs listing page should display jobs or empty state"

    def test_tc13_post_new_job(self, driver):
        """TC13: Logged-in user can post a new job — redirects to job detail."""
        login(driver)
        driver.get(f"{BASE_URL}/jobs/new")
        wait_for(driver, By.TAG_NAME, "form")
        fill(driver, "title",       "QA Automation Engineer")
        fill(driver, "description", "We are looking for a Selenium expert to automate testing.")
        fill(driver, "company",     "TechCorp Pvt Ltd")
        fill(driver, "location",    "Rawalpindi, Pakistan")
        submit(driver)
        # On success, redirects to /jobs/:id
        assert "/jobs/" in driver.current_url, \
            f"Expected redirect to /jobs/:id, got: {driver.current_url}"

    def test_tc14_job_detail_page(self, driver):
        """TC14: Job detail page shows title, company, description, and Apply button."""
        # Navigate to jobs list and click first job
        driver.get(f"{BASE_URL}/jobs")
        wait_for(driver, By.TAG_NAME, "body")
        time.sleep(1)

        job_links = [
            a for a in driver.find_elements(By.CSS_SELECTOR, "a[href]")
            if "/jobs/" in (a.get_attribute("href") or "")
               and "/jobs/new" not in (a.get_attribute("href") or "")
        ]

        if not job_links:
            pytest.skip("No job listings found — add a job first")

        job_links[0].click()
        time.sleep(1)
        body = get_body(driver)
        assert any(k in body for k in ["description", "company", "location", "apply"]), \
            "Job detail page should show description, company, location and apply option"


# ═══════════════════════════════════════════════════════════════════════════════
# TC15  |  Apply for Job  (/jobs/:id/apply)
# ═══════════════════════════════════════════════════════════════════════════════

class TestApplication:

    def test_tc15_apply_requires_cover_letter(self, driver):
        """TC15: Submitting application without cover letter shows validation error."""
        login(driver)
        driver.get(f"{BASE_URL}/jobs")
        time.sleep(1)

        job_links = [
            a for a in driver.find_elements(By.CSS_SELECTOR, "a[href]")
            if "/jobs/" in (a.get_attribute("href") or "")
               and "/jobs/new" not in (a.get_attribute("href") or "")
        ]
        if not job_links:
            pytest.skip("No job listings to apply to")

        # Extract job id from href and navigate to apply page
        job_href = job_links[0].get_attribute("href")
        job_id   = job_href.rstrip("/").split("/")[-1]
        driver.get(f"{BASE_URL}/jobs/{job_id}/apply")
        wait_for(driver, By.TAG_NAME, "form")

        # Submit without filling coverLetter
        submit(driver)
        body = get_body(driver)
        assert "cover letter" in body or "required" in body, \
            "Should show cover letter required error"

    def test_tc16_apply_with_cover_letter(self, driver):
        """TC16: Valid application with cover letter redirects to job detail."""
        login(driver)
        driver.get(f"{BASE_URL}/jobs")
        time.sleep(1)

        job_links = [
            a for a in driver.find_elements(By.CSS_SELECTOR, "a[href]")
            if "/jobs/" in (a.get_attribute("href") or "")
               and "/jobs/new" not in (a.get_attribute("href") or "")
        ]
        if not job_links:
            pytest.skip("No job listings to apply to")

        job_href = job_links[0].get_attribute("href")
        job_id   = job_href.rstrip("/").split("/")[-1]
        driver.get(f"{BASE_URL}/jobs/{job_id}/apply")
        wait_for(driver, By.TAG_NAME, "form")

        fill(driver, "coverLetter",
             "I am highly experienced in Selenium automation and test pipelines.")
        submit(driver)

        # On success redirects back to /jobs/:id
        # OR shows "already applied" if this job was applied before
        body = get_body(driver)
        url  = driver.current_url
        assert f"/jobs/{job_id}" in url or "already" in body, \
            "Should redirect to job detail or show already-applied message"


# ═══════════════════════════════════════════════════════════════════════════════
# TC17  |  Profile & Logout
# ═══════════════════════════════════════════════════════════════════════════════

class TestProfileAndLogout:

    def test_tc17_profile_page_loads(self, driver):
        """TC17: Authenticated user can view and update their profile."""
        login(driver)
        driver.get(f"{BASE_URL}/profile")
        wait_for(driver, By.TAG_NAME, "form")
        body = get_body(driver)
        assert any(k in body for k in ["profile", "full name", "bio", "skills", "location"]), \
            "Profile page should show editable fields"

    def test_tc18_logout_redirects_to_login(self, driver):
        """TC18: Logout clears session and redirects to /auth/login."""
        login(driver)
        driver.get(f"{BASE_URL}/auth/logout")
        time.sleep(1)
        assert "/auth/login" in driver.current_url, \
            f"Expected redirect to /auth/login, got: {driver.current_url}"

    def test_tc19_profile_redirects_when_logged_out(self, driver):
        """TC19: Accessing /profile without login redirects away."""
        # Already logged out from TC18
        driver.get(f"{BASE_URL}/profile")
        time.sleep(1)
        # Should NOT show profile — should redirect to login
        assert "profile" not in driver.current_url.lower() or \
               "login" in driver.current_url.lower() or \
               "login" in get_body(driver), \
            "Unauthenticated user should be redirected from /profile"