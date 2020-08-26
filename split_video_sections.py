#%%
import os , shutil, time, sys, errno
from os import pipe
from pathlib import Path
from sequence_run import main
# from videoprops import get_video_properties
import cv2


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
    def __init__(self, file_name, interpolation, output_path_from_gui):
        self.current_working_dir = ''
        self.file = file_name
        self.interp_num = interpolation
        self.input_dir = ''
        self.dir_name_based_off_filename = os.path.splitext(self.file)[0]
        self.path_to_dir_name_based_off_filename = ''
        self.output_dir_name_based_off_filename = ''
        self.output_path = output_path_from_gui
        

    def createDir(self):
        self.current_working_dir = Path.cwd()
        self.input_dir = self.current_working_dir
        self.path_to_dir_name_based_off_filename = self.input_dir / self.dir_name_based_off_filename
        
        self.output_dir = Path(self.output_path + '/output/')
        self.output_dir_name_based_off_filename = self.output_dir / self.dir_name_based_off_filename

        # Path(self.input_dir /self.path_to_dir_name_based_off_filename).mkdir(parents=True, exist_ok=True)
        # Path(self.output_dir_name_based_off_filename).mkdir(parents=True, exist_ok=True)

    def removeDupFrames(self):
        filename = self.dir_name_based_off_filename
        file = self.path_to_dir_name_based_off_filename / filename
        print(file)
        print('ffmpeg -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
        os.system('ffmpeg -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')

    def runFeatureFlow(self):
        interpolation_num = self.interp_num
        filename = self.dir_name_based_off_filename
        cwd = Path(self.current_working_dir)
        cwd_output_file = cwd / 'output.mp4'
        # TOP LEFT
        print('INTERP TOP LEFT')
        file = str(filename + '-decimated.mp4')
        # print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + file + ' --t_interp ' + str(interpolation_num))
        main(interpolation_num, file)

        
        print('RENAME')
        # print(str(self.output_path / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-left.mp4')
        # os.rename(Path(self.output_path) / 'output.mp4', Path(self.output_path) / 'final-' + str(filename) + '.mp4')
        os.rename(cwd_output_file, str(Path(self.output_path) / filename) + '-final.mp4')
    
        print("!!!CWD OUTPUT")
        renamed_file = str(Path(self.output_path) / filename) + '-final.mp4'
        print(cwd_output_file)
        print(str(self.output_path))
        shutil.move(str(renamed_file), str(self.output_path))
        time.sleep(5)

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
        os.system('ffmpeg -i ' + str(file) + '.mp4 -vsync 0 -frame_pts true -vf mpdecimate ' + str(self.input_dir / filename) + '-decimated.mp4')
    
    def run_splitter(self):
        filename = self.file_dir_name
        file = str(self.input_dir / filename)    # /cwd/input/filename

        top_left_dir = str(self.top_left_dir)
        os.system('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:0" ' + top_left_dir + '/' +'decimated-top-left.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:0" ' + top_left_dir + '/' +'decimated-top-left.mp4')

        # remove top right
        top_right_dir = str(self.top_right_dir)
        os.system('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:0" ' + top_right_dir + '/' +'decimated-top-right.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:0" ' + top_right_dir + '/' +'decimated-top-right.mp4')
        

        # remove bottom left
        bottom_left_dir = str(self.bottom_left_dir)
        os.system('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + bottom_left_dir + '/' +'decimated-bottom-left.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + bottom_left_dir + '/' +'decimated-bottom-left.mp4')
        

        # remove bottom right
        bottom_right_dir = str(self.bottom_right_dir)
        os.system('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + bottom_right_dir + '/' +'decimated-bottom-right.mp4')
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
        os.system('ffmpeg -i ' + str(self.output_file_dir / 'top-left.mp4') +
                        ' -i ' + str(self.output_file_dir / 'top-right.mp4') + 
                        ' -i ' + str(self.output_file_dir / 'bottom-left.mp4') + 
                        ' -i ' + str(self.output_file_dir / 'bottom-right.mp4') + 
                        ' -filter_complex "[0:v][1:v]hstack=inputs=2[top];[2:v][3:v]hstack=inputs=2[bottom];[top][bottom]vstack=inputs=2[v]" -map "[v]" ' + 
                        str(self.output_dir / filename) + '-final.mp4')
        print(('ffmpeg -i ' + str(self.output_file_dir / 'top-left.mp4') +
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

# #%%

# #%%
# split = HighRes('lego.mp4', '2')
# #%%

# #%%
# split.create_dir()
# #%%

# #%%
# split.remove_dup_frames()
# #%%

# #%%
# split.run_splitter()
# #%%

# #%%
# split.run_feature_flow()

# #%%
# split.stitch_sections()
# #%%

# #%%
# split.delete_files()
# #%%
# %%
