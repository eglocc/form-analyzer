import requests
from bs4 import BeautifulSoup


def get_data(team: str) -> list:
    """
    Gets the fixture and game results data of the given team.
    :param team: str
        Name of the team (does not expect any format)
    :return: list
        A list of data containing team names and game results
    """
    def format_team() -> str:
        import re
        import unicodedata
        english_check = re.compile(r'[a-z]|[A-Z]')
        formatted_team = team.lower().strip().replace(' ', '-')
        if not english_check.match(team):
            normalized_team = unicodedata.normalize('NFD', formatted_team)
            return u"".join([c for c in normalized_team if not unicodedata.combining(c)])
        return formatted_team

    formatted_team = format_team()
    url = f'https://www.sporx.com/{formatted_team}-fiksturu-ve-mac-sonuclari'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='table table-fixture')
    return table.find_all_next('td', class_=['td-team-name', 'td-team-score'])


def format_data(cells: list) -> list:
    """
    Groups the fixture of the team into a list. Each element contains information about a single game.
    :param cells: list
        A list of data containing team names and match scores
    :return: list
        A list of lists containing elements which are grouped by [{home_team}, {score}, {away_team}]
    """
    result, fixture = [], []
    for i in range(0, len(cells)):
        result.append(cells[i].text.strip())
        if i % 3 == 2:
            fixture.append(result)
            result = []
    return fixture


def analyze_form(fixture: list) -> list:
    """
    Maps the games results to states.
    :param fixture: list
        A list of lists containing elements which are grouped by [{home_team}, {score}, {away_team}]
    :return: list
        A list in which elements are single characters of 'W', 'D' or 'L' representing respectively "Won", "Draw" or
        "Lost"
    """
    streak = []
    for match in fixture:
        home_team, score, away_team = match
        try:
            home_score, away_score = score.split('-')
        except ValueError:
            break
        if home_score == away_score:
            letter = 'D'
        elif my_team == home_team:
            letter = 'W' if home_score > away_score else 'L'
        else:
            letter = 'L' if home_score > away_score else 'W'
        streak.append(letter)
    return streak


if __name__ == '__main__':
    # Team name should be entered in word capitalized form.
    # TODO: Handle word capitalization automatically in script
    my_team = input('Type your team\'s name: ')
    print('analyzing form...')
    data = get_data(my_team)
    fixture = format_data(data)
    streak = analyze_form(fixture)
    print(streak)
