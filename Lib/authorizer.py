class Authorizer():
    def __init__(self, request): 
        self.token = request.headers['Authorization']

    def valid(self):
      if not self.token: return False
      if self.token == 'invalid': return False
      return True
