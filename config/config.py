import os

class Config:

  def __init__(self):
    self.env = 'development' if self.isDev(self.getEnvVar('ENV')) else self.getEnvVar('ENV')
    self.dbURI = 'localhost' if self.isDev(self.env) else self.getEnvVar('DB_URI')
    self.dbName = 'hcfa_app'
    self.dbUser = 'collinprice'
    self.dbPassword = 'password' if self.isDev(self.env) else self.getEnvVar('DB_PASSWORD')

  def getEnvVar(self, key):
    if key in os.environ:
      return os.environ[key]
    return None

  def isDev(self, var):
    return var != 'testing' and var != 'production'

  def isTesting(self):
    return self.env == 'testing'

  def isProd(self):
    return self.env == 'production'
