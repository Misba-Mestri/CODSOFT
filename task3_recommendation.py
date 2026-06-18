"""
╔══════════════════════════════════════════════════════════════╗
║         CODSOFT AI INTERNSHIP — TASK 3                       ║
║         Movie Recommendation System                          ║
║         (Collaborative + Content-Based Filtering)            ║
║         Author: Your Name | CodSoft AI Intern               ║
╚══════════════════════════════════════════════════════════════╝

WHAT IT DOES:
  A movie recommendation engine using two techniques:
  1. Content-Based Filtering — recommends movies similar to ones
     you like, based on genre, director, and keywords.
  2. Collaborative Filtering — finds users with similar tastes
     and recommends what they loved (user-user similarity).

INSTALL DEPENDENCIES:
  pip install pandas numpy scikit-learn
"""

import sys

def check_dependencies():
    missing = []
    for pkg in ['pandas', 'numpy', 'sklearn']:
        try:
            __import__(pkg)
        except ImportError:
            missing.append('scikit-learn' if pkg == 'sklearn' else pkg)
    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
        print(f"   Run: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────────
#  SAMPLE DATASET
# ─────────────────────────────────────────────
MOVIES = pd.DataFrame({
    "movie_id": range(1, 21),
    "title": [
        "The Dark Knight", "Inception", "Interstellar", "The Matrix",
        "Avengers: Endgame", "Iron Man", "The Godfather", "Pulp Fiction",
        "Forrest Gump", "The Shawshank Redemption", "Titanic", "Avatar",
        "The Lion King", "Toy Story", "Finding Nemo", "Spirited Away",
        "Parasite", "1917", "Joker", "Dune"
    ],
    "genres": [
        "Action Crime Thriller", "Sci-Fi Thriller Mystery", "Sci-Fi Drama Adventure",
        "Sci-Fi Action Thriller", "Action Adventure Superhero", "Action Superhero Sci-Fi",
        "Crime Drama", "Crime Drama Thriller", "Drama Romance Comedy",
        "Drama", "Romance Drama Disaster", "Sci-Fi Action Adventure",
        "Animation Drama Musical", "Animation Comedy Adventure", "Animation Comedy Adventure",
        "Animation Fantasy Adventure", "Thriller Drama", "War Drama",
        "Crime Drama Psychological", "Sci-Fi Adventure Drama"
    ],
    "director": [
        "Nolan", "Nolan", "Nolan", "Wachowski",
        "Russo", "Favreau", "Coppola", "Tarantino",
        "Zemeckis", "Darabont", "Cameron", "Cameron",
        "Minkoff", "Lasseter", "Stanton", "Miyazaki",
        "Bong", "Mendes", "Phillips", "Villeneuve"
    ],
    "rating": [9.0, 8.8, 8.6, 8.7, 8.4, 7.9, 9.2, 8.9, 8.8, 9.3,
               7.8, 7.9, 8.5, 8.3, 8.1, 8.6, 8.5, 8.3, 8.4, 7.9]
})

# ─────────────────────────────────────────────
#  USER RATINGS (Collaborative Filtering)
# ─────────────────────────────────────────────
# Rows = users, Columns = movies (0 = not rated)
USER_RATINGS = pd.DataFrame({
    "The Dark Knight":   [5, 4, 0, 3, 0, 5, 4],
    "Inception":         [5, 5, 4, 0, 3, 4, 5],
    "Interstellar":      [4, 5, 5, 0, 4, 3, 5],
    "The Matrix":        [4, 3, 0, 5, 0, 4, 3],
    "Avengers: Endgame": [3, 0, 2, 5, 5, 3, 0],
    "Iron Man":          [3, 0, 0, 5, 5, 2, 0],
    "The Godfather":     [0, 4, 3, 0, 0, 5, 4],
    "Pulp Fiction":      [0, 4, 4, 0, 0, 5, 4],
    "Forrest Gump":      [0, 3, 5, 0, 3, 4, 3],
    "The Shawshank Redemption": [0, 4, 5, 0, 2, 5, 4],
    "Parasite":          [0, 4, 5, 0, 0, 4, 5],
    "1917":              [0, 3, 4, 0, 0, 3, 4],
    "Joker":             [4, 4, 3, 2, 0, 4, 4],
    "Dune":              [3, 5, 4, 3, 2, 3, 5],
}, index=["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace"])

# ─────────────────────────────────────────────
#  1. CONTENT-BASED FILTERING
# ─────────────────────────────────────────────
def build_content_model():
    """Build TF-IDF matrix over genres + director."""
    MOVIES["features"] = MOVIES["genres"] + " " + MOVIES["director"]
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(MOVIES["features"])
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return similarity

CONTENT_SIM = build_content_model()

def content_based_recommend(movie_title: str, n: int = 5):
    """Return top N movies similar to the given title."""
    titles = MOVIES["title"].tolist()
    if movie_title not in titles:
        return None
    idx = titles.index(movie_title)
    scores = list(enumerate(CONTENT_SIM[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]
    recs = []
    for i, score in scores:
        recs.append({
            "title": MOVIES.iloc[i]["title"],
            "genres": MOVIES.iloc[i]["genres"],
            "rating": MOVIES.iloc[i]["rating"],
            "similarity": round(score * 100, 1)
        })
    return recs

# ─────────────────────────────────────────────
#  2. COLLABORATIVE FILTERING
# ─────────────────────────────────────────────
def collaborative_recommend(user_name: str, n: int = 5):
    """Find similar users and recommend movies the user hasn't seen."""
    if user_name not in USER_RATINGS.index:
        return None

    # Cosine similarity between users
    user_matrix = USER_RATINGS.values.astype(float)
    sim = cosine_similarity(user_matrix)
    sim_df = pd.DataFrame(sim, index=USER_RATINGS.index, columns=USER_RATINGS.index)

    # Find the most similar users (excluding self)
    user_sims = sim_df[user_name].drop(user_name).sort_values(ascending=False)
    top_users = user_sims.head(3).index.tolist()

    # Movies the current user hasn't rated
    user_ratings = USER_RATINGS.loc[user_name]
    unseen = user_ratings[user_ratings == 0].index.tolist()

    # Score unseen movies by weighted average from similar users
    scores = {}
    for movie in unseen:
        weighted_sum = 0
        sim_sum = 0
        for similar_user in top_users:
            rating = USER_RATINGS.loc[similar_user, movie]
            if rating > 0:
                sim_weight = user_sims[similar_user]
                weighted_sum += rating * sim_weight
                sim_sum += sim_weight
        if sim_sum > 0:
            scores[movie] = weighted_sum / sim_sum

    if not scores:
        return []

    sorted_recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
    recs = []
    for title, score in sorted_recs:
        movie_info = MOVIES[MOVIES["title"] == title]
        if not movie_info.empty:
            recs.append({
                "title": title,
                "genres": movie_info.iloc[0]["genres"],
                "predicted_rating": round(score, 2),
                "similar_to": top_users
            })
    return recs

# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────
def print_separator():
    print("─" * 55)

def show_content_recs(movie: str):
    print(f"\n🎬 Content-Based Recommendations for: \"{movie}\"")
    print_separator()
    recs = content_based_recommend(movie)
    if recs is None:
        print(f"❌ Movie '{movie}' not found in database.")
        print(f"   Available: {', '.join(MOVIES['title'].tolist())}")
        return
    for i, r in enumerate(recs, 1):
        stars = "★" * int(r["rating"] / 2)
        print(f"  {i}. {r['title']}")
        print(f"     Genre: {r['genres']}")
        print(f"     Rating: {r['rating']} {stars}  |  Similarity: {r['similarity']}%")
    print_separator()

def show_collab_recs(user: str):
    print(f"\n👤 Collaborative Recommendations for: {user}")
    print_separator()
    recs = collaborative_recommend(user)
    if recs is None:
        print(f"❌ User '{user}' not found.")
        print(f"   Known users: {', '.join(USER_RATINGS.index.tolist())}")
        return
    if not recs:
        print("  No new recommendations (all movies already rated).")
        return
    for i, r in enumerate(recs, 1):
        print(f"  {i}. {r['title']}")
        print(f"     Genre: {r['genres']}")
        print(f"     Predicted Rating: ⭐ {r['predicted_rating']}/5")
    print_separator()

def interactive_menu():
    while True:
        print("\n┌─────────────────────────────────────┐")
        print("│     🎥 Movie Recommender System     │")
        print("│     CodSoft AI Internship Task 3    │")
        print("├─────────────────────────────────────┤")
        print("│  1. Content-Based Recommendations   │")
        print("│  2. Collaborative Recommendations   │")
        print("│  3. Show All Movies                 │")
        print("│  4. Show All Users                  │")
        print("│  5. Exit                            │")
        print("└─────────────────────────────────────┘")

        choice = input("\nChoose (1–5): ").strip()

        if choice == "1":
            movie = input("Enter a movie title: ").strip()
            show_content_recs(movie)

        elif choice == "2":
            user = input("Enter user name: ").strip()
            show_collab_recs(user)

        elif choice == "3":
            print("\n🎬 All Movies in Database:")
            print_separator()
            for _, row in MOVIES.iterrows():
                print(f"  {row['movie_id']:2}. {row['title']:<35} ⭐{row['rating']}")
            print_separator()

        elif choice == "4":
            print(f"\n👥 Known Users: {', '.join(USER_RATINGS.index.tolist())}")

        elif choice == "5":
            print("\nGoodbye! 🎬\n")
            break
        else:
            print("⚠️  Invalid choice. Please enter 1–5.")

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("   🎬 Movie Recommendation System — Task 3")
    print("=" * 55)

    # Quick demo
    print("\n📌 DEMO: Content-Based")
    show_content_recs("Inception")

    print("\n📌 DEMO: Collaborative Filtering")
    show_collab_recs("Alice")

    # Interactive mode
    interactive_menu()

if __name__ == "__main__":
    main()
