# for Lucia's project

import os
import cv2
import ffmpeg
import imutils # resize frame

from TransNetV2.inference.transnetv2 import TransNetV2

# @article{soucek2020transnetv2,
#     title={TransNet V2: An effective deep network architecture for fast shot transition detection},
#     author={Sou{\v{c}}ek, Tom{\'a}{\v{s}} and Loko{\v{c}}, Jakub},
#     year={2020},
#     journal={arXiv preprint arXiv:2008.04838},
# }

frame_path = './frames/' # position for screenshots
source_path = './source/' # position for mp4, notice update line 36 if you change this line
video_format = '.mkv'

# take screenshots using ffmpeg
def getFrameFFMPEG(vid_path, frm_num, frm_name):
    out, err = (
        ffmpeg.input(vid_path)
            .filter('select','gte(n,{})'.format(frm_num))
            .output(frm_name, vframes=1)
            .run()
    )
# take screenshots using cv2
def getFrameCV2(cap, frm_num, frm_name):
    print('getFrame - frm_num:', frm_num)
    print('getFrame - frm_name:', frm_name)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frm_num)
    success, frame = cap.read()
    frame = imutils.resize(frame, width=640)
    if(success):
        cv2.imwrite(frm_name, frame)
    else:
        print('frame'+str(frm_name)+'failed')

if __name__ == '__main__':
    # obtain source, should be the same as source path (change manually)
    path = os.path.abspath(os.path.dirname(__file__))+'\\source'
    for root, dirs, names in os.walk(path):
        for name in names:
            file_name = os.path.splitext(name)
            video_name = file_name[0]
            ext = file_name[1]  # get file type
            shot_num = 1
            if ext == video_format:
                # create folders of frames for this mp4 file
                os.makedirs(os.path.abspath(os.path.dirname(__file__))+'\\frames\\'+video_name)
                print('processing '+name)
                model = TransNetV2('./TransNetV2/inference/transnetv2-weights/')
                video_path = source_path+video_name+video_format
                cap = cv2.VideoCapture(video_path)
                frame_rate = cap.get(cv2.CAP_PROP_FPS)
                frame_amount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                clip_1 = frame_amount
                print('frame_rate:',frame_rate)
                # segmentation using transnetv2
                video_frames, single_frame_p, all_frame_p = \
                    model.predict_video(video_path)
                print('len(VideoFrames):', len(video_frames))
                print('len(VideoFrames):', len(video_frames))
                print('len(SingleFrameP):', len(single_frame_p))
                print('len(AllFrameP):', len(all_frame_p))
                print('-------- SINGLE --------')
                quarter = int(frame_amount/4)
                size = (int(cap.get(3)),int(cap.get(4)))
                print('size:',size)
                for i in range(0,len(single_frame_p)):
                    # condition of screenshot
                    if single_frame_p[i] > 0.5:
                        shot_num += 1
                        if i in range(quarter,quarter+int(60*frame_rate)) or \
                            i in range(2*quarter,2*quarter+int(60*frame_rate)) or\
                            i in range(3*quarter,3*quarter+int(60*frame_rate)):
                            print('time:', i)
                            frm = int(i%frame_rate)
                            sec = int((i//frame_rate)%60)
                            min = int(((i//frame_rate)//60)%60)
                            hr = int(((i//frame_rate)//60)//60)
                            # seems like transnet takes the last frame, to get the first of next
                            getFrameCV2(cap, i+1, frame_path+video_name+'/'+\
                                str(shot_num)+'_'+str(hr).zfill(2)+'-'+str(min).zfill(2)+'-'+str(sec).zfill(2)+'-'+str(frm).zfill(2)+'.jpg')

    input("\n>> Execution done, click any key to exit.")

