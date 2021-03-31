class Config:
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1@localhost/academic_english?charset=utf8'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://snapper:m_SM3x3Z@localhost/adstetic_creative?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False