from java.lang import *
from java.sql import *

#these needs to be explicitly imported
from java.lang import Class
from java.sql import DriverManager

def connect(dburl="jdbc:mysql://localhost:3306/mtgo", dbuser="root", dbpass=None):
    try:
        try:
            Class.forName("com.mysql.jdbc.Driver").newInstance()
        except NameError:
            raise ErrorHandler("Internal MySQL error")
        conn = DriverManager.getConnection(dburl, dbuser, dbpass)
    except SQLException, error:
        raise ErrorHandler("MySQL error: %s" % str(error))

def get_product_info(product):
    """
    @product: string
    will call query with select statement
    @return: dict
    """
    pass
    
def set_product_info(product, product_info):
    """
    @product: string, @update_info: dict
    will call select query with to see if product exists,
    if yes, it will call query with update statement,
    otherwise it will use insert statement.
    @return: boolean
    """
    pass
    
def query(query):
    """
    Returns None if you haven't establed a connection yet.
    Use for select queries only, no inserts, updates, etc.
    """
    if not conn:
        return None
    data = {}
    stmnt = conn.createStatement()
    sql = query
    results = stmnt.executeQuery(sql)

    while results.next():
        data["quantity"] = results.getString("quantity")
    data[2] = results.getString(2)
    results.close()
    stmnt.close()

def close():
    conn.close()