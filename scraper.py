from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime


def is_valid_match(odds):
    sum_odds = sum(odds)
    return all(odd >= 1.80 for odd in odds) and sum_odds >= 8.50


def scrape_with_date(date_str):
    formatted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    url = f"https://www.comeon.com/da/sportsbook/sports/1-fodbold/upcoming/{formatted_date}"
    scraped_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Change headless to False if you want to see the browser window
        page = browser.new_page()
        page.goto(url)
        # Wait for the content to load; adjust the selector as needed
        page.wait_for_selector('div[class="sportsbook-column-layout__ColumnLayoutContainer-sc-zksktt-1 cYZprt"]')
        html = page.inner_html('div[class="sportsbook-column-layout__ColumnLayoutContainer-sc-zksktt-1 cYZprt"]')

        soup = BeautifulSoup(html, 'html.parser')

        dates_times = soup.find_all('small', class_='sportsbook-game-card__UpcomingGameTime-sc-q3kmnq-5')
        teams = soup.find_all('p', class_='sportsbook-event-scoreboard__ScoreboardParticipantLabel-sc-ksfxup-1')
        odds = soup.find_all('small', class_='selection-button__SelectionButtonOdds-sc-1msr0zh-1')

        for i in range(0, len(teams), 2):  # Assuming two teams per match
            if (i // 2 * 3 + 2) < len(odds):
                match_odds = [float(odds[j].text) for j in range(i // 2 * 3, i // 2 * 3 + 3)]
                if is_valid_match(match_odds):
                    scraped_data.append({
                        "Date and Time": dates_times[i // 2].text,
                        "Teams": f"{teams[i].text} vs {teams[i + 1].text}",
                        "Odds": ", ".join(str(odd) for odd in match_odds),
                        "Sum of Odds": sum(match_odds)
                    })
        browser.close()
    return scraped_data
