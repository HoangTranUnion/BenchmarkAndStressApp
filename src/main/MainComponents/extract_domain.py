import random
import os


class InvalidArgument(Exception):
    pass


class ExtractDomain:
    '''
    This class is for extracting links from files supplied.
    These files are assumed, by default, to be .txt files that have data line by line.

    '''

    def __init__(self, filePath:str, shuffle = False, limit = None):
        '''
        Initiates the ExtractDomain class.
        :param filePath: The path to the desired file(s).
            This can either be a directory to a folder containing the files or a path to the exact file.
        :param shuffle: Whether the list of extracted links should be shuffled or not.
        :param limit: The maximum amount of links that the user wants.
        '''
        self.file_path = filePath
        if os.path.isfile(self.file_path):
            self._structure = "file"
        elif os.path.isdir(self.file_path):
            self._structure = "dir"
        else:
            raise InvalidArgument("The given string is not a path.")

        self.shuffle = shuffle
        if limit is not None:
            self.limit = int(limit)
        else:
            self.limit = limit
        self.data = self._extract()

    @classmethod
    def get_all_data(cls, file_loc):
        return ExtractDomain(file_loc).data

    def _extract(self):
        if self._structure == 'file':
            with open(self.file_path,'r') as f:
                data = [line.rstrip("\n") for line in f.readlines()]
        else:
            all_files = os.listdir(self.file_path)
            data = []
            if len(all_files) != 0:
                for file in all_files:
                    if file[file.rfind(".") + 1:] == 'txt':
                        with open(os.path.join(self.file_path, file), 'r') as f:
                            data.extend([line.rstrip("\n") for line in f.readlines()])

        if self.shuffle:
            random.shuffle(data)
        if self.limit is not None:
            data = data[:self.limit]
        return data
