def display_top_collaborations():
    '''displays the ranking of tuples (director, actor,
and number of movies) for movies in which the director and actor worked together and the movie is
also listed in the top rated movie list. The list should be in descending ordered of the total number of
movies that director and that actor worked together. For equal values the order does not matter.
Notice that the number of movies in the imdb-top-casts.csv file exceeds the number of movies in imdb-
top-rated.csv. You may have to open the csv files like this: open(filename, 'r', encoding = 'utf-8').'''
    try:
        top_rated_movies = set()
        top_rated = open('imdb-top-rated.csv', 'r', encoding='utf-8')
        next(top_rated)  # Skip the header
        for line in top_rated:
            parts = line.strip().split(',')
            movie_title = parts[1]
            movie_year = parts[2]
            top_rated_movies.add((movie_title, movie_year))
        top_rated.close()

        collaborations = {}
        top_casts =  open('imdb-top-casts.csv', 'r', encoding='utf-8')
        next(top_casts)  # Skip the header
        for line in top_casts:
            parts = line.strip().split(',')
            movie_title = parts[0]
            movie_year = parts[1]
            director = parts[2]

            if (movie_title, movie_year) in top_rated_movies:
                for actor in parts[3:]:
                    key = (director, actor)

                    if key in collaborations:
                        collaborations[key] += 1
                    else:
                        collaborations[key] = 1

        top_casts.close()

        sorted_collaborations = sorted(collaborations.items(), key=lambda x: x[1], reverse=True)
        result = []
        for (director, actor), count in sorted_collaborations:
            result.append((director, actor, count))
        return result
    
    except FileNotFoundError as e:
        print(f"Unable to find a file with name: {e.filename} . Check spelling and placement of file.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def display_top_actors():
    '''displays the ranking of actors from the top grossing
    list ordered by the total box office money they acted in.'''
    try:
        movie_earnings = {}
        top_grossing =  open('imdb-top-grossing.csv', 'r', encoding='utf-8')
        next(top_grossing)  # Skip the header
        for line in top_grossing:
            parts = line.strip().split(',')
            movie_title = parts[1]
            movie_year = parts[2]
            box_office = int(parts[3].replace('$', '').replace(',', ''))  # Convert to integer
            movie_earnings[(movie_title, movie_year)] = box_office
        top_grossing.close()

        actor_earnings = {}
        top_casts = open('imdb-top-casts.csv', 'r', encoding='utf-8')
        for line in top_casts:
            parts = line.strip().split(',')
            movie_title = parts[0]
            movie_year = parts[1]
            movie_key = (movie_title, movie_year)
            if movie_key in movie_earnings:
                for actor in parts[3:]:
                    actor_earnings[actor] = actor_earnings.get(actor, 0) + movie_earnings[movie_key]
        top_casts.close()

        sorted_actors = sorted(actor_earnings.items(), key=lambda x: x[1], reverse=True)
        result = []
        for actor, earnings in sorted_actors:
            result.append((actor, earnings))
        return result
    
    except FileNotFoundError as e:
        print(f"Unable to find a file with name: {e.filename} . Check spelling and placement of file.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def main():
    display_num = int(input("Enter the number of entries to display: "))
    top_collaborations = display_top_collaborations()
    print("Top Collaborations (Director, Actor, Number of Movies):")
    for director, actor, count in top_collaborations[:display_num]:
        print(f"{director}, {actor}, {count}")

    top_actors = display_top_actors()
    print("\nTop Actors (Actor, Total Box Office Earnings):")
    for actor, earnings in top_actors[:display_num]:
        print(f"{actor}, ${earnings:,}")  # Format earnings with commas

if __name__ == "__main__":
    main()