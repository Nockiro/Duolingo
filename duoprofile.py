from duorequest import DuoRequest

class DuoProfile():
    def __init__(self, user_data, session):
        self.user_data = user_data
        self.session = session

    def get_activity(self, language_abbr=None):
        """Get user's last actions in the currently selected language."""
        """Array of {datetime, event_type, improvement, skill_id} """
        return self.user_data.calendar

    def get_friendlist_leaderbord(self, unit=None):
        """
        Get user's rank in the week in descending order, stream from
        ``https://www.duolingo.com/friendships/leaderboard_activity?unit=week

        :param unit: maybe week or month
        :type unit: str
        :rtype: List
        """
        if unit:
            url = 'https://www.duolingo.com/friendships/leaderboard_activity?unit={}'
        else:
            raise Exception('Needs unit as argument (week or month)')

        leader_data = DuoRequest.do_request(url, self.session).json()
        data = []
        for result in self.get_friends():
            for value in leader_data['ranking']:
                if result['id'] == int(value):
                    temp = {'points': int(leader_data['ranking'][value]),
                            'unit': unit,
                            'id': result['id'],
                            'username': result['username']}
                    data.append(temp)

        return sorted(data, key=lambda user: user['points'], reverse=True)

    def get_friends(self):
        """Get user's friends."""
        for k, v in self.user_data.language_data.items():
            data = []
            for friend in v['points_ranking_data']:
                temp = {'username': friend['username'],
                        'id': friend['id'],
                        'points': friend['points_data']['total'],
                        'languages': [i['language_string'] for i in
                                      friend['points_data']['languages']]}
                data.append(temp)

            return data
