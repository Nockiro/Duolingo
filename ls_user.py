from duosession import DuoSession
from duorequest import DuoRequest
from duoprofile import DuoProfile
from learnsession import DuolingoLearnSession
from dicthelper import DictHelper

# lingo = duo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class User():
    def __init__(self, username, password):
        self.username: str = username
        self.password: str = password
        self.session: DuoSession = None
        self._user_data = None

        if password:
            self._login()

        self._refreshUserData()

    def _login(self):
        """
        Creates a new session from duoSession
        Exception: Can throw exception if login wasn't successful
        """

        self.session = DuoSession(self.username, self.password)

    def _refreshUserData(self):

        user_url = "https://duolingo.com/users/%s" % self.username
        self._user_data = Struct(
            **DuoRequest.doRequest(user_url, self.session).json())

    def _switchWorkingLanguage(self, lang):
        """
        Change the learned language (the "working language") with
        ``https://www.duolingo.com/switch_language``.

        :param lang: Wanted language abbreviation (example: ``'fr'``)
        :type lang: str
        """
        data = {"learning_language": lang}
        url = "https://www.duolingo.com/switch_language"
        request = DuoRequest.doRequest(url, self.session, data)

        try:
            parse = request.json()['tracking_properties']
            if parse['learning_language'] == lang:
                self._refreshUserData()
        except:
            raise Exception('Failed to switch language')

    def get_settings(self):
        """Get user settings."""
        keys = ['notify_comment', 'deactivated', 'is_follower_by', 'is_following']

        return DictHelper.make(keys, self._user_data)

    def getLanguage(self):
        return self.lingo._is_current_language

    def getAvailableLanguages(self, abbreviations=False):
        """
        Get praticed languages.

        :param abbreviations: Get language as abbreviation or not
        :type abbreviations: bool
        :return: List of languages
        :rtype: list of str
        """
        data = []

        for lang in self._user_data.languages:
            if lang['learning']:
                if abbreviations:
                    data.append(lang['language'])
                else:
                    data.append(lang['language_string'])

        return data

    def getFullUserInfo(self):
        """Get user's information"""
        fields = ['username', 'bio', 'id', 'num_following', 'cohort',
                  'language_data', 'num_followers', 'learning_language_string',
                  'created', 'contribution_points', 'gplus_id', 'twitter_id',
                  'admin', 'invites_left', 'location', 'fullname', 'avatar',
                  'ui_language']

        return DictHelper.make(fields, self._user_data)

    def getProfileInfo(self):
        return DuoProfile(self._user_data, self.session)

    def getCurrentLearnSession(self, topic=None):
        if not self.password and not __DEBUG__:
            raise Exception("You must provide a password for this function")

        #data = {"fromLanguage":self._user_data.ui_language,"learningLanguage":topic['language'],"challengeTypes":["translate"],"type":"LESSON", "levelIndex":topic["levels_finished"], "levelSessionIndex":topic["progress_level_session_index"],"juicy":True,}

        if topic['title'] in self.get_golden_topics(topic['language']):
            data = {"fromLanguage": self._user_data.ui_language, "learningLanguage": topic['language'], "challengeTypes": ['translate'], "type": "SKILL_PRACTICE", "skillId": topic['id']}
        else:
            data = {"fromLanguage": self._user_data.ui_language, "learningLanguage": topic['language'], "challengeTypes": ['translate'],
                    "type": "LESSON", "skillId": topic['id'], "levelIndex": topic['levels_finished'], "levelSessionIndex": topic['progress_level_session_index']
                    }

        """ Set Debug to false to get real server data """
        if not __DEBUG__:
            if topic['language'] and not self._is_current_language(topic['language']):
                self._switchWorkingLanguage(topic['language'])

            learnRequest = DuoRequest.doRequest(self.learn_session_data_url, self.session, data)
            print(learnRequest)
            learnSessionData = learnRequest.json()

        else:
            learnSessionData = __sampleData__

        return DuolingoLearnSession(learnSessionData)


if __name__ == '__main__':
    from pprint import pprint
    """ Sample Login """
    user = User("DSA975012", "sprachassist")
    pprint(user.getAvailableLanguages())
    pprint(user.get_settings())
    pprint(user.getProfileInfo().getFriendlistLeaderboard("week"))
    pprint(user.getProfileInfo().getActivity())
    pprint(user.getProfileInfo().get_friends())
