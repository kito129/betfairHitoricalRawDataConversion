import pprint


class DBUploadStats:
    uploadStats = {
        'toAdd': {
            'data': [],
            'number': 0
        },
        'uploaded': {
            'data': [],
            'number': 0
        },
        'error': {
            'data': [],
            'number': 0
        },
    }

    # empty constructor
    def default(self, o):
        return o.__dict__

    def _to_add_append(self, data):
        self.uploadStats['toAdd']['number'] = self.uploadStats['toAdd']['number'] + 1
        self.uploadStats['toAdd']['data'].append(data)

    def _uploaded_append(self, data):
        self.uploadStats['uploaded']['number'] = self.uploadStats['uploaded']['number'] + 1
        self.uploadStats['uploaded']['data'].append(data)

    def _error_append(self, data):
        self.uploadStats['error']['number'] = self.uploadStats['error']['number'] + 1
        self.uploadStats['error']['data'].append(data)

    def _print_stats(self):
        print("\n---- Upload Stats ----\n")

        print("Docs to upload: " + str(self.uploadStats['toAdd']['number']))
        pprint.pprint("Docs: " + str(self.uploadStats['toAdd']['data']))
        print("\nOK: " + str(self.uploadStats['uploaded']['number']))
        pprint.pprint("Docs: " + str(self.uploadStats['uploaded']['data']))
        print("\nERROR: " + str(self.uploadStats['error']['number']))
        pprint.pprint("Docs: " + str(self.uploadStats['error']['data']))
        print('\nTOTAL:\n' + str(self.uploadStats['uploaded']['number']) + ' / ' + str(
            self.uploadStats['toAdd']['number']) + ' (' + str(self.uploadStats['error']['number']) + ')')

        print("\n---- ----\n")
