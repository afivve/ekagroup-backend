generate PK =  openssl genrsa -out private.pem 2048

sqlalchemy.url = mysql+pymysql://root:@localhost/ekagroup_test
target_metadata = Base.metadata