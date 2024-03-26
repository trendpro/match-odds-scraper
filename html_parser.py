# html_parser.py
from bs4 import BeautifulSoup
import json
from date_util import parse_event_date
import datetime


def parse_html_dump(html_dump):
    """
    Parse HTML dump to extract event data.

    Args:
        html_dump (str): HTML dump string.

    Returns:
        list: List of dictionaries containing fixtures.

    """

    soup = BeautifulSoup(html_dump, "html.parser")
    data = []

    # Get the current timestamp in UTC
    current_time_utc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")

    events = soup.find_all(
        "ms-event", class_="grid-event ms-active-highlight ng-star-inserted"
    )

    for event in events:
        event_data = {}

        # Extract tournament name
        tournament_name = (
            event.find_previous("ms-league-header")
            .find("div", class_="title")
            .text.strip()
        )
        event_data["tournament"] = tournament_name

        event_details = event.find("ms-event-detail", class_="grid-event-detail")
        if event_details:
            event_name = event_details.find("ms-event-name", class_="grid-event-name")
            if event_name:
                event_name_text = event_name.text.strip()
                if "-" in event_name_text:
                    tournament, event_name = map(
                        str.strip, event_name_text.split("-", 1)
                    )
                    event_data["eventName"] = event_name

            participants = event_details.find_all("div", class_="participant")
            if len(participants) == 2:
                player1_name = participants[0].text.strip()
                player2_name = participants[1].text.strip()
                event_data["player1"] = player1_name
                event_data["player2"] = player2_name

                # Concatenate player names to create eventName
                event_data["eventName"] = f"{player1_name} vs {player2_name}"

            event_info = event_details.find("ms-event-info", class_="grid-event-info")
            if event_info:
                timer = event_info.find(
                    "ms-prematch-timer",
                    class_="starting-time timer-badge ng-star-inserted",
                )
                if timer:
                    # Parse and format event date
                    event_date = parse_event_date(timer.text.strip())
                    if event_date:
                        event_data["eventDate"] = event_date.strftime("%Y-%m-%d %H:%M")

        options = event.find_all("ms-option-group")
        for option in options:
            odds = option.find_all("ms-font-resizer")
            if len(odds) == 2:
                player1_odds = (
                    odds[0].text.strip().split()[0]
                )  # Extracting the odds from text content
                player2_odds = (
                    odds[1].text.strip().split()[0]
                )  # Extracting the odds from text content
                event_data["player1_odds"] = player1_odds
                event_data["player2_odds"] = player2_odds
                break  # Assuming only one set of odds is needed, exit loop once found

        # Add additional properties
        event_data["lastUpdate"] = current_time_utc

        data.append(event_data)

    return data


def save_data_as_json(data, json_file_path):
    """
    Save event data as JSON.

    Args:
        data (list): List of dictionaries containing event data.
        json_file_path (str): File path to save the JSON data.

    """

    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)
