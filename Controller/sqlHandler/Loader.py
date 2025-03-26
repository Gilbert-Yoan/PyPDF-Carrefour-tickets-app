class Loader():
    def __init__(self, master):
        self.Controller = master

    def sql_load_desc(self, existing, text=""):
        con,curs = self.Controller.session.start_session()
        params = False
        if not existing :
            load_missing_desc = "\
            SELECT * ,'NO_DESC', '0', '1' FROM product WHERE description IS NULL\
            "
            if text != "":
                load_missing_desc = load_missing_desc + "AND (description LIKE :text OR stock_id LIKE :text)"
                params = True
        else:
            load_missing_desc = "\
            SELECT *, '0', '1' FROM product\
            "
            if text != "":
                load_missing_desc = load_missing_desc + "WHERE description LIKE :text OR stock_id LIKE :text"
                params = True

        load_missing_desc = load_missing_desc + ';'
        if params:
            curs.execute(load_missing_desc, {"text":'%'+text+'%'})
        else:
            curs.execute(load_missing_desc)
        res = curs.fetchall()
        self.Controller.session.end_session(con)
        return list(map(list, res))


    def get_products(self):
        con,curs = self.Controller.session.start_session()
        query = "SELECT COUNT(*) FROM product;"
        curs.execute(query)

        #Tuple with 2 items
        nb_product = curs.fetchone()[0]
        self.Controller.session.end_session(con)
        #Supossing it could be None, return 0, even though it is not supposed to be
        if nb_product is None:
            return 0
        else:
            #Else only catch the integer value
            return nb_product

    def get_recent_price(self, id, close=1):
        con,curs = self.Controller.session.start_session()
        query = "SELECT total_price/quantity FROM shopping WHERE item_id = (?) ORDER BY date DESC LIMIT 1;"
        curs.execute(query, (id,))

        #Tuple with 2 items
        price = curs.fetchone()[0]
        if close == 1:
            self.Controller.session.end_session(con)
        return price

    def get_recent_date(self):
        con,curs = self.Controller.session.start_session()
        query = "select date from shopping order by date desc limit 1;"
        curs.execute(query)

        #Tuple with 2 items
        date = curs.fetchone()[0]
        print(date)
        return date
