#%%
import os , shutil, time, sys, errno
from os import pipe
from pathlib import Path

from numpy.core.arrayprint import str_format
from sequence_run import main
import cv2

ffmpeg_exe = Path().cwd() / 'ffmpeg.exe'

class CheckResolution:
    def __init__(self, file_name):
        self.file = file_name
        self.vcap = cv2.VideoCapture(self.file)
    
    def getWidth(self):
        width = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        return int(width)

    def getHeight(self):
        height = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return int(height)

class Resolution360P:
    def __init__(self, file_input_path_from_gui : str, interpolation : int, output_path_from_gui : str):
        self.current_working_dir : str = Path.cwd()
        self.input_video : str = file_input_path_from_gui
        self.file_name : str = os.path.splitext(file_input_path_from_gui)[0]   # returns file name from example.mp4 to example
        self.interp_num : int = interpolation 
        self.output_path : str = output_path_from_gui

        self.finished_file_name : str = Path.cwd() / str(self.file_name + '-final.mp4')
        self.interp_output_file_name : str = Path.cwd() / 'output.mp4'

    # def removeDupFrames(self):
        # filename = self.dir_name_based_off_filename
        # file = self.path_to_dir_name_based_off_filename / filename
        # print(file)
        # print('ffmpeg.exe  -qscale 0 -i ' + str(self.file_name) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
        # os.system('ffmpeg.exe -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
        # os.system(str(ffmpeg_exe) + ' -i '+ str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')

    def runFeatureFlow(self):
        print(self.interp_num)
        print('Input Video: ',(self.input_video))

        main(self.interp_num, self.input_video)

        print(Path(self.interp_output_file_name) / Path(self.output_path))
        time.sleep(3)
        shutil.move('output.mp4', Path(self.interp_output_file_name) / Path(self.output_path))

    def deleteFiles(self):
        cwd = Path(self.current_working_dir)
        filename = self.dir_name_based_off_filename
        cwd_decimated_file = cwd / str(filename + '-decimated.mp4')
        # decimated_file = str(Path(self.input_dir / filename)) + '-decimated.mp4'
        print(cwd_decimated_file)
        os.remove(cwd_decimated_file)

class Resolution720P:

    def __init__(self, file_name, interpolation, output_path_from_gui):
        self.file_name = file_name
        self.interpolation = int(interpolation)
        self.input_dir = ''
        self.top_left_dir = ''
        self.top_right_dir = ''
        self.bottom_left_dir = ''
        self.bottom_right_dir = ''
        self.file_dir_name = os.path.splitext(self.file_name)[0]
        self.output_dir = ''
        self.output_file_dir = ''
        self.current_working_dir = ''
        self.filename_dir = ''
        # self.model_dir = './models/bdcn/final-model/bdcn_pretrained_on_bsds500.pth'
        # self.model_dir = '.\\models\\bdcn\\final-model\\bdcn_pretrained_on_bsds500.pth'
        self.output_path = output_path_from_gui

        if self.interpolation % 2 != 0:
            # print('Use the power of two for interpolation')
            sys.exit('Error!: Use the power of two for interpolation')


    def create_dir(self):
                    
        self.current_working_dir = os.getcwd()
        self.input_dir = Path(self.current_working_dir + '/input/')
        self.filename_dir = self.input_dir / self.file_dir_name
        self.top_left_dir = self.filename_dir / 'top-left'
        self.top_right_dir = self.filename_dir / 'top-right'
        self.bottom_left_dir = self.filename_dir / 'bottom-left'
        self.bottom_right_dir = self.filename_dir / 'bottom-right'

        # self.output_dir = Path(self.current_working_dir + '/output/')
        self.output_dir = Path(self.output_path + '/output/')
        self.output_file_dir = self.output_dir / self.file_dir_name
        
        Path(self.output_file_dir).mkdir(parents=True, exist_ok=True)
        Path(self.filename_dir).mkdir(parents=True, exist_ok=True)
        Path(self.top_left_dir).mkdir(parents=True, exist_ok=True)
        Path(self.top_right_dir).mkdir(parents=True, exist_ok=True)
        Path(self.bottom_left_dir).mkdir(parents=True, exist_ok=True)
        Path(self.bottom_right_dir).mkdir(parents=True, exist_ok=True)

        print(self.file_dir_name)

    def remove_dup_frames(self):
        filename = self.file_dir_name
        file = self.input_dir / filename
        print(file)
        print('ffmpeg -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
        # os.system('ffmpeg -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
        os.system(str(ffmpeg_exe) + ' -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
    
    def run_splitter(self):
        filename = self.file_dir_name
        file = str(self.input_dir / filename)    # /cwd/input/filename

        top_left_dir = str(self.top_left_dir)
        os.system(str(ffmpeg_exe) + ' -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:0" ' + top_left_dir + '/' +'decimated-top-left.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:0" ' + top_left_dir + '/' +'decimated-top-left.mp4')

        # remove top right
        top_right_dir = str(self.top_right_dir)
        os.system(str(ffmpeg_exe) + ' -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:0" ' + top_right_dir + '/' +'decimated-top-right.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:0" ' + top_right_dir + '/' +'decimated-top-right.mp4')
        

        # remove bottom left
        bottom_left_dir = str(self.bottom_left_dir)
        os.system(str(ffmpeg_exe) + ' -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + bottom_left_dir + '/' +'decimated-bottom-left.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + bottom_left_dir + '/' +'decimated-bottom-left.mp4')
        

        # remove bottom right
        bottom_right_dir = str(self.bottom_right_dir)
        os.system(str(ffmpeg_exe) + ' -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + bottom_right_dir + '/' +'decimated-bottom-right.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + bottom_right_dir + '/' +'decimated-bottom-right.mp4')
        
    
    def run_feature_flow(self):
        interpolation_num = self.interpolation
        filename = self.file_dir_name
        cwd = Path(self.current_working_dir)
        cwd_output_file = cwd / 'output.mp4'
        # TOP LEFT
        print('INTERP TOP LEFT')
        top_left_file = str(self.top_left_dir / 'decimated-top-left.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_left_file + ' --t_interp ' + str(interpolation_num))
        # os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_left_file + ' --t_interp ' + str(interpolation_num))
        # os.system('set CUDA_VISIBLE_DEVICES= 0 & python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_left_file + ' --t_interp ' + str(interpolation_num))
        # main(interpolation_num, str(self.model_dir) ,'checkpoints/FeFlow.ckpt', top_left_file)
        # print(interpolation_num)
        main(interpolation_num, top_left_file)

        print("!!!CWD OUTPUT")
        print(cwd_output_file)
        print(str(self.output_file_dir))
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        time.sleep(5)
        
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-left.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-left.mp4')
        
        # TOP RIGHT
        print('INTERP TOP RIGHT')
        top_right_file = str(self.top_right_dir / 'decimated-top-right.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_right_file + ' --t_interp ' + str(interpolation_num))
        # os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_right_file + ' --t_interp ' + str(interpolation_num))
        # os.system('set CUDA_VISIBLE_DEVICES= 0 & python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_right_file + ' --t_interp ' + str(interpolation_num))
        # main(interpolation_num, str(self.model_dir) ,'checkpoints/FeFlow.ckpt', top_right_file)
        main(interpolation_num, top_right_file)
        # MOVE
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        time.sleep(5)
        
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-right.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-right.mp4')
        
        # BOTTOM LEFT
        print('INTERP BOTTOM LEFT')
        bottom_left_file = str(self.bottom_left_dir / 'decimated-bottom-left.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_left_file + ' --t_interp ' + str(interpolation_num))
        # os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_left_file + ' --t_interp ' + str(interpolation_num))
        # os.system('set CUDA_VISIBLE_DEVICES= 0 & python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_left_file + ' --t_interp ' + str(interpolation_num))
        # main(interpolation_num, str(self.model_dir)  ,'checkpoints/FeFlow.ckpt', bottom_left_file)
        main(interpolation_num, bottom_left_file)

        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        time.sleep(5)
        
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-left.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-left.mp4')
        
        # BOTTOM RIGHT
        print('INTERP BOTTOM RIGHT')
        bottom_right_file = str(self.bottom_right_dir / 'decimated-bottom-right.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_right_file + ' --t_interp ' + str(interpolation_num))
        # os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_right_file + ' --t_interp ' + str(interpolation_num))
        # os.system('set CUDA_VISIBLE_DEVICES= 0 & python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_right_file + ' --t_interp ' + str(interpolation_num))
        # main(interpolation_num, str(self.model_dir)  ,'checkpoints/FeFlow.ckpt', bottom_right_file)
        main(interpolation_num, bottom_right_file)
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        
        time.sleep(5)
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-right.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-right.mp4')




    def stitch_sections(self):
        filename = self.file_dir_name
        os.system(str(ffmpeg_exe) + ' -i ' + str(self.output_file_dir / 'top-left.mp4') +
                        ' -i ' + str(self.output_file_dir / 'top-right.mp4') + 
                        ' -i ' + str(self.output_file_dir / 'bottom-left.mp4') + 
                        ' -i ' + str(self.output_file_dir / 'bottom-right.mp4') + 
                        ' -filter_complex "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v]" -map "[v]" ' + 
                        str(self.output_dir / filename) + '-final.mp4')
        print((str(ffmpeg_exe) + ' -i ' + str(self.output_file_dir / 'top-left.mp4') +
                        ' -i ' + str(self.output_file_dir / 'top-right.mp4') + 
                        ' -i ' + str(self.output_file_dir / 'bottom-left.mp4') + 
                        ' -i ' + str(self.output_file_dir / 'bottom-right.mp4') + 
                        ' -filter_complex "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v]" -map "[v]" ' + 
                        str(self.output_dir / filename) + '-final.mp4'))

    def delete_files(self):
        filename = self.file_dir_name
        decimated_file = str(Path(self.input_dir / filename)) + '-decimated.mp4'
        print(self.filename_dir)
        print(decimated_file)
        print(self.output_file_dir)
        shutil.rmtree(self.filename_dir)
        os.remove(decimated_file)
        shutil.rmtree(self.output_file_dir)