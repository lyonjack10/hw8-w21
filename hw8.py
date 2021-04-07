import unittest
import sqlite3
import json
import os

#
# Name:
# Who did you work with:
#

def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCategoriesTable(data, cur, conn):
    category_list = []
    for business in data['businesses']:
        business_categories = business['categories']
        for category in business_categories:
            if category['title'] not in category_list:
                category_list.append(category['title'])

    cur.execute("DROP TABLE IF EXISTS Categories")
    cur.execute("CREATE TABLE Categories (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(category_list)):
        cur.execute("INSERT INTO Categories (id,title) VALUES (?,?)",(i,category_list[i]))
    conn.commit()



def setUpRestaurantTable(data, cur, conn):
    ## [TASK 1]: 25 points
    # Finish the function setUpRestaurantTable
    # Iterate through the JSON data to get a list of restaurants
    # Load all of the restaurants into a database table called Restaurants, with the following columns in each row:
    # restaurant_id (datatype: text; primary key)
    # name (datatype: text)
    # address (datatype: text)
    # zip (datatype: text)
    # category_id (datatype: integer)
    # rating (datatype: real)
    # price (datatype: text)
    pass



def getRestaurantsByPrice(price, cur, conn):
    ## [TASK 2]: 10 points
    # The function takes 3 arguments as input: a price,
    # the database cursor, and database connection object. It selects all
    # the restaurants of a particular price and returns a list of tuples.
    # Each tuple contains the restaurant name and address.
    pass



def getRestaurantsByZipcodeBelowRatingAndByPrice(zip_code, rating, price, cur, conn):
    ## [TASK 3]: 10 points
    # The function takes 5 arguments as input: the zip_code,
    # the rating, the price, the database cursor, and database connection object.
    # It selects all the restaurants with a certain zip code, rating less than or 
    # equal to the rating passed to the function, with a particular price, and returns 
    # a list of tuples. Each tuple in the list contains the restaurant name, 
    # address, rating, and price.
    pass




def getRestaurantsAboveRatingOfCategory(rating, category, cur, conn):
    ## [TASK 4]: 10 points
    # The function takes 4 arguments as input: a rating, a category, the database cursor,
    # and database connection object.  It returns a list of tuples for all of the 
    # restaurant names that match that category and have a rating greater than or equal 
    # to the rating passed to the function. Each tuple in the list should contain the 
    # restaurant name, address and rating.
    #Note: You have to use JOIN  for this task.
    pass


def getRestaurantsOfType(price, rating, category, cur, conn):
    # [EXTRA CREDIT]
    # This function takes in 5 parameters: price, rating, category,
    # the database cursor, and database connection object. It returns
    # a list of all of the restaurant names that match the price, are
    # greater than or equal to that rating, and match that category.
    pass



class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'restaurants.db')
        self.cur = self.conn.cursor()
        self.data = readDataFromFile('yelp_data.txt')

    def test_businesses_table(self):
        self.cur.execute('SELECT * from Restaurants')
        resturant_list = self.cur.fetchall()
        self.assertEqual(len(resturant_list), 50)
        self.assertEqual(len(resturant_list[0]),7)
        self.assertIs(type(resturant_list[0][0]), str)
        self.assertIs(type(resturant_list[0][1]), str)
        self.assertIs(type(resturant_list[0][2]), str)
        self.assertIs(type(resturant_list[0][3]), str)
        self.assertIs(type(resturant_list[0][4]), int)
        self.assertIs(type(resturant_list[0][5]), float)
        self.assertIs(type(resturant_list[0][6]), str)

    def test_restaurants_by_price(self):
        x = sorted(getRestaurantsByPrice('$$$$', self.cur, self.conn))
        self.assertEqual(len(x),3)
        self.assertEqual(x[0][0],"Aamani's Smokehouse & Pizza")

        y = sorted(getRestaurantsByPrice('$$', self.cur, self.conn))
        self.assertEqual(y[0][0],"Anthony's Gourmet Pizza")
        self.assertEqual(len(getRestaurantsByPrice('$$', self.cur, self.conn)),29)

    def test_restaurants_by_zipcode_below_rating_by_price(self):

        z = getRestaurantsByZipcodeBelowRatingAndByPrice('48104', 4.0, '$', self.cur, self.conn)
        self.assertEqual(len(z),6)
        self.assertEqual(z[0][1],"808 S State St, Ann Arbor")

        self.assertEqual(len(getRestaurantsByZipcodeBelowRatingAndByPrice('48104', 2.0, '$$', self.cur, self.conn)),0)

        a = sorted(getRestaurantsByZipcodeBelowRatingAndByPrice('48104', 5.0, '$$$', self.cur, self.conn))
        self.assertEqual(len(a),2)
        self.assertEqual(a[0][0], "Gratzi")
        self.assertEqual(len(getRestaurantsByZipcodeBelowRatingAndByPrice('48104', 4.5, '$', self.cur, self.conn)[0]),4)

    def test_restaurants_above_rating_of_category(self):
        b = sorted(getRestaurantsAboveRatingOfCategory(4.0, "Salad", self.cur, self.conn))
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0][0], "NeoPapalis")

        c = sorted(getRestaurantsAboveRatingOfCategory(3.0, "Bakeries", self.cur, self.conn))
        self.assertEqual(len(c), 2)
        self.assertEqual(c[1][1], "3711 Plaza Dr, Ann Arbor")

        d = sorted(getRestaurantsAboveRatingOfCategory(4.5, "Pizza", self.cur, self.conn))
        self.assertEqual(len(d), 4)
        self.assertEqual(d[2][0], "Little Caesars Pizza")


    def test_restaurants_of_type_extra_credit(self):
        e = sorted(getRestaurantsOfType("$$", 4.0, "Pizza", self.cur, self.conn))
        self.assertEqual(len(e), 3)
        self.assertEqual(e[2][0], 'Red Rooster Pizzeria')

        f = getRestaurantsOfType("$$$$", 3.5, "Chicken Wings", self.cur, self.conn)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0][0], 'Wings N Things')


def main():
    json_data = readDataFromFile('yelp_data.txt')
    cur, conn = setUpDatabase('restaurants.db')
    setUpCategoriesTable(json_data, cur, conn)
    setUpRestaurantTable(json_data, cur, conn)

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)