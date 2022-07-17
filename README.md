# ShotSegExcel
shot segmentation, screenshot, and excel generation

*The code uses @TransNetV2 for shot segmentation (https://github.com/soCzech/TransNetV2).

1. preparation:
 - clone transnetv2 and install dependencies
 - python should remind you what are needed
 - place videos in the 'source' folder：
 - adjust the variable 'video_format' in the SegTest.py file based on your videos format. 
2. run: python SegTest.py
 - this will capture the first frames of the shots that belongs to the 1 minute clips start from 1st, 2nd, and 3rd quarter of each video and saves them in the 'frames' folder in the format '<shot number>_<shot time>'
3. run: python FormTest.py
 - this will generate excels using the frames saved in 'source' folder for coding. The excels will be saved in the 'sheets' folder.
