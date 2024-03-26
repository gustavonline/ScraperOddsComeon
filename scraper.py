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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('div[class="sportsbook-column-layout__ColumnLayoutContainer-sc-zksktt-1 cYZprt"]')
        html = page.inner_html('div[class="sportsbook-column-layout__ColumnLayoutContainer-sc-zksktt-1 cYZprt"]')

        soup = BeautifulSoup(html, 'html.parser')

        # Find each league group
        league_groups = soup.find_all('div', class_='sportsbook-game-card-group__GameCardGroup-sc-glf6kw-1')

        for league_group in league_groups:
            league_header = league_group.find('h5',
                                              class_=lambda x: x and 'sportsbook-game-card-list-header__Title' in x)

            if league_header:  # Check if the league header was found
                league_name = league_header.text
            else:
                league_name = "Unknown League"  # Default or placeholder value if not found

            matches = league_group.find_all('div', class_='sportsbook-game-card-base__GameCardWrapper-sc-148z13o-0')

            for match in matches:
                dates_times = match.find('small', class_='sportsbook-game-card__UpcomingGameTime-sc-q3kmnq-5')
                teams = match.find_all('p',
                                       class_='sportsbook-event-scoreboard__ScoreboardParticipantLabel-sc-ksfxup-1')
                odds = match.find_all('small', class_='selection-button__SelectionButtonOdds-sc-1msr0zh-1')

                if len(teams) == 2 and len(odds) >= 3:
                    match_odds = [float(od.text) for od in odds[:3]]
                    if is_valid_match(match_odds):
                        scraped_data.append({
                            "Date and Time": dates_times.text if dates_times else "N/A",
                            "Teams": f"{teams[0].text} vs {teams[1].text}" if len(teams) > 1 else "Unknown Teams",
                            "Odds": ", ".join(str(odd) for odd in match_odds),
                            "Sum of Odds": sum(match_odds),
                            "League": league_name
                        })

        browser.close()
    return scraped_data
