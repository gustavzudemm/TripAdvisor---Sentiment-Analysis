from helium import *
from review import TripAdvisorReview
from pprint import pprint
import dataclasses
from dataclasses import dataclass
import time
import string
import random
import re
import pandas as pd



''' Scrolling the page'''
def scroll_page(pagination: int):

    if pagination == 0:
        first_page_url = 'https://www.tripadvisor.de/Airline_Review-d8729177-Reviews-United-Airlines.html#REVIEWS'

        '''Check currently scraped page'''
        print(first_page_url)
        start_firefox(headless=True)
        go_to(first_page_url)
    else:
        url_paginated = f'https://www.tripadvisor.de/Airline_Review-d8729177-Reviews-or{pagination}-United-Airlines.html#REVIEWS'

        '''Check currently scraped page'''
        print(url_paginated)
        start_firefox(headless=True)
        go_to(url_paginated)

    ''' Scrolling routine '''
    click('Akzeptieren')
    scroll_down(150)
    time.sleep(1)
    # scroll_down(2500)

''' Scrolling after scraping the ratings first'''
def scroll_delay():
    click('Mehr lesen')
    scroll_down(500)

def get_ratings() -> list[int]:
    review_stars = find_all(S('.ui_bubble_rating'))

    # Only the last five ratings are review-related
    review_stars = review_stars[11:]

    # Convert Helium class objects to string objects
    review_stars = [str(stars) for stars in review_stars]

    # Extracting digits and converting to single digits
    star_ratings = [re.findall(r"\d+", stars) for stars in review_stars]
    star_ratings = [int(stars[0]) for stars in star_ratings]
    star_ratings = [rating / 10 for rating in star_ratings]

    return star_ratings

def get_review_titles() -> list[str]:

    review_titles = find_all(S('.Qwuub'))
    titles = [item.web_element.text for item in review_titles]
    return titles

def get_review_texts() -> list[str]:
    review_text = find_all(S('.QewHA'))
    review_text = [review.web_element.text for review in review_text]

    return review_text

def get_travel_dates() -> list[str]:

    dates = find_all(S('.teHYY'))
    dates = [date.web_element.text for date in dates]

    # Convert to datetime
    months = [date.split(' ')[1] for date in dates]
    years = [date.split(' ')[2] for date in dates]
    # months_num = [month_ger[month] for month in months]

    datetime_obj = [f'{month} {year}' for year, month in zip(years, months)]

    return datetime_obj

def get_flight_connections():

    headers = find_all(S('.tNvbV'))
    headers = [header.web_element.text for header in headers]
    flight_connections = [header.split('\n')[0] for header in headers]

    return flight_connections


''' Generate unique ID for each Review '''
def generate_uid() -> str:

    # Define the pool of characters to choose from
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(8))
    return unique_id

    
def extract(starting_page: int= 0, number_of_pages: int = 5) -> list[dict]:

    review_list = []

    for i in range(starting_page, number_of_pages, 5):

        try:

            print(f'Scraping page {i} of {number_of_pages}...')

            scroll_page(i)
            star_ratings = get_ratings()
            scroll_delay()
            # review_titles = get_review_titles()
            review_texts = get_review_texts()
            print(review_texts)
            # travel_dates = get_travel_dates()
            # flight_connections = get_flight_connections()

            kill_browser()

            ''' Create dictionaries and append them to review_list '''
            for rating, text in zip(star_ratings, review_texts):
                review = {}
                review['_id'] = generate_uid()
                # review['title'] = title
                review['rating'] = rating
                review['text'] = text
                # review['date'] = date
                # review['connection'] = connection
                review['airline'] = 'Singapore Airlines'

                ''' Single Review scraped feedback'''
                print(f'Review with ID: {review["_id"]} scraped!')

                review_list.append(review)
            
            ''' Set sleeping time to avoid too many requests in a short period of time'''
            if (i != number_of_pages-5):
                # sleeping_time = random.randint(5,10)
                sleeping_time = random.randint(10,15)
                print(f'Sleeping time: {sleeping_time} sec.')
                time.sleep(sleeping_time)
        except LookupError:
            print("LookupError: continue scraping...")

        except TypeError:
            print("Browser Window closed: continue scraping...")

        except Exception as e:
            print("Unknown error occurred: continue scraping...")
            time.sleep(10)

    return review_list

def transform(reviews: list[dict]) -> list[TripAdvisorReview]:

    review_dataobj = []
    
    for review in reviews:

        id = review['_id']
        # title = review['title']
        text = review['text']
        rating = review['rating']
        # flight_date = review['date']
        # flight_connection = review['connection']
        airline_name = review['airline']

        ta_review = TripAdvisorReview(id, None, text, rating, None, None, airline_name, None, None, None, None)
        review_dataobj.append(ta_review)
    
    return review_dataobj

def load(reviews: list[TripAdvisorReview], number_of_pages: int):
    
    review_dict = []

    for ta_review in reviews:
        review = dataclasses.asdict(ta_review)
        review_dict.append(review)

    df = pd.DataFrame.from_records(review_dict)
    df.to_csv(f'tripadvisor_airline_ua_batch_{number_of_pages}.csv', encoding='UTF-8')
        

def main():

    # Params
    pages = 685
    starting_at = 0

    # First 100 Batch
    review_list = extract(starting_page=starting_at, number_of_pages=pages)
    review_list = transform(review_list)
    load(reviews=review_list, number_of_pages=pages)


if __name__ == "__main__":
    main()