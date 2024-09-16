import requests
from bs4 import BeautifulSoup
import csv
import random  # Import the random module

# IMBD url to scrape from
url = 'https://www.imdb.com/title/tt0141842/quotes/'

# Define headers to mimic browser request and circumvent error 403
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request with headers
response = requests.get(url, headers=headers)

# Check if the request worked
if response.status_code == 200:
    print("Page was fetched successfully")
    html_content = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the elements containing quotes (list items)
    quote_items = soup.find_all('li')  # Look for all <li> elements

    # Extract the quotes and save them to a list
    quotes = []
    for item in quote_items:
        # Find the text after the <a> tag
        actor = item.find('a')  # Extract the actor name from the <a> tag
        if actor:
            quote_text = item.get_text().split(':', 1)[-1].strip()  # Extract text after ":"
            if quote_text:
                full_quote = f"{actor.get_text()} : {quote_text}"  # Combine actor and quote
                quotes.append(full_quote)  # Save the full quote to the list

    # Check if quotes were found
    if quotes:
        # Select a random quote
        random_quote = random.choice(quotes)
        print(f"Random Quote: {random_quote}")

        # Save all quotes to a CSV file (optional)
        with open('sopranos_quotes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Quote"])  # Write header row
            writer.writerows([[quote] for quote in quotes])  # Write all quotes to the file

        print(f"Saved {len(quotes)} quotes to 'sopranos_quotes.csv'")
    else:
        print("No quotes found.")
else:
    print("Failed to retrieve the page:", response.status_code)
