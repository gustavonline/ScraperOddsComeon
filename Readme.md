
# ComeOn Odds Scraper

Arbitrage odds scraper used to find potential matches.

Developed using **Flask** for building the api endpoint. **Playwright** and **bs4** for scraping html data. **Streamlit** for a simple frontend gui.


## Run Locally

Clone the project

```bash
  git clone https://github.com/gustavonline/ScraperOddsComeon.git
```

Go to the project directory

```bash
  cd ScraperOddsComeon
```

Create enviroment

```bash
  python3.12 -m venv env
```

Activate enviroment
```bash
  source env/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```

Start the app

```bash
  streamlit run gui.py
```

Go to url

```bash
  http://localhost:8501
```




## API Reference

#### Get all matches that have an arbitrage

```http
  GET /scrape?date=2024-03-29
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `date` | `date` | **Required format** yyyy-mm-dd |

