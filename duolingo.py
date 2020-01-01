"""Unofficial API for duolingo.com"""
import re
import json
import random
import datetime
import time

import requests
from requests import Session

__DEBUG__ = False

with open('sampleLearnSession.json', 'r') as f:
    __sampleData__ = json.load(f)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class AlreadyHaveStoreItemException(Exception):
    pass


class Duolingo(object):
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.user_url = "https://duolingo.com/users/%s" % self.username
        self.session = requests.Session()
        self.session.verify = False

    def buy_item(self, item_name, abbr):
        url = 'https://www.duolingo.com/2017-06-30/users/{}/shop-items'
        url = url.format(self.user_data.id)

        data = {'itemName': item_name, 'learningLanguage': abbr}
        request = self._make_req("POST", url, data)

        """
        status code '200' indicates that the item was purchased
        returns a text like: {"streak_freeze":"2017-01-10 02:39:59.594327"}
        """

        if request.status_code == 400 and request.json()['error'] == 'ALREADY_HAVE_STORE_ITEM':
            raise AlreadyHaveStoreItemException(
                'Already equipped with ' + item_name + '.')
        if not request.ok:
            # any other error:
            raise Exception('Not possible to buy item.')

    def buy_streak_freeze(self):
        """
        figure out the users current learning language
        use this one as parameter for the shop
        """
        lang = self.get_abbreviation_of(
            self.get_user_info()['learning_language_string'])
        if lang is None:
            raise Exception('No learning language found')
        try:
            self.buy_item('streak_freeze', lang)
            return True
        except AlreadyHaveStoreItemException:
            return False

    def get_language_from_abbr(self, abbr):
        """Get language full name from abbreviation."""
        for language in self.user_data.languages:
            if language['language'] == abbr:
                return language['language_string']
        return None

    def get_abbreviation_of(self, name):
        """Get abbreviation of a language."""
        for language in self.user_data.languages:
            if language['language_string'] == name:
                return language['language']
        return None

    def get_language_details(self, language):
        """Get user's status about a language."""
        for lang in self.user_data.languages:
            if language == lang['language_string']:
                return lang

        return {}

    def get_streak_info(self):
        """Get user's streak informations."""
        fields = ['daily_goal', 'site_streak', 'streak_extended_today']
        return self._make_dict(fields, self.user_data)

    def _is_current_language(self, abbr):
        """Get if user is learning a language."""
        return abbr in self.user_data.language_data.keys()

    def get_language_progress(self, lang):
        """Get informations about user's progression in a language."""
        if not self._is_current_language(lang):
            self._switch_language(lang)

        fields = ['streak', 'language_string', 'level_progress',
                  'num_skills_learned', 'level_percent', 'level_points',
                  'points_rank', 'next_level', 'level_left', 'language',
                  'points', 'fluency_score', 'level']

        return self._make_dict(fields, self.user_data.language_data[lang])

    def get_known_words(self, lang):
        """Get a list of all words learned by user in a language."""
        words = []
        for topic in self.user_data.language_data[lang]['skills']:
            if topic['learned']:
                words += topic['words']
        return set(words)

    def get_learned_skills(self, lang):
        """
        Return the learned skill objects sorted by the order they were learned
        in.
        """
        skills = [skill for skill in
                  self.user_data.language_data[lang]['skills']]

        return [skill for skill in skills
                if skill['learned']]

    def get_known_topics(self, lang):
        """Return the topics learned by a user in a language."""
        return [topic['title']
                for topic in self.user_data.language_data[lang]['skills']
                if topic['learned']]

    def get_unknown_topics(self, lang):
        """Return the topics remaining to learn by a user in a language."""
        return [topic['title']
                for topic in self.user_data.language_data[lang]['skills']
                if not topic['learned']]

    def get_golden_topics(self, lang):
        """Return the topics mastered ("golden") by a user in a language."""
        return [topic['title']
                for topic in self.user_data.language_data[lang]['skills']
                if topic['learned'] and topic['levels_finished'] == 5]

    def get_reviewable_topics(self, lang):
        """Return the topics learned but not golden by a user in a language."""
        return [topic['title']
                for topic in self.user_data.language_data[lang]['skills']
                if topic['learned'] and topic['strength'] < 1.0]

    def get_translations(self, words, source=None, target=None):
        """
        Get words' translations from
        ``https://d2.duolingo.com/api/1/dictionary/hints/<source>/<target>?tokens=``<words>``

        :param words: A single word or a list
        :type: str or list of str
        :param source: Source language as abbreviation
        :type source: str
        :param target: Destination language as abbreviation
        :type target: str
        :return: Dict with words as keys and translations as values
        """
        if not source:
            source = self.user_data.ui_language
        if not target:
            target = list(self.user_data.language_data.keys())[0]

        word_parameter = json.dumps(words, separators=(',', ':'))
        url = "https://d2.duolingo.com/api/1/dictionary/hints/{}/{}?tokens={}" \
            .format(target, source, word_parameter)

        request = self.session.get(url)
        try:
            return request.json()
        except:
            raise Exception('Could not get translations')

    def get_vocabulary(self, language_abbr=None):
        """Get overview of user's vocabulary in a language."""
        if not self.password:
            raise Exception("You must provide a password for this function")
        if language_abbr and not self._is_current_language(language_abbr):
            self._switch_language(language_abbr)

        overview_url = "https://www.duolingo.com/vocabulary/overview"
        overview_request = self._make_req("GET", overview_url)
        overview = overview_request.json()

        return overview

    _cloudfront_server_url = None
    _homepage_text = None

    @property
    def _homepage(self):
        if self._homepage_text:
            return self._homepage_text
        homepage_url = "https://www.duolingo.com"
        request = self._make_req("GET", homepage_url)
        self._homepage_text = request.text
        return self._homepage

    @property
    def _cloudfront_server(self):
        if self._cloudfront_server_url:
            return self._cloudfront_server_url

        server_list = re.search('//.+\.cloudfront\.net', self._homepage)
        self._cloudfront_server_url = "https:{}".format(server_list.group(0))

        return self._cloudfront_server_url

    _tts_voices = None

    def _process_tts_voices(self):
        voices_js = re.search('duo\.tts_multi_voices = {.+};',
                              self._homepage).group(0)

        voices = voices_js[voices_js.find("{"):voices_js.find("}") + 1]
        self._tts_voices = json.loads(voices)

    def get_language_voices(self, language_abbr=None):
        if not language_abbr:
            language_abbr = list(self.user_data.language_data.keys())[0]
        voices = []
        if not self._tts_voices:
            self._process_tts_voices()
        for voice in self._tts_voices[language_abbr]:
            if voice == language_abbr:
                voices.append('default')
            else:
                voices.append(voice.replace('{}/'.format(language_abbr), ''))
        return voices

    def get_audio_url(self, word, language_abbr=None, rand=True, voice=None):
        # Check word is in vocab
        if word is None:
            raise DuolingoException(
                'A word must be specified to use this function')
        word = word.lower()
        # Get default language abbr
        if not language_abbr:
            language_abbr = list(self.user_data.language_data.keys())[0]
        tts_voice = self._get_voice(language_abbr, rand=random, voice=voice)
        return "{}/tts/{}/token/{}".format(self._cloudfront_server, tts_voice,
                                           word)	        # Populate voice url dict
        if self.voice_url_dict is None or language_abbr not in self.voice_url_dict:
            self._populate_voice_url_dictionary(language_abbr)
        # If no audio exists for a word, return None
        if word not in self.voice_url_dict[language_abbr]:
            return None
        # Get word audio links
        word_links = list(self.voice_url_dict[language_abbr][word])
        # If a voice is specified, get that one or None
        if voice:
            for word_link in word_links:
                if "/{}/".format(voice) in word_link:
                    return word_link
            return None
        # If random, shuffle
        if rand:
            return random.choice(word_links)
        return word_links[0]

    def _populate_voice_url_dictionary(self, lang_abbr):
        if self.voice_url_dict is None:
            self.voice_url_dict = {}
        self.voice_url_dict[lang_abbr] = {}
        # Get skill IDs
        skill_ids = []
        for skill in self.user_data.language_data[lang_abbr]['skills']:
            skill_ids.append(skill['id'])
        # Scrape all sessions and create voice url dictionary
        for skill_id in skill_ids:
            req_data = {
                "fromLanguage": "en" if lang_abbr != "en" else "de",
                "learningLanguage": lang_abbr,
                "challengeTypes": ["definition", "translate"],
                "skillId": skill_id,
                "type": "SKILL_PRACTICE",
                "juicy": True,
                "smartTipsVersion": 2
            }
            resp = self._make_req(
                "https://www.duolingo.com/2017-06-30/sessions", req_data)
            if resp.status_code != 200:
                continue
            resp_data = resp.json()
            for challenge in resp_data['challenges']:
                self._add_to_voice_url_dict(
                    lang_abbr, challenge['prompt'], challenge['tts'])
                if challenge.get("metadata") and challenge['metadata'].get("non_character_tts"):
                    for word, url in challenge['metadata']['non_character_tts']['tokens'].items():
                        self._add_to_voice_url_dict(lang_abbr, word, url)
                for token in challenge['tokens']:
                    if token.get("tts") and token.get("value"):
                        self._add_to_voice_url_dict(
                            lang_abbr, token['value'], token['tts'])

    def _add_to_voice_url_dict(self, lang_abbr, word, url):
        word = word.lower()
        if word not in self.voice_url_dict[lang_abbr]:
            self.voice_url_dict[lang_abbr][word] = set()
        self.voice_url_dict[lang_abbr][word].add(url)

    def get_related_words(self, word, language_abbr=None):
        if not self.password:
            raise Exception("You must provide a password for this function")
        if language_abbr and not self._is_current_language(language_abbr):
            self._switch_language(language_abbr)

        overview_url = "https://www.duolingo.com/vocabulary/overview"
        overview_request = self._make_req("GET", overview_url)
        overview = overview_request.json()

        for word_data in overview['vocab_overview']:
            if word_data['normalized_string'] == word:
                related_lexemes = word_data['related_lexemes']
                return [w for w in overview['vocab_overview']
                        if w['lexeme_id'] in related_lexemes]

    def get_user_input(self, sentence=None):
        user_input = input(sentence)
        return user_input

    def get_active_topics(self, language_abbr=None):
        """Return the topics that are active for a user in a language."""

        return [topic['title']
                for topic in self.user_data.language_data[language_abbr]['skills']
                if not topic['locked']]

    def get_active_skills(self, language_abbr=None):
        """Return active skill object  """
        skills = [skill for skill in
                  self.user_data.language_data[language_abbr]['skills']]

        return [skill for skill in skills
                if not skill['locked']]

    def get_skills_in_progress(self, language_abbr=None):
        """Return topics that have been started but are not mastered yet"""
        return [topic
                for topic in self.get_active_topics(language_abbr)
                if topic not in self.get_golden_topics(language_abbr)]

    def get_current_language_abbr(self):
        """Return the abbreviation of the current active language the user is studying"""
        return self.get_abbreviation_of(self.get_user_info()['learning_language_string'])

if __name__ == '__main__':
    pass
