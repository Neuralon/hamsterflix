import sqlite3
import json
import time

movies = [
  { "id": 1, "title": "Sunflower Seeds" },
  { "id": 2, "title": "The Maze Runner" },
  { "id": 3, "title": "Midnight Snack" },
  { "id": 4, "title": "Tube City" },
  { "id": 5, "title": "Cheek Pouches" },
  { "id": 6, "title": "Wheel of Time" },
  { "id": 7, "title": "Furry Fury" },
  { "id": 8, "title": "Bite Sized" },
  { "id": 9, "title": "Rodent Racer" },
  { "id": 10, "title": "The Great Cage" },
  { "id": 11, "title": "Wood Shavings" },
  { "id": 12, "title": "Sleep All Day" },
  { "id": 13, "title": "The Nut Job" },
  { "id": 14, "title": "Midnight Runner" },
  { "id": 15, "title": "Fuzz Ball" },
  { "id": 16, "title": "Cage Break" },
  { "id": 17, "title": "Squeak" },
  { "id": 18, "title": "The Burrow" },
  { "id": 19, "title": "Life in the Tubes" },
  { "id": 20, "title": "Seed Gatherers" },
  { "id": 21, "title": "Beyond the Wheel" },
  { "id": 22, "title": "Nocturnal Habits" },
  { "id": 23, "title": "The Escape Artist" },
  { "id": 24, "title": "Cheeks of Steel" },
  { "id": 25, "title": "Squeaky Clean" },
  { "id": 26, "title": "Drop the Seed" },
  { "id": 27, "title": "Hamster Dance" },
  { "id": 28, "title": "Stuck in the Tube" },
  { "id": 29, "title": "Wheel Fail" },
  { "id": 30, "title": "Bite Me" },
  { "id": 31, "title": "Space Hamster" },
  { "id": 32, "title": "The Galactic Cage" },
  { "id": 33, "title": "Alien Seeds" },
  { "id": 34, "title": "Tube Portals" },
  { "id": 35, "title": "Laser Eyes" },
  { "id": 36, "title": "Planet Fluff" },
  { "id": 37, "title": "The Cat Next Door" },
  { "id": 38, "title": "Shadows in the Cage" },
  { "id": 39, "title": "Lost in the Tubes" },
  { "id": 40, "title": "Midnight Squeak" },
  { "id": 41, "title": "The Hand" }
]

def generate_mock_vision_data(title):
    # Generates a contextual payload based on the movie title
    genres = {
        "Sci-Fi": ["Space Hamster", "The Galactic Cage", "Alien Seeds", "Tube Portals", "Laser Eyes", "Planet Fluff"],
        "Thriller": ["The Cat Next Door", "Shadows in the Cage", "Lost in the Tubes", "Midnight Squeak", "The Hand"],
        "Comedy": ["Squeaky Clean", "Drop the Seed", "Hamster Dance", "Stuck in the Tube", "Wheel Fail", "Bite Me"],
        "Documentary": ["Life in the Tubes", "Seed Gatherers", "Beyond the Wheel", "Nocturnal Habits", "The Escape Artist", "Cheeks of Steel"],
        "Action": ["Furry Fury", "Bite Sized", "Rodent Racer", "The Great Cage", "Wood Shavings", "Sleep All Day"]
    }
    
    genre = "Drama"
    for g, titles in genres.items():
        if title in titles:
            genre = g
            break
            
    moods = ["Exciting", "Furry", "Intense", "Squeaky", "Fast-Paced", "Heartwarming"]
    cast = ["Michael Douglas", "Chris Pratt", "Margot Robbie", "Jack Black", "Awkwafina", "Danny DeVito"]
    
    return {
        "cast": f"{random.choice(cast)}, {random.choice(cast)}",
        "director": random.choice(["Steven Spielberg", "Christopher Nolan", "Greta Gerwig", "Wes Anderson"]),
        "synopsis": f"In a world where the wheel never stops turning, one hamster must face the ultimate challenge. Experience '{title}' like never before in this epic {genre.lower()} tale of survival, seeds, and late-night running.",
        "genres": json.dumps([genre, random.choice(["Family", "Adventure", "Animation"])]),
        "mood": json.dumps([random.choice(moods), random.choice(moods)])
    }

conn = sqlite3.connect('hamsterflix.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    cast TEXT,
    director TEXT,
    synopsis TEXT,
    genres TEXT,
    mood TEXT
)
''')

import random
random.seed(42)

for movie in movies:
    print(f"Processing poster_{movie['id']}.png ({movie['title']}) via Vision API...")
    time.sleep(0.1) # Simulate API latency
    data = generate_mock_vision_data(movie['title'])
    
    cursor.execute('''
    INSERT OR REPLACE INTO movies (id, title, cast, director, synopsis, genres, mood)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (movie['id'], movie['title'], data['cast'], data['director'], data['synopsis'], data['genres'], data['mood']))

conn.commit()
conn.close()

print("Successfully processed all 41 posters and stored metadata into hamsterflix.db!")
