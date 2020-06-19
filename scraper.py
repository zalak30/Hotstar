# import libraries
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import numpy as np
import mysql.connector
import conn

# create empty list
episodes = []


# scrape the data
async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('https://www.hotstar.com/in/tv/iss-pyar-ko-kya-naam/s-29/list/episodes/t-1_2_29')

    while len(episodes) <= 400:
        html = await page.evaluate('''() => {
            return document.querySelector('.resClass').innerHTML;
        }''')

        # find episode date, link and detail
        episodes_html = BeautifulSoup(html, 'html.parser')
        for episode in episodes_html:
            link = episode.find('a')
            date = episode.find('div', {'class': 'title ellipsize'})
            des = episode.find('div', {'class': 'description ellipsize'})

            # check if value is None
            if link is not None and date is not None and des is not None:
                episode = (date.find('span', {'class': 'subtitle'}).get_text(), link.get('href'),  des.get_text())

                # append episode detail to "episodes" list
                if episode not in episodes:
                    episodes.append(episode)

        # scroll the page
        await page.evaluate('window.scroll(0, document.body.scrollHeight)')
        await asyncio.sleep(np.random.randint(5, 8))  # will wait to sending requests for 5 to 8 seconds
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
print(len(episodes))

# connect to sql
mydb = mysql.connector.connect(
  host=conn.host,
  user=conn.user,
  passwd=conn.passwd,
  database=conn.database
)

mycursor = mydb.cursor()

# add data in table
sql = "INSERT INTO serial(Date, Link, Description) VALUES(%s, %s, %s)"
mycursor.executemany(sql, episodes)

mydb.commit()
print(mycursor.rowcount, "record was inserted.")
