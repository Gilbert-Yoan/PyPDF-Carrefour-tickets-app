class Editer():

    def __init__(self, master):
        self.Controller = master

    def update_desc(self, id, val):
        con,curs = self.Controller.session.start_session()

        update_query = "UPDATE product SET description = (?) WHERE id = (?);"

        curs.execute(update_query, (val, id))

        self.Controller.session.end_session(con)
        return True
