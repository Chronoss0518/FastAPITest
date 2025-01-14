from base.db_base import DBExtra


class PostgreSQL(DBExtra):
    
    def __init__(self,host:str,db_name:str,role_name:str,password:str):
        super().__init__(host,db_name,role_name,password)
        # super().__init__("localhost","testdb","chronoss","1925613Ex")
        
    
    def get_user_table_desc(self):
        return self.get_table_desk_data("TestTable")
    
    def get_user_table_where_id(self,user_id):
        user_data_list = self.__sql__(f'SELECT * FROM "TestTable" WHERE id = {user_id}')
        if user_data_list == None:
            return None
        return self._list_to_dict('TestTable',user_data_list)

    def get_user_table(self):
        user_data_list = self.__sql__('SELECT * FROM "TestTable"')
        if user_data_list == None:
            return None
        return self._list_to_dict('TestTable',user_data_list)
