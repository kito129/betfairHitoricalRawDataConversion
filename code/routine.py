import main
import os
import time



# the path were al files are extracte, you have to sperate file extracted by sport and by type of data
workPath = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/code/rawInput/'

# the path were i will place the file to be converted
data_ADVANCED_SOCCER = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/ADVANCED/SOCCER/'
data_ADVANCED_TENNIS = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/ADVANCED/TENNIS/'
data_ADVANCED_HORSE_RACING = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/ADVANCED/HORSE RACING/'

data_BASIC_SOCCER = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/BASIC/SOCCER/'
data_BASIC_TENNIS = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/BASIC/TENNIS/'
data_BASIC_HORSE_RACING = 'D:/00_PROJECTs/40_betfair/rawDataConversion/rawDataConversion/rawData/BASIC/HORSE RACING/'


# have to run for all above folder

# start the routine
main.main(data_ADVANCED_TENNIS,workPath,'ADVANCED')


print(' -----  END ADVANCED ----')

"""
# EMPTY FOLDER
for filename in os.listdir(mainPath):
    file_path = os.path.join(mainPath, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            mainPath.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


print(' -----  EMPTY ----')
time.sleep(3)
print('\n\n\n\n -----  START ADVANCED ----')
main.main(data_BASIC,mainPath,'BASIC')

# EMPTY FOLDER
for filename in os.listdir(mainPath):
    file_path = os.path.join(mainPath, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            mainPath.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


print(' -----  EMPTY ----')
time.sleep(3)



print(' -----  END ----')
"""