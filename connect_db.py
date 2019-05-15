import pymysql.cursors
import json, math

# import numpy as np

host = "127.0.0.1"
username = "root"
password = "123456"
database_name = "game_recommend"
table_name = "classified_data"


def drop_database():
    try:
        connection = pymysql.connect(host, username, password)
        with connection.cursor() as cs:
            query_drop_database = """drop database """ + database_name
            cs.execute(query_drop_database)
    finally:
        connection.close()


def create_database():
    try:
        connection = pymysql.connect(host, username, password)
        with connection.cursor() as cs:
            query_create_db = "create database if not exists " + database_name
            cs.execute(query_create_db)
    finally:
        connection.close()


def get_connect():
    try:
        connection = pymysql.connect(host, username, password, database_name)
        connection.autocommit(True)
        return connection
    except:
        print("connect fail")


def create_table_data():
    try:
        connection = get_connect()
        with connection.cursor() as cs:
            query_create_table = """
               create table if not exists classified_data(
                    id int primary key auto_increment,
                    url text not null,
                    name text not null,
                    price float,
                    platform text,
                    metascore float,
                    userscore float,
                    total int,
                    positive int
                );
            """
            cs.execute(query_create_table)

            query_2 = """ALTER TABLE `game_recommend`.`classified_data`
                CHANGE COLUMN `name` `name` TEXT CHARACTER SET 'utf8mb4' NOT NULL ;
            """
            cs.execute(query_2)
    finally:
        connection.close()


def select_all():
    try:
        connection = get_connect()
        with connection.cursor() as cs:
            query_select_all = """
                select * from classified_data
            """
            cs.execute(query_select_all)
            result = cs.fetchall()
            return result
    finally:
        connection.close()


def select_name():
    try:
        connection = get_connect()
        with connection.cursor() as cs:
            query_select_link = """
                select distinct `name` from game_recommend.classified_data
            """
            cs.execute(query_select_link)
            result = []
            
            for a in cs.fetchall():
                result.append(a[0])

            return result
    finally:
        connection.close()


def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)


def insert(classified_result_fn):
    try:
        connection = get_connect()
        with connection.cursor() as cs:
            with open(classified_result_fn, mode='r', encoding='utf8') as f:
                data = json.load(f)
                for x in data:
                    # print(x)
                    if '\'' in x['name']:
                        idx = [i for i in findall('\'', x['name'])]
                        for i in range(len(idx)):
                            x['name'] = x['name'][:idx[i]] + '\\' + x['name'][idx[i]:]
                            if i != len(idx) - 1:
                                idx[i + 1] += 1
                    query_insert = """
                        insert into game_recommend.classified_data(url, name, price, platform, metascore, userscore, total,  positive)
                        values
                            ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');                  
                    """.format(str(x['url']), str(x['name']), float(x['price']) / 2304000, x['platform'],
                               float(x['metascore']), float(x['userscore']), int(x['Total']), int(x['Positive']))
                    cs.execute(query_insert)
    finally:
        connection.close()


def turn_to_matrix(game_list, platform_list, price):
    try:
        connection = get_connect()
        with connection.cursor() as cs:
            placeholders1 = ','.join('%s' for i in game_list)
            placeholders2 = ','.join('%s' for i in platform_list)
            query = "select * from game_recommend.classified_data where `name` in ({}) and `platform` in ({}) and `price` <= {};".format(placeholders1, placeholders2, price)
            # print(query)
            cs.execute(query, game_list + platform_list)
            matrix = []
            id_list = []
            for row in cs:
                avg_score = (float(row[5]) / 10 + float(row[6])) / 2
                if float(row[7]) != 0:
                    pos = float(row[8]) / float(row[7])
                else:
                    pos = 0
                matrix.append([1 / math.exp(float(row[3])), avg_score, float(row[7]), pos])
                id_list.append(row[0])
            print(cs.rowcount)
            return (matrix, id_list)

    finally:
        connection.close()

def select_game(id_list):
    try:
        connection = get_connect()
        with connection.cursor() as cs:
            placeholders = ','.join('%s' for i in id_list)
            query = "select * from game_recommend.classified_data where `id` in ({});".format(placeholders)
            cs.execute(query, id_list)
            result = []

            for a in cs.fetchall():
                result.append(a)

            return result
    finally:
        connection.close()


# if __name__ == '__main__':
    # drop_database()
    # create_database()
    # create_table_data()
    # insert("/home/vudat1710/Downloads/game (1).json")
    # turn_to_matrix()
    # print("end")
    # select_all()
    # select_name()
