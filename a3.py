from songs import song_db  # Assume this is your song database
from match import match
from typing import List, Tuple, Callable, Any

# Projection functions for accessing song properties
def get_title(song: Tuple[str, str, int, List[str]]) -> str:
    return song[0]

def get_artist(song: Tuple[str, str, int, List[str]]) -> str:
    return song[1]

def get_year(song: Tuple[str, str, int, List[str]]) -> int:
    return song[2]

def get_genres(song: Tuple[str, str, int, List[str]]) -> List[str]:
    return song[3]

# Functions to find songs based on different criteria
def title_by_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    return [get_title(song) for song in song_db if get_year(song) == year]

def title_by_year_range(matches: List[str]) -> List[str]:
    start_year = int(matches[0])
    end_year = int(matches[1])
    return [get_title(song) for song in song_db if start_year <= get_year(song) <= end_year]

def title_before_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    return [get_title(song) for song in song_db if get_year(song) < year]

def title_after_year(matches: List[str]) -> List[str]:
    year = int(matches[0])
    return [get_title(song) for song in song_db if get_year(song) > year]

def artist_by_title(matches: List[str]) -> List[str]:
    title = matches[0]
    return [get_artist(song) for song in song_db if get_title(song) == title]

def title_by_artist(matches: List[str]) -> List[str]:
    artist = matches[0]
    return [get_title(song) for song in song_db if get_artist(song) == artist]

def genres_by_title(matches: List[str]) -> List[str]:
    title = matches[0]
    for song in song_db:
        if get_title(song) == title:
            return get_genres(song)
    return []

def year_by_title(matches: List[str]) -> List[int]:
    title = matches[0]
    for song in song_db:
        if get_title(song) == title:
            return [get_year(song)]
    return []

def title_by_genre(matches: List[str]) -> List[str]:
    genre = matches[0]
    return [get_title(song) for song in song_db if genre in get_genres(song)]

def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt

# Pattern-action mapping
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what songs were made in _"), title_by_year),
    (str.split("what songs were made between _ and _"), title_by_year_range),
    (str.split("what songs were made before _"), title_before_year),
    (str.split("what songs were made after _"), title_after_year),
    (str.split("who is the artist of %"), artist_by_title),
    (str.split("what songs were performed by %"), title_by_artist),
    (str.split("what genres does % belong to"), genres_by_title),
    (str.split("when was % released"), year_by_title),
    (str.split("what songs belong to the genre %"), title_by_genre),
    (["bye"], bye_action),
]

def search_pa_list(src: List[str]) -> List[str]:
    for pattern, action in pa_list:
        value = match(pattern, src)
        if value is not None:
            result = action(value)
            if result:
                return result
            return ["No answers"]
    return ["I don't understand"]

def query_loop() -> None:
    print("Welcome to the song database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)
        except (KeyboardInterrupt, EOFError):
            break
    print("\nSo long!\n")

if __name__ == "__main__":
    # Test assertions (you need to fill song_db accordingly)
    assert isinstance(title_by_year(["2014"]), list), "title_by_year not returning a list"
    assert sorted(title_by_year(["2014"])) == sorted(["song1", "song2"]), "failed title_by_year test"

    assert isinstance(title_by_year_range(["2010", "2013"]), list), "title_by_year_range not returning a list"
    assert sorted(title_by_year_range(["2010", "2013"])) == sorted(["song3", "song4"]), "failed title_by_year_range test"

    assert isinstance(title_before_year(["2012"]), list), "title_before_year not returning a list"
    assert sorted(title_before_year(["2012"])) == sorted(["song5", "song6"]), "failed title_before_year test"

    assert isinstance(title_after_year(["2013"]), list), "title_after_year not returning a list"
    assert sorted(title_after_year(["2013"])) == sorted(["song7", "song8"]), "failed title_after_year test"

    assert isinstance(artist_by_title(["song1"]), list), "artist_by_title not returning a list"
    assert sorted(artist_by_title(["song1"])) == sorted(["artist1"]), "failed artist_by_title test"

    assert isinstance(title_by_artist(["artist1"]), list), "title_by_artist not returning a list"
    assert sorted(title_by_artist(["artist1"])) == sorted(["song1"]), "failed title_by_artist test"

    assert isinstance(genres_by_title(["song1"]), list), "genres_by_title not returning a list"
    assert sorted(genres_by_title(["song1"])) == sorted(["pop", "rock"]), "failed genres_by_title test"

    assert isinstance(year_by_title(["song1"]), list), "year_by_title not returning a list"
    assert sorted(year_by_title(["song1"])) == sorted([2014]), "failed year_by_title test"

    assert isinstance(title_by_genre(["rock"]), list), "title_by_genre not returning a list"
    assert sorted(title_by_genre(["rock"])) == sorted(["song1", "song2"]), "failed title_by_genre test"

    assert sorted(search_pa_list(["hi", "there"])) == sorted(["I don't understand"]), "failed search_pa_list test 1"
    assert sorted(search_pa_list(["what", "songs", "were", "made", "in", "2014"])) == sorted(["song1", "song2"]), "failed search_pa_list test 2"
    
    print("All tests passed!")

