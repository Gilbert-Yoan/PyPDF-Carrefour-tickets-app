from datetime import datetime


class Inserter():

    def __init__(self, master):
        self.Controller = master

    def get_category_id(self, curs, tax):
        #Get Category ID of current item
        query = "SELECT id FROM category WHERE tax=(?)"
        curs.execute(query, (tax,))

        #Tuple with 2 items
        category_id = curs.fetchone()
        #If the category cannot be found then error release
        if category_id is None:
            return False
        else:
            #Else only catch the integer value
            return category_id[0]

    def get_item_id(self, curs, stock_id):
        #Get Item ID of the current item
        query = "SELECT id FROM product WHERE stock_id = (?)"
        curs.execute(query, (stock_id,))

        #Tuple with 2 items
        item_id = curs.fetchone()
        #If the category cannot be found then we need to create it
        if item_id is None:
            return 0
        else:
            return item_id[0]

    def get_is_already_bought(self, curs, date, item_id):
        query_check_bought = "SELECT COUNT(*) as nb FROM shopping \
        WHERE date=(?) AND item_id =(?)"
        curs.execute(query_check_bought, (date, item_id))

        return curs.fetchone()[0] > 0

    def insert_db(self, date, list):
        con,curs = self.Controller.session.start_session()

        #For every object we will check:
        #--Its category
        #--If it already exists or not
        #--Else we will insert it
        #--If it was bought the same day, if so change the shopping qty and total price
        #--Else we will insert it
        for obj in list:

            category_id = self.get_category_id(curs, obj[0])
            #if category_id is 0, raise error
            if not category_id :
                return 0

            item_id = self.get_item_id(curs, obj[1])
            if item_id == 0 :
                #Add the product if it's unknown
                query_product_insert = "INSERT INTO product(stock_id, cat_id) VALUES ((?),(?))"
                curs.execute(query_product_insert, (obj[1], category_id))
                #Update item_id
                item_id = self.get_item_id(curs, obj[1])

            #Add the shopping values
            #First, we need to verify that there isn't a product already
            #If there is, price should be multiplied and quantity increased
            check_already_bought = self.get_is_already_bought(curs, date, item_id)

            #Update shopping table if needed

            if check_already_bought:
                update_shopping = "UPDATE shopping \
                SET quantity = quantity + (?), \
                total_price = total_price * (quantity + (?)) \
                WHERE date=(?) AND item_id = (?);"
                curs.execute(update_shopping, (obj[2],obj[2],date,item_id))
            else:
                query_shopping_insert = "INSERT INTO shopping VALUES ((?),(?),(?),(?))"
                curs.execute(query_shopping_insert, (date, item_id, obj[3], obj[2]))

        self.Controller.session.end_session(con)
        return 1

    def insert_prediction(self, data):
        conn,curs = self.Controller.session.start_session()
        date = datetime.today().strftime('%Y-%m-%d')
        for x in data :
            if x[4] == '1':
                #Here we query database for the most recent price of the item
                price = self.Controller.loader.get_recent_price(x[0], close=0) * float(x[5])
                query_shopping_insert = "INSERT INTO shopping VALUES ((?),(?),(?),(?),1)"
                curs.execute(query_shopping_insert, (date, x[0], price, x[5]))
                conn.commit()

        self.Controller.session.end_session(conn)
        return 1
