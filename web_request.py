import requests

class DuolingoReadData():
    def __init__(self):
        self.header = {
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjo0MzIzMTk2MTl9.GwAO5PqmhXupIlZX67wDTXrWscKePLuJiI1pGqe695E'
        }
        self.data = '{"fromLanguage":"en","learningLanguage":"pt","challengeTypes":["translate"],"skillId":"6c1d9faaa8f142e3a28d844de8f78d08","levelIndex":0,"levelSessionIndex":1,"type":"LESSON","juicy":true}'


    def getData(self):
        response = requests.post('https://www.duolingo.com/2017-06-30/sessions', headers=self.header, data=self.data)
        
        return response.text