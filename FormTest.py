import xlsxwriter
import os
from PIL import Image
import csv

# obtain folder names
root = os.path.abspath(os.path.dirname(__file__))
source_path = root + '\\frames' # 获取目录
target_path = root + '\\sheets'
cell_width = 160
folders = []
for root, dirs, names in os.walk(source_path):
    for dir in dirs:
        # print('processing ' + dir)
        if dir.strip() != '':
            folders.append(dir)
# print(folders)
folders = {}.fromkeys(folders).keys()
print('folders:',folders)
for dir in folders:
    print('processing ' + dir)
    # create folder
    try:
        workbook = xlsxwriter.Workbook(target_path+'\\'+dir+'.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column_pixels(0,0, cell_width)
        # worksheet.set_column('B:B', 15)
        worksheet.write(0, 0, 'First Frame')
        worksheet.write(0, 1, 'shot number')
        worksheet.write(0, 2, 'shot beginning time')
        worksheet.write(0, 3, 'shot scale(close-up, code 1; others code 0)')
        worksheet.write(0, 4, 'event ( 1,2,3…..)')
        worksheet.write(0, 5, 'roving camera( yes, code 1, no code 0)')

        print(dir)
        # open excel for beginning time & ending time
        # with open('./source/'+dir+'.mp4.csv', newline='') as csvfile:
        # print('opened ./source/'+dir+'.mp4.csv')
        # temp_reader = csv.reader(csvfile, delimiter=',')
        # data = list(temp_reader)

        dir_path = source_path+'\\'+dir
        row_num = 1
        # go over all screenshots
        for root_, dirs_, names_ in os.walk(dir_path):
            for name in names_:
                temp = name.split('.')[0].split('_')
                shot_num = temp[0]
                time_stamp = ':'.join(temp[1].split('-'))
                print('shot_num:', shot_num)
                print('screenshot:', name)
                print('time_stamp:', time_stamp)
                image = Image.open(dir_path+'\\'+name)
                width, height = image.size
                x_scale = cell_width/width
                print('height:',height)
                print('width:',width)
                worksheet.set_row_pixels(row_num, cell_width*(height/width))
                # y_scale = cell_height/height
                #insert image
                # print(row_cnt)
                worksheet.insert_image(row_num, 0, dir_path+'\\'+name, {'x_scale': x_scale, 'y_scale': x_scale, 'positioning': 1})
                worksheet.write(row_num, 1, shot_num)
                worksheet.write(row_num, 2, time_stamp)
                # worksheet.write(row_cnt, 2, data[row_cnt-1][0])
                # worksheet.write(row_cnt, 3, data[row_cnt-1][1])
                row_num += 1
            workbook.close()
    except Exception as e:
        print(f"Error: {e}")

input("\n>> Execution done, click any key to exit.")