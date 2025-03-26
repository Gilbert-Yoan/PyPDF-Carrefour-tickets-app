
class Initializer():

    def __init__(self, master):
        self.Controller = master

    def sql_init(self):
        con,curs = self.Controller.session.start_session()

        create_category_table = "\
        CREATE TABLE IF NOT EXISTS category (\
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            name TEXT,\
            tax REAL \
            );\
        "

        create_product_table = "\
        CREATE TABLE IF NOT EXISTS product (\
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            stock_id TEXT UNIQUE, \
            description TEXT,\
            cat_id INTEGER REFERENCES category(id)\
            );\
        "

        create_shopping_table = "\
        CREATE TABLE IF NOT EXISTS shopping( \
            date DATE, \
            item_id INTEGER REFERENCES product(id), \
            total_price REAL, \
            quantity INTEGER, \
            PRIMARY KEY (date,item_id) \
            );"

        init_category_table = " \
         INSERT OR REPLACE INTO category(name,tax) \
         VALUES ('Alimentaire',5.5), ('Restauration rapide',10), ('Divers',20); \
        "

        curs.execute(create_category_table)
        curs.execute(create_product_table)
        curs.execute(create_shopping_table)
        curs.execute(init_category_table)

        self.Controller.session.end_session(con)


    def truncate_all(self):
        con,curs = self.Controller.session.start_session()

        trunc_category_table = "DROP TABLE category;"

        trunc_product_table = "DROP TABLE product;"

        trunc_shopping_table = "DROP TABLE shopping;"

        curs.execute(trunc_shopping_table)
        curs.execute(trunc_category_table)
        curs.execute(trunc_product_table)
        self.Controller.session.end_session(con)
        self.sql_init()
