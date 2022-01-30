class Authorizer():
    def __init__(self, request): 
        self.token = request.headers.get('Authorization', None)

    def valid(self):
      if not self.token: return False
      if self.token == 'invalid': return False
      return True
