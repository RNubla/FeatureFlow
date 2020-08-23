#%%
import os , shutil, time, sys, errno
from pathlib import Path

class HighRes:

    def __init__(self, file_name, interpolation):
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

        if self.interpolation % 2 != 0:
            # print('Use the power of two for interpolation')
            sys.exit('Error!: Use the power of two for interpolation')


    def create_dir(self):
                    
        self.current_working_dir = os.getcwd()
        self.input_dir = Path(self.current_working_dir + '/input/')
        # self.file_dir_name = os.path.splitext(self.file_name)[0]
        filename_dir = self.input_dir / self.file_dir_name
        self.top_left_dir = filename_dir / 'top-left'
        self.top_right_dir = filename_dir / 'top-right'
        self.bottom_left_dir = filename_dir / 'bottom-left'
        self.bottom_right_dir = filename_dir / 'bottom-right'

        self.output_dir = Path(self.current_working_dir + '/output/')
        self.output_file_dir = self.output_dir / self.file_dir_name
        
        # os.mkdir(self.output_file_dir)
        Path(self.output_file_dir).mkdir(parents=True, exist_ok=True)
        # os.makedirs(filename_dir)
        Path(filename_dir).mkdir(parents=True, exist_ok=True)
        # os.makedirs(self.top_left_dir)
        Path(self.top_left_dir).mkdir(parents=True, exist_ok=True)
        # os.makedirs(self.top_right_dir)
        Path(self.top_right_dir).mkdir(parents=True, exist_ok=True)
        # os.makedirs(self.bottom_left_dir)
        Path(self.bottom_left_dir).mkdir(parents=True, exist_ok=True)
        # os.makedirs(self.bottom_right_dir)
        Path(self.bottom_right_dir).mkdir(parents=True, exist_ok=True)

        print(self.file_dir_name)


        # root_dir = os.getcwd()
        # input_dir = 'input'
        # file_dir = self.file_name
        # top_left_dir = 'top-left'
        # top_right_dir = 'top-right'
        # bottom_left_dir = 'bottom-left'
        # bottom_right_dir = 'bottom-right'
        
        # self.input_path = os.path.join(root_dir, input_dir)
        # self.file_path = os.path.join(self.input_path, file_dir)
        # filename_path_no_extensions = os.path.splitext(self.file_path)

        # self.top_left_path = os.path.join(filename_path_no_extensions[0], top_left_dir)
        # self.top_right_path = os.path.join(filename_path_no_extensions[0], top_right_dir)
        # self.bottom_left_path = os.path.join(filename_path_no_extensions[0], bottom_left_dir)
        # self.bottom_right_path = os.path.join(filename_path_no_extensions[0], bottom_right_dir)

        # print(filename_path_no_extensions[0])
        # os.mkdir(filename_path_no_extensions[0])
        # os.mkdir(self.top_left_path)
        # os.mkdir(self.top_right_path)
        # os.mkdir(self.bottom_left_path)
        # os.mkdir(self.bottom_right_path)

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
        # os.system('ffmpeg -i ' + self.input_path + '/' + str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:0" ' + self.top_right_path +'/'+ str(filename)+ '-decimated-top-right.mp4')

        # remove bottom left
        bottom_left_dir = str(self.bottom_left_dir)
        os.system('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + bottom_left_dir + '/' +'decimated-bottom-left.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + bottom_left_dir + '/' +'decimated-bottom-left.mp4')
        # os.system('ffmpeg -i ' + self.input_path + '/' + str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:0:oh" ' + self.bottom_left_path +'/'+ str(filename)+ '-decimated-bottom-left.mp4')

        # remove bottom right
        bottom_right_dir = str(self.bottom_right_dir)
        os.system('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + bottom_right_dir + '/' +'decimated-bottom-right.mp4')
        print('ffmpeg -i ' + file + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + bottom_right_dir + '/' +'decimated-bottom-right.mp4')
        # os.system('ffmpeg -i ' + self.input_path + '/' + str(filename) + '-decimated.mp4 -vsync 0 -frame_pts true -vf "crop=iw/2:ih/2:ow:oh" ' + self.bottom_right_path +'/'+ str(filename)+ '-decimated-bottom-right.mp4')
    
    def run_feature_flow(self):
        interpolation_num = self.interpolation
        filename = self.file_dir_name
        cwd = Path(self.current_working_dir)
        cwd_output_file = cwd / 'output.mp4'
        # output_filename_dir = os.path.splitext(os.getcwd() +'/output/' + filename)[0]
        # os.makedirs(output_filename_dir)
        # TOP LEFT
        print('INTERP TOP LEFT')
        top_left_file = str(self.top_left_dir / 'decimated-top-left.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_left_file + ' --t_interp ' + str(interpolation_num))
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_left_file + ' --t_interp ' + str(interpolation_num))
        # shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        # top_left_file_out = 

        print("!!!CWD OUTPUT")
        print(cwd_output_file)
        print(str(self.output_file_dir))
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        time.sleep(5)
        
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-left.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-left.mp4')
        # os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'top-left.mp4')
        # os.rename(self.output_file_dir / 'output.mp4', self.output_file_dir / 'top-left.mp4')
        
        # TOP RIGHT
        print('INTERP TOP RIGHT')
        top_right_file = str(self.top_right_dir / 'decimated-top-right.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_right_file + ' --t_interp ' + str(interpolation_num))
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + top_right_file + ' --t_interp ' + str(interpolation_num))
        # MOVE
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        time.sleep(5)
        
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-right.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'top-right.mp4')
        # shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        # time.sleep(5)
        # os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'top-right.mp4')
        
        # BOTTOM LEFT
        print('INTERP BOTTOM LEFT')
        bottom_left_file = str(self.bottom_left_dir / 'decimated-bottom-left.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_left_file + ' --t_interp ' + str(interpolation_num))
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_left_file + ' --t_interp ' + str(interpolation_num))
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        time.sleep(5)
        
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-left.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-left.mp4')
        # shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        # time.sleep(5)
        # os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'bottom-left.mp4')
        
        # BOTTOM RIGHT
        print('INTERP BOTTOM RIGHT')
        bottom_right_file = str(self.bottom_right_dir / 'decimated-bottom-left.mp4')
        print('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_right_file + ' --t_interp ' + str(interpolation_num))
        os.system('CUDA_VISIBLE_DEVICES=0 python sequence_run.py --checkpoint checkpoints/FeFlow.ckpt --video_path ' + bottom_right_file + ' --t_interp ' + str(interpolation_num))
        shutil.move(str(cwd_output_file), str(self.output_file_dir))
        
        time.sleep(5)
        print('RENAME')
        print(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-left.mp4')
        os.rename(str(self.output_file_dir / 'output.mp4'), cwd / 'output' / self.file_dir_name /  'bottom-left.mp4')
        # shutil.move(os.getcwd()+ '/output.mp4', output_filename_dir)
        # time.sleep(5)
        # os.rename(output_filename_dir + '/output.mp4', output_filename_dir +'/'+ filename + 'bottom-right.mp4')

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
split = HighRes('berlin.mp4', '2')
#%%

#%%
split.create_dir()
#%%

#%%
split.remove_dup_frames()
#%%

#%%
split.run_splitter()
#%%

#%%
split.run_feature_flow()

#%%
split.stitch_sections()
split.delete_files()
#%%