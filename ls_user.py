from duosession import DuoSession
from duorequest import DuoRequest
from duoprofile import DuoProfile
from duovoice import DuoVoice
from learnsession import DuolingoLearnSession
from helpers.dicthelper import DictHelper

# lingo = duo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com

__DEBUG__ = False


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class User():
    def __init__(self, userormail: str, password: str):
        if not password and not __DEBUG__:
            raise Exception("You must provide a password for this function")

        self.session: DuoSession = None
        self._user_data = None

        if password:
            self._login(userormail, password)

        self._refresh_user_data()

    def _login(self, userormail: str, password: str):
        """
        Creates a new session from duoSession
        Exception: Can throw exception if login wasn't successful
        """

        self.session = DuoSession(userormail, password)
        # set username here as the login could've been done with mail address
        self.username = self.session.username

    def _refresh_user_data(self):

        user_url = "https://duolingo.com/users/%s" % self.username
        response = DuoRequest.do_request(user_url, self.session)

        self._user_data = Struct(**response.json())

    def _switch_working_language(self, lang):
        """
        Change the learned language (the "working language") with
        ``https://www.duolingo.com/switch_language``.

        :param lang: Wanted language abbreviation (example: ``'fr'``)
        :type lang: str
        """
        data = {"learning_language": lang}
        url = "https://www.duolingo.com/switch_language"
        request = DuoRequest.do_request(url, self.session, data)

        try:
            parse = request.json()['tracking_properties']
            if parse['learning_language'] == lang:
                self._refresh_user_data()
        except:
            raise Exception('Failed to switch language')

    def _is_current_language(self, abbr):
        """Get if user is learning a language."""
        return abbr in self.get_full_user_info()["language_data"].keys()

    def get_working_language(self, abbr : bool):
        """Return the abbreviation of the current active language the user is studying"""
        if abbr:
            return self.get_full_user_info()["learning_language"]
        else:
            return self.get_full_user_info()["learning_language_string"]

    def get_settings(self):
        """Get user settings."""
        keys = ['notify_comment', 'deactivated',
                'is_follower_by', 'is_following']

        return DictHelper.make(keys, self._user_data)

    def get_available_languages(self, abbreviations=False):
        """
        Get praticed languages.

        :param abbreviations: Get language as abbreviation or not
        :type abbreviations: bool
        :return: List of languages
        :rtype: list of str
        """
        data = []

        for lang in self.get_full_user_info()["languages"]:
            if lang['learning']:
                if abbreviations:
                    data.append(lang['language'])
                else:
                    data.append(lang['language_string'])

        return data

    def get_full_user_info(self):
        """Get user's information"""
        fields = ['username', 'bio', 'id', 'num_following', 'cohort',
                  'language_data', 'languages', 'learning_language', 'learning_language_string', 'num_followers',
                  'created', 'contribution_points', 'gplus_id', 'twitter_id',
                  'admin', 'invites_left', 'location', 'fullname', 'avatar',
                  'ui_language']

        return DictHelper.make(fields, self._user_data)

    def get_profile_info(self):
        return DuoProfile(self._user_data, self.session)

    def get_voice_stuff(self):
        return DuoVoice(user.session, user.get_full_user_info()["language_data"])

    def get_current_learnsession(self, topic):
        # data = {"fromLanguage":self._user_data.ui_language,"learningLanguage":topic['language'],"challengeTypes":["translate"],"type":"LESSON", "levelIndex":topic["levels_finished"], "levelSessionIndex":topic["progress_level_session_index"],"juicy":True,}

        if topic['title'] in self.get_golden_topics(topic['language']):
            data = {"fromLanguage": self.get_full_user_info()["ui_language"], "learningLanguage": topic['language'], "challengeTypes": [
                'translate'], "type": "SKILL_PRACTICE", "skillId": topic['id']}
        else:
            data = {"fromLanguage": self.get_full_user_info()["ui_language"], "learningLanguage": topic['language'], "challengeTypes": ['translate'],
                    "type": "LESSON", "skillId": topic['id'], "levelIndex": topic['levels_finished'], "levelSessionIndex": topic['progress_level_session_index']
                    }

        if topic['language'] and not self._is_current_language(topic['language']):
            self._switch_working_language(topic['language'])

        return DuolingoLearnSession.fetch(self.session, data)

    def get_active_skills(self, language_abbr):
        """
        Return active skill object
        """
        skills = [skill for skill in
                  self.get_full_user_info()["language_data"][language_abbr]['skills']]

        return [skill for skill in skills
                if not skill['locked']]

    def get_skills_in_progress(self, language_abbr):
        """Return topics that have been started but are not mastered yet"""
        return [topic
                for topic in self.get_active_topics(language_abbr)
                if topic not in self.get_golden_topics(language_abbr)]

    def get_active_topics(self, language_abbr):
        """Return the topics that are active for a user in a language."""

        return [topic['title']
                for topic in self.get_full_user_info()["language_data"][language_abbr]['skills']
                if not topic['locked']]

    def get_golden_topics(self, language_abbr):
        """Return the topics mastered ("golden") by a user in a language."""
        return [topic['title']
                for topic in self.get_full_user_info()["language_data"][language_abbr]['skills']
                if topic['learned'] and topic['levels_finished'] == 5]


if __name__ == '__main__':
    from pprint import pprint
    """ Sample Login """
    user = User("DSA975012", "sprachassist")
    pprint(user.get_available_languages())
    pprint(user.get_working_language(False))
    pprint(user.get_settings())
    pprint(user.get_profile_info().get_friendlist_leaderbord("week"))
    pprint(user.get_profile_info().get_activity())
    pprint(user.get_profile_info().get_friends())
    #pprint(user.get_voice_stuff().get_audio_url("hello", "en"))
