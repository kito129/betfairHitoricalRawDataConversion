# ##
#  --- IMPORT ---
# ##
import os
import bz2
import json


# loop on all folder in path and extract bz2 to JSON file
def extractJson(dataPath, extractPath):
    print("\nExtracting File...")
    countOK = 0
    for (dirpath, dirnames, files) in os.walk(dataPath):
        for fileName in files:
            # filter out decompressed files
            if fileName.endswith('.json'):
                continue

            # save file as .json
            filepath = os.path.join(dirpath, fileName)
            newFilepath = extractPath + fileName + '.json'
           

            # save JSON file
            with open(newFilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
                for data in iter(lambda: file.read(), b''):
                    new_file.write(data)
            file.close()
            countOK = countOK +1

    # print recap
    print("Files Extracted: " + str(countOK))
    print('\nEnd of extraction..\n')
