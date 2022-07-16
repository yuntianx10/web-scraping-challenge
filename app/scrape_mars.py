from dataclasses import dataclass
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


def scrape_data():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()

    }

    browser.quit()
    return data


def mars_news(browser):
    # Scrape the Mars News Site and collect the latest News Title and Paragraph Test.
    news_url = "https://redplanetscience.com/"

    # Visit the Mars News site
    browser.visit(news_url)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        news_title = news_soup.select_one('div.list_text').find(
            'div', class_='content_title').get_text()
        news_p = news_soup.select_one('div.list_text').find(
            'div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_rel_url = img_soup.find('img', class_='headerimage').get('src')

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com/{img_rel_url}'

    return img_url


def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    df.columns = ['Properties', 'Mars', 'Earth']
    df.set_index('Properties', inplace=True)

    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    hemi_img_urls = []
    links = browser.find_by_css('a.product-item img')

    for i in range(len(links)):
        hemisphere_info = {}

        browser.find_by_css('a.product-item img')[i].click()

        img = browser.links.find_by_text('Sample').first
        hemisphere_info['img_url'] = img['href']
        hemisphere_info['title'] = browser.find_by_css('h2.title').text

        hemi_img_urls.append(hemisphere_info)

        browser.back()

    return hemi_img_urls


if __name__ == "__main__":

    print(scrape_data())
