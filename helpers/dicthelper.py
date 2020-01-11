class DictHelper():
    @staticmethod
    def make(keys, array):
        """
        Creates a dictionary with the given keys and the array values
        """
        data = {}

        for key in keys:
            if type(array) == dict:
                data[key] = array[key]
            else:
                data[key] = getattr(array, key, None)

        return data
