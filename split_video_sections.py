#%%
import os , shutil, time, sys
from pathlib import Path
# print(os.getcwd())
# input_path = ''
# top_left_path = ''
# top_right_path = ''
# bottom_left_path = ''
# bottom_right_path = ''

class HighRes:

    input_path = ''
    top_left_path = ''
    top_right_path = ''
    bottom_left_path = ''
    bottom_right_path = ''

    def __init__(self, file_name, interpolation):
        self.file_name = file_name
        self.interpolation = int(interpolation)

        if self.interpolation % 2 != 0:
            # print('Use the power of two for interpolation')
            sys.exit('Error!: Use the power of two for interpolation')


    def create_dir(self):
        root_dir = os.getcwd()
        input_dir = 'input'
        file_dir = self.file_name
        top_left_dir = 'top-left'
        top_right_dir = 'top-right'
        bottom_left_dir = 'bottom-left'
        bottom_right_dir = 'bottom-right'
        
        self.input_path = os.path.join(root_dir, input_dir)
        self.file_path = os.path.join(self.input_path, file_dir)
        filename_path_no_extensions = os.path.splitext(self.file_path)

        self.top_left_path = os.path.join(filename_path_no_extensions[0], top_left_dir)
        self.top_right_path = os.path.join(filename_path_no_extensions[0], top_right_dir)
        self.bottom_left_path = os.path.join(filename_path_no_extensions[0], bottom_left_dir)
        self.bottom_right_path = os.path.join(filename_path_no_extensions[0], bottom_right_dir)

        # print(filename_path_no_extensions[0])
        os.mkdir(filename_path_no_extensions[0])
        os.mkdir(self.top_left_path)
        os.mkdir(self.top_right_path)
        os.mkdir(self.bottom_left_path)
        os.mkdir(self.bottom_right_path)

    def remove_dup_frames(self):
        filename = self.file_name
        os.system('ffmpeg -i ' + self.input_path + '/' + filename + ' -vsync 0 -frame_pts true -vf mpdecimate ' + self.input_path + '/' + filename + '-decimated.mp4')
        print('ffmpeg -i ' + self.input_path + '/' + filename + ' -vsync 0 -frame_pts true -vf mpdecimate' + self.input_path + '/' + filename + '-decimate.mp4')
    
    def run_splitter(self):
        filename = self.file_name
        # file_name = 'berlin.mp4'
        # remove duplicate frames top left
        os.system('ffmpeg -i ' + self.input_path +'/'+ str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:0" ' + self.top_left_path +'/'+ str(filename)+ '-decimated-top-left.mp4')

        # remove top right
        os.system('ffmpeg -i ' + self.input_path + '/' + str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:0" ' + self.top_right_path +'/'+ str(filename)+ '-decimated-top-right.mp4')

        # remove bottom left
        os.system('ffmpeg -i ' + self.input_path + '/' + str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + self.bottom_left_path +'/'+ str(filename)+ '-decimated-bottom-left.mp4')

        # remove bottom right
        os.system('ffmpeg -i ' + self.input_path + '/' + str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + self.bottom_right_path +'/'+ str(filename)+ '-decimated-bottom-right.mp4')
    
    def run_feature_flow(self):
        interpolation_num = self.interpolation
        filename = self.file_name
        output_filename_dir = os.path.splitext(os.getcwd() +'/output/' + filename)[0]
        os.makedirs(output_filename_dir)
        # TOP LEFT
        print('INTERP TOP LEFT')
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + self.top_left_path + '/' + str(filename) + '-decimated-top-left.mp4 --t_interp ' + str(interpolation_num))
        shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        time.sleep(5)
        os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'top-left.mp4')
        
        # TOP RIGHT
        print('INTERP TOP RIGHT')
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + self.top_right_path + '/' + str(filename) + '-decimated-top-right.mp4 --t_interp ' + str(interpolation_num))
        shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        time.sleep(5)
        os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'top-right.mp4')
        
        # BOTTOM LEFT
        print('INTERP BOTTOM LEFT')
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + self.bottom_left_path + '/' + str(filename) + '-decimated-bottom-left.mp4 --t_interp ' + str(interpolation_num))
        shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        time.sleep(5)
        os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'bottom-left.mp4')
        
        # BOTTOM RIGHT
        print('INTERP BOTTOM RIGHT')
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + self.bottom_right_path + '/' + str(filename) + '-decimated-bottom-right.mp4 --t_interp ' + str(interpolation_num))
        shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        time.sleep(5)
        os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'bottom-right.mp4')

    def stitch_sections(self):
        filename = self.file_name
        output_filename_dir = os.path.splitext(os.getcwd() +'/output/' + filename)[0]
        output_filename = os.path.splitext(os.getcwd() +'/output/' + filename)[0]
        os.system('ffmpeg -i ' + output_filename_dir +'/' + filename +'top-left.mp4' +
                        ' -i ' + output_filename_dir +'/' + filename +'top-right.mp4' + 
                        ' -i ' + output_filename_dir +'/' + filename +'bottom-left.mp4' + 
                        ' -i ' + output_filename_dir +'/' + filename +'bottom-right.mp4' + 
                        ' -filter_complex "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v]" -map "[v]" ' + 
                        output_filename + '-final.mp4')
        # output_path = os.path.join(output_path  + filename +'top-left.mp4 -i ' + output_path + filename + 'top-right.mp4 -i ' + output_path + filename + 'bottom-left.mp4 -i ' + output_path + filename + 'bottom-right.mp4 -filter_complex "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v]" -map "[v]" ' + (os.path.splitext(output_path + filename)[0]) + '-output.mp4')

    def delete_files(self):
        filename = self.file_name
        output_filename_dir = os.path.splitext(os.getcwd() +'/output/' + filename)[0]
        input_filename_dir = os.path.splitext(os.getcwd() + '/input/' + filename)[0]
        decimated_file = os.getcwd() + '/input/' + filename +'-decimated.mp4'
        # print(decimated_file)
        os.system('rm -rf ' + input_filename_dir + ' ' + decimated_file + ' ' + output_filename_dir)
        
#%%

#%%
split = HighRes('berlin.mp4', '4')
#%%

split.create_dir()
split.remove_dup_frames()
split.run_splitter()
split.run_feature_flow()

#%%
split.stitch_sections()
split.delete_files()
#%%