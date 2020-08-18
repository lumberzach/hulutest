import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# Setting options and path to your chrome profile.
options = Options()
options.add_argument("user-data-dir=C:\\Users\\Boxca\\AppData\\Local\\Google\\Chrome\\profiletwo")
driver = webdriver.Chrome(r"C:\Users\Boxca\Downloads\Drivers\chromedriver_win32 (1)\chromedriver.exe", options=options)

# Opening hulu to the search page
driver.get('https://www.hulu.com/search')
driver.find_element_by_xpath("//input[@placeholder='Search']").click()
search_box = WebDriverWait(driver, 4).until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
)

# Taking user's search string
search_query = input('What do you want to watch?')
search_box.send_keys(search_query)

# Gives user first 3 results and allows selection.
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.InstantSearch__Option a")))
search_result_count = len(driver.find_elements_by_css_selector('li.InstantSearch__Option a'))

print(
    f"Please enter choice from 1 to 3:") if search_result_count else print(
    "No result Found")

for num, element in enumerate(driver.find_elements_by_css_selector('li.InstantSearch__Option a'),
                              start=1):
    print(f"Enter {num} for {element.text}")
    if num == 3:
        break

choice = int(input())
if search_result_count < choice:
    print(f"Please enter only digits from 1 to 3")

javaScript = f"document.querySelectorAll('li.InstantSearch__Option a')[{choice - 1}].click();"
driver.execute_script(javaScript)


# Checking if the selection is a series with more than one season.
def has_seasons():
    try:
        time.sleep(.5)
        driver.find_element_by_css_selector('button.Select__control')
        return True

    except NoSuchElementException:
        return False


print(f"Seasons found: {has_seasons()}")


# Checking if the selection is a series.
def has_episodes():
    try:
        time.sleep(.5)
        driver.find_element_by_css_selector("#Episodes")
        return True

    except NoSuchElementException:
        return False


print(f"Episodes found: {has_episodes()}")


# Checking if the selection is a movie.
def is_movie():
    if not has_episodes():
        return True
    else:
        return False


print(f"Movie: {is_movie()}")


# Hulu changed the way the play button element was identified.
# This is the workaround to to select episode choice.
def play_episode():
    episode = driver.find_elements_by_class_name("StandardEmphasisHorizontalTileContent__prompt")[choice - 1]
    print(episode.text)
    print(episode.location)
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(episode, 25, -25)
    action.click()
    action.perform()


# Playing the selection
if is_movie():
    print("It's a movie, lets play it")
    driver.find_element_by_xpath("//a[@class='WatchAction__btn']").click()


# If selection has seasons, we find which season user would like to choose.
elif has_seasons():
    print("It's a series with more than one season, let's ask which season")

    # Finds out how many seasons available
    def get_seasons():
        season_dropdown = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Select__control"))
        )
        season_dropdown.click()

        return WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.Select__option")))

    seasons_list = get_seasons()
    seasons_count = len(seasons_list)

    for num, element in enumerate(seasons_list, start=1):
        print(f"Enter {num} for {element.text}")

    choice = int(input(f"Please enter choice from 1 to {seasons_count}:"))
    if seasons_count < choice:
        print(f"Please enter only digits from 1 to {seasons_count}")

    time.sleep(1)
    driver.find_elements_by_css_selector('.Select__menu-list li')[choice - 1].click()

    # Finds out how many episodes are in the given season
    def get_episodes():
        global episodes_exist
        episodes_exist = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "StandardEmphasisHorizontalTileContent__prompt")))
        return WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "StandardEmphasisHorizontalTileContent__prompt")))

    episode_list = get_episodes()
    episode_count = len(episode_list)

    for num, element in enumerate(episode_list, start=1):
        print(f"Enter {num} for Episode {num}")

    choice = int(input())
    play_episode()

    if episode_count < choice:
        print(f"Please enter only digits from 1 to {num}")


# Selecting an episode if it is a series with only one season.
else:
    print("It's a series with only one season")

    def get_episodes():
        global episodes_exist
        episodes_exist = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "StandardEmphasisHorizontalTileContent__prompt")))
        return WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "StandardEmphasisHorizontalTileContent__prompt")))

    get_episodes()
    episode_list = get_episodes()
    episode_count = len(episode_list)

    for num, element in enumerate(episode_list, start=1):
        print(f"Enter {num} for episode {num}")

    choice = int(input())
    play_episode()

    if episode_count < choice:
        print(f"Please enter only digits from 1 to {episode_count}")
