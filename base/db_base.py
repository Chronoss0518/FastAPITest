import psycopg2

class DBbase:
    
    def __connection__(self,localhost:str,dbname:str,user_name:str,password:str):
        connect = psycopg2.connect(f"host={localhost} dbname={dbname} user={user_name} password={password}")
        if connect != None:
            self._cursor_ =  connect.cursor()

    def __sql__(self,sqltext:str):
        if self._cursor_ == None:
            return None
        self._cursor_.execute(sqltext)
        query_result = self._cursor_.fetchall()
        print(query_result)
        return query_result
    
    def get_table_list(self):
        return self.__sql__(f"SELECT relname as TABLE_NAME FROM pg_stat_user_tables")

    def get_table_desc(self,table_name):
        return self.__sql__(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position")

    def get_user_list(self):
        return self.__sql__("SELECT * FROM pg_user")
    
    
class TableData:

    def __init__(self,db_base : DBbase,table_name:str):
        desc = db_base.get_table_desc(table_name)
        if desc == None:
            return
        self.__table_name__ = table_name
        self.__desc__ = list()
        for i in range(len(desc)):
            self.__desc__.append(desc[i][0])

    def get_table_name(self):
        return self.__table_name__

    def get_desc_list(self):
        return self.__desc__

class DBExtra(DBbase):

    def __init__(self,host:str,db_name:str,role_name:str,password:str):
        self.__connection__(host,db_name,role_name,password)
        table_list = super().get_table_list()
        if table_list == None:
            return
        table_list = list(table_list)
        self.__table_data_dictionary = dict()
        for i in range(len(table_list)):
            table_data = list(table_list[i])
            self.__table_data_dictionary[table_data[0]] = TableData(self,table_data[0])
        
    def _list_to_dict(self,table_name:str,data_list:tuple):
        if data_list == None:
            return None
        
        if not(table_name in self.__table_data_dictionary.keys()):
            return None
        
        table_data = self.__table_data_dictionary[table_name]
        column_list = table_data.get_desc_list()
        
        res = []
        
        for i in range(len(data_list)):
            if len(column_list) > len(data_list[i]):
                continue

            obj = {}
            for j in range(len(column_list)):
                obj[column_list[j]] = data_list[i][j]
            res.append(obj)

        return res

    def get_table_structure_data(self,table_name:str):
        
        if not(table_name in self.__table_data_dictionary.keys()):
            return None
        obj = self.__table_data_dictionary[table_name]
        return obj.get_desc_list()
    
    def get_table_list(self):
        return list(self.__table_data_dictionary.keys())