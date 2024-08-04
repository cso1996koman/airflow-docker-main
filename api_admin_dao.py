from airflow.providers.mysql.hooks.mysql import MySqlHook
from api_admin_dvo import ApiAdminDvo

class ApiAdminDao:
    def __init__(self, mysql_conn_id):
        self.mysql_hook = MySqlHook(mysql_conn_id=mysql_conn_id)
        self.connection = self.mysql_hook.get_conn()
        self.cursor = self.connection.cursor()
    def selectBySrcNm(self, src_nm) -> list:
        self.cursor.execute(f"SELECT * FROM api_admin_tb WHERE src_nm = '{src_nm}'")
        result = self.cursor.fetchall()
        api_admin_dvos : list = []
        for row in result:
            api_admin_dvo = ApiAdminDvo(
            src_nm=row[0],
            tb_nm=row[1],
            tb_code=row[2],
            version=row[3],
            uri=row[4],
            created_at=row[5],
            dir_path=row[6],
            column1=row[7]
            )
            api_admin_dvos.append(api_admin_dvo)
        return api_admin_dvos
    def close(self):
        self.cursor.close()
        self.connection.close()
        