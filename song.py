from music_item import MusicItem, MUS_FORMATS
import mutagen
from mutagen.easyid3 import EasyID3
import json
import os


class Song(MusicItem):

    def add_song(self, tags, title, artist, album, genre, filename):
        # print("title", title)
        # print("artist", artist)
        # print("genre", genre)
        if filename.endswith(MUS_FORMATS):
            try:
                audio_file = EasyID3(filename)
            except mutagen.id3.ID3NoHeaderError:
                audio_file = mutagen.File(filename)  # , easy=True)
                audio_file.add_tags()#(ID3=EasyID3)

            try:
                audio_file['title'] = title
                audio_file['artist'] = artist
                audio_file['album'] = album
                audio_file['genre'] = genre
                audio_file.save(filename)
                # print(audio_file)
            except TypeError:
                pass
        # changed = EasyID3(filename)
        # for k, v in changed.items():
        #     print(f"{k}: {v}")
        return audio_file

    def add_song_to_json(self, audio_file):
        song_data = {k: v[0] for (k, v) in audio_file.items()}
        print(song_data)
        try:
            file = open("database.json")
            dictObj = json.load(file)
            dictObj.update(song_data)
            print(dictObj)
        except FileNotFoundError:
            dictObj = song_data

        with open("database.json", 'w') as json_file:
            json.dump(
                dictObj, json_file,
                indent=4,
                separators=(',', ': '))
  
# if path.isfile(filename) is False:
#   raise Exception("File not found")
 
# # Read JSON file
# with open(filename) as fp:
#   dictObj = json.load(fp)
 
# # Verify existing dict
# print(dictObj)

# print(type(dictObj))
 
# dictObj.update({"Age": 12,"Role": "Developer"})
 
# # Verify updated dict
# print(dictObj)
 
# with open(filename, 'w') as json_file:
    # json.dump(dictObj, json_file, 
    #                     indent=4,  
    #                     separators=(',',': '))