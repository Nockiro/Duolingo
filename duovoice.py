import re
import json
import random
from duorequest import DuoRequest

class DuoVoice():

    def __init__(self, session, langData):
        self._langData = langData
        self._userSession = session
        self._tts_voices = None
        self._cloudfront_server_url = None
        self._homepage_text = None
        self.voice_url_dict = None


    def get_audio_url(self, word, language_abbr=None, rand=True, voice=None):
        # Check word is in vocab
        if word is None:
            raise Exception('A word must be specified to use this function')
        word = word.lower()
        # Get default language abbr
        if not language_abbr:
            language_abbr = list(self._langData.keys())[0]

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

    @property
    def _homepage(self):
        if self._homepage_text:
            return self._homepage_text
        homepage_url = "https://www.duolingo.com"
        
        request = DuoRequest.doRequest(homepage_url, self._userSession)
        self._homepage_text = request.text
        return self._homepage

    @property
    def _cloudfront_server(self):
        if self._cloudfront_server_url:
            return self._cloudfront_server_url

        server_list = re.search('//.+\.cloudfront\.net', self._homepage)
        self._cloudfront_server_url = "https:{}".format(server_list.group(0))

        return self._cloudfront_server_url

    def _populate_voice_url_dictionary(self, lang_abbr):
        if self.voice_url_dict is None:
            self.voice_url_dict = {}
        self.voice_url_dict[lang_abbr] = {}
        # Get skill IDs
        skill_ids = []
        for skill in self._langData[lang_abbr]['skills']:
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

            resp = DuoRequest.doRequest("https://www.duolingo.com/2017-06-30/sessions", self._userSession, req_data)
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
