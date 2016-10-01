#!/usr/bin/env python

import csv
import operator
import sys
from collections import OrderedDict

"""
Q1. Given a user who has rated x amount of movies that have been watched, what are
the movies that have a high likelihood of being rated similarly by the user?

-> Using dissimilarity measure: d(i, j) = (p - m)/p

Workflow:
- Functions are named sequentially, in the format  s1()...sN()
- Output files of each function are named following the format a1-.csv...aN-.csv

s1()
- Process the input.csv data, extract rows where movie-rating tuples match with input

s2()
- Sort the users that have the most movie-rating tuples agreement with the input user
- After above sorting, print counts for each frequency

s3()
- Get the userIDs with high agreement values

s4()
- Get all movie-rating tuples by high agreement users

s5()
- Sort movies column by distinct movies
- After above sorting, get counts of # of movie-rating tuples for each movie

s6()
- Extract the movies with # ratings above a certain threshold
- Extract the movie-rating tuples
- Average the ratings per movie

s7()
- Using raw recommendation data, get the movie titles and only return those above min_avg_rating


TODO: create support lookup table: movieID - Rating(0.5-5.0) - Count - %
"""


def s1(input_file):
    """
    Process the input.csv data, extract rows where movie-rating tuples match with input

    input_file: CSV file - the ml-ratings.csv has columns: ['userId', 'movieId', 'rating', 'timestamp']
    """
    input_data = open(input_file, "r").readlines()[1:]

    input_user = []
    input_movie_and_ratings = []
    for ln in input_data:
        ln = ln.split(",")
        input_movie_and_ratings.append([ln[1], ln[2]])  # [float(ln[1]), float(ln[2])])
        if ln[0] not in input_user:
            input_user.append(ln[0])  # int(ln[0]))
    #print ">>> Movie-Rating Tuples: " + str(input_movie_and_ratings)
    #print ">>> Input User(s): " + str(input_user)

    #print ">>> Accessing ratings data..."
    ratings = open("../data/ml-ratings-lean.csv", "r").readlines()[1:]

    count = 0
    total = float(len(ratings))
    for ln in ratings:  # range(0, len(ratings)):
        count += 1  # Progress Bar
        #p = count / total * 100.0
        #sys.stdout.write("\r>>> Ratings processed: %d (%i%%)" % (count, p))
        #sys.stdout.flush()

        ln2 = ln.split(",")
        pair = [ln2[1], ln2[2].strip()]

        # pair = [ratings[ln][1], ratings[ln][2]]
        # if pair in input_movie_and_ratings and ratings[ln][0] not in input_user:
        if pair in input_movie_and_ratings and ln2[0] not in input_user:
            with open("../data/output/a1-ratings-extract.csv", "a") as f:
                f.write(ln)
                # f.write(','.join([str(ratings[ln][0]), str(ratings[ln][1]), str(ratings[ln][2]), '\n']))

    print "\nDone s1\n"


def s2():
    """
    Sort the users that have the most movie-rating tuples agreement with the input user
    """
    data = open("../data/output/a1-ratings-extract.csv", "r").readlines()
    ratings_count = 1
    ratings_count_list = []
    ratings_count_list_uniques = []

    for n in range(0, len(data)):
        row1 = data[n].split(",")
        try:
            row2 = data[n + 1].split(",")
        except IndexError:  # exception thrown when file reaches end of line
            #print ">>> Max Agreement: " + str(max(ratings_count_list))
            ratings_count_list_uniques.sort()
            #print ">>> Freqs Present: " + str(ratings_count_list_uniques)

        user_id1 = row1[0]
        user_id2 = row2[0]

        if user_id1 == user_id2:
            ratings_count += 1
        if user_id1 != user_id2:

            with open("../data/output/a2-ratings-extract-counts-by-user.csv", "a") as f:
                f.write(user_id1 + "," + str(ratings_count) + "\n")
                ratings_count_list.append(ratings_count)
                if ratings_count not in ratings_count_list_uniques:
                    ratings_count_list_uniques.append(ratings_count)
            ratings_count = 1

    output = open("../data/output/a2-ratings-extract-counts-by-user.csv", "r").readlines()
    #print ">>> # Output Rows: " + str(len(output))


    """
    After above sorting, print counts for each frequency
    """
    output = open("../data/output/a2-ratings-extract-counts-by-user.csv", "r").readlines()

    count_dict = {}
    for n in range(0, len(output)):
        row1 = output[n].split(",")

        count1 = int(row1[1].strip())

        if count1 not in count_dict:
            count_dict[count1] = 0
        if count1 in count_dict:
            count_dict[count1] += 1

    OrderedDict(sorted(count_dict.items(), key=lambda t: t[0]))
    #print ">>> Distribution : " + str(count_dict)

    for i in count_dict:
        with open("../data/output/a2-ratings-extract-counts-by-user-distrib.csv", "a") as f:
            f.write(str(i) + ',' + str(count_dict[i]) + '\n')

    print "Done s2\n"


def s3(lower_limit=6, upper_limit=8):
    """
    Get the userIDs with high agreement values
    """
    data = open("../data/output/a2-ratings-extract-counts-by-user.csv", "r").readlines()
    agreeing_users = []

    for n in range(0, len(data)):
        row1 = data[n].split(",")
        count = int(row1[1].strip())

        if lower_limit <= count and count <= upper_limit:
            agreeing_users.append(row1[0])

    #print ">>> Users (" + str(len(agreeing_users)) + "): " + str(agreeing_users)

    for row in agreeing_users:
        with open("../data/output/a3-userids-extract-agreeing-users.csv", "a") as f:
            f.write(row + '\n')

    print "Done s3\n"


def s4():
    """
    Get all movie-rating tuples by high agreement users
    """
    # ratings_extract = open("a1-ratings-extract.csv", "r").readlines()
    ratings = open("../data/ml-ratings-lean.csv", "r").readlines()[1:]
    agreeing_users_extract = open("../data/output/a3-userids-extract-agreeing-users.csv", "r").readlines()
    input_data = open("../data/input/v1-input-ratings.csv", "r").readlines()
    input_data = input_data[1:]

    input_movie_and_ratings = []
    for ln in input_data:
        ln = ln.split(",")
        input_movie_and_ratings.append([ln[1], ln[2]])

    agreeing_users = []
    for ln in agreeing_users_extract:
        agreeing_users.append(ln.strip())
    #print ">>> # Users: " + str(len(agreeing_users))

    count = 0
    total = float(len(ratings))
    for ln in ratings:
        ln2 = ln.split(",")
        count += 1
        #p = count / total * 100.0
        #sys.stdout.write("\r>>> Ratings processsed: %d (%i%%)" % (count, p))
        #sys.stdout.flush()

        pair = [ln2[1], ln2[2]]

        if ln2[0] in agreeing_users and pair not in input_movie_and_ratings:
            with open("../data/output/a4-ratings-extract-recommended.csv", "a") as f:
                f.write(ln)

    print "\nDone s4\n"


def s5():
    """
    Sort movies column by distinct movies
    """
    data = []
    with open("../data/output/a4-ratings-extract-recommended.csv", "rb") as f:
        for row in csv.reader(f):
            data.append(row)
    data.sort(key=operator.itemgetter(1))  # Column to sort
    with open("../data/output/a5-ratings-extract-recommended-sorted.csv", "wb") as f:
        csv.writer(f).writerows(data)


    """
    After above sorting, get counts of # of movie-rating tuples for each movie
    """
    output = open("../data/output/a5-ratings-extract-recommended-sorted.csv", "r").readlines()
    count_dict = {}
    for n in range(0, len(output)):
        row1 = output[n].split(",")
        count1 = int(row1[1].strip())

        if count1 not in count_dict:
            count_dict[count1] = 0
        if count1 in count_dict:
            count_dict[count1] += 1
    OrderedDict(sorted(count_dict.items(), key=lambda t: t[0]))

    for i in count_dict:
        with open("../data/output/a5-ratings-extract-recommended-sorted-counts.csv", "a") as f:
            f.write(str(i) + ',' + str(count_dict[i]) + '\n')

    #print ">>> # Movie-Rating Tuples: " + str(len(count_dict))

    print "Done s5\n"


def s6(min_ratings=10):
    """
    Extract the movies with # ratings above a certain threshold
    """
    min_rated_movies = []
    with open("../data/output/a5-ratings-extract-recommended-sorted-counts.csv", "rb") as f:
        for row in csv.reader(f):
            if int(row[1]) >= min_ratings:
                min_rated_movies.append(row[0])

    #print ">>> Sample of Movies (5): " + str(min_rated_movies[:5])
    #print ">>> # of Agreeing Movies: " + str(len(min_rated_movies))

    """
    Extract the movie-rating tuples
    Average the ratings per movie
    """
    extracted_ratings = open("../data/output/a5-ratings-extract-recommended-sorted.csv", "r").readlines()

    count = 0
    temp_movie_ratings_sum = 0.0
    temp_movie_counts = 0
    temp_movie_avg = 0

    for n in range(0, len(extracted_ratings)):
        count += 1  # Progress Bar
        #sys.stdout.write("\r>>> Ratings processsed: %i" % count)
        #sys.stdout.flush()

        row1 = extracted_ratings[n].split(",")
        try:
            row2 = extracted_ratings[n + 1].split(",")
        except IndexError:  # exception thrown when file reaches end of line
            print "\n>>> End of Input"

        movie1 = row1[1]
        movie2 = row2[1]
        temp_rating_delta = float(row1[2])

        if movie1 in min_rated_movies and movie2 == movie1:  # If next row is same movie as current row
            temp_movie_ratings_sum += temp_rating_delta
            temp_movie_counts += 1

        if movie1 in min_rated_movies and movie2 != movie1:
            temp_movie_ratings_sum += temp_rating_delta
            temp_movie_counts += 1

            temp_movie_avg = temp_movie_ratings_sum / temp_movie_counts  # Avg upon movie switch
            with open("../data/output/a6-movies-extract-recommended.csv", "a") as f:
                f.write(str(movie1) + ',' + str(temp_movie_avg) + ',' + str(temp_movie_counts) + '\n')

            temp_movie_ratings_sum = 0
            temp_movie_counts = 0

    print "Done s6\n"


def s7(min_avg_rating=4.0):
    """
    Using raw recommendation data, get the movie titles and only return those above min_avg_rating
    """
    movies = open("../data/ml-movies.csv", "r").readlines()
    rec_data = open("../data/output/a6-movies-extract-recommended.csv", "r").readlines()

    with open("../data/output/a7-movies-extract-recommended-films.csv", "a") as f:
        f.write(','.join(['movieId', 'avgRating', 'agreeCount', 'title', 'genres', '\n']))

    count = 0
    for ln in rec_data:
        count += 1  # Progress Bar
        sys.stdout.write("\r>>> Ratings processsed: %i" % count)
        sys.stdout.flush()

        ln2 = ln.split(",")
        movie = ln2[0]
        avg_rating = float(ln2[1])
        rating_supp = ln2[2].strip()

        if avg_rating >= min_avg_rating:
            for row in movies:
                row = row.split(",", 1)
                if movie == row[0]:
                    movie_title_genre = row[1]
                    with open("../data/output/a7-movies-extract-recommended-films.csv", "a") as f:
                        f.write(ln.strip() + ',' + movie_title_genre)

    print "\nDone s7\n"


if __name__ == '__main__':
    s1("../data/input/v1-input-ratings.csv")
    s2()
    s3(7, 8)
    s4()
    s5()
    s6()
    s7()

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('data_input', help='')
    args = parser.parse_args()
    process_images(args.data_input)
    """

