# main.py
# This generates Apology videos
# Daniel Kogan, 6/30/2020

import gtts
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.audio.fx.volumex import volumex
import concurrent.futures

from pydub import AudioSegment
from pysrt import SubRipItem
import speech_recognition as sr
import pysrt

import os, random, ffmpy, asyncio
from script import *

# TODO: add subtitles 🥺😳
# TODO: Organize different steps into separate functions (ex: tts to tts function)
# TODO: DEBUG!!! It crashes and is unable to load the video every so often, and that must be fixed

def gen_ID(char):
    ID = ''
    for i in range(char):
        ID += str(random.randint(0, 9))
    return ID

def clutter():
    for i in os.listdir('Temp-Files'):
        if not i=='.gitkeep':
            os.remove('Temp-Files/' + i)

def gtts_to_srt(tts):
    subs = pysrt.SubRipFile()
    # subs = SubRipFile()
    sentences = tts.text.split()
    time = 0
    for index, token in enumerate(sentences):
      start = time
      end = time+350  
      time+=350
      text = token
      # Add a new subtitle to the SubRipFile object
      subs.append(SubRipItem(index=index, start=start, end=end, text=text))
    subs.save("Assets/audio.srt")

def compression(input_name, output_name):
    inp = {input_name: None}
    outp = {output_name: f'-vcodec libx264 -crf 23'} #  -vf subtitles=Assets/audio.srt
    ff = ffmpy.FFmpeg(inputs=inp, outputs=outp)
    print(ff.cmd)
    ff.run()
    
def audio_length(audio_path):
    audio = AudioFileClip(audio_path)
    return audio.duration

async def create_video(bool_inp, ID, apolo):
    loop  = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        result = await loop.run_in_executor(
                            pool, create_video_blocking_function, bool_inp, ID, apolo)

async def create_audio(reason):
    loop  = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as pool:
        result = await loop.run_in_executor(
                pool, create_audio_blocking_function, reason)
        return 'Assets/audio.aac'

def create_audio_blocking_function(reason):
    try:
        script = create_script(reason) # create a script with the reason
        print('Processing audio...')
        audio = gtts.gTTS(script) # create the voiceover
        audio.save('Assets/audio.aac') # download script into an audio file
        return True
    except Exception as e:
        print(e)
        return False

def create_video_blocking_function(bool_inp, ID, apology_reason=None):
    if bool_inp: # if this is true, use the function call var
        reason = apology_reason
    else: # if false, command line input for apology
        reason = input('Why are you apologizing? ') 
    create_audio_blocking_function(reason)
    audioClip = AudioFileClip("Assets/audio.aac")

    audio.save('Assets/audio.aac')
    gtts_to_srt(audio)
    # create_srt_from_audio("Assets/audio.aac") # creates a caption file
    print('processing srt')
    
    audioClip = AudioFileClip("Assets/audio.aac")
    subtitles = SubtitlesClip("Assets/audio.srt")
    # subtitles = TextFileClip("Assets/audio.srt")


    MusicFile = random.choice(os.listdir('./Assets/music'))
    while MusicFile == "./Assets/music/.DS_Store":
      MusicFile = random.choice(os.listdir('./Assets/music'))
    # print(MusicFile)
    try:
        backgroundMusic = AudioFileClip("Assets/music/" + MusicFile)
    except Exception as e:
        print(e)
        print(MusicFile)
        return False
    backgroundMusic = backgroundMusic.set_duration(audioClip.duration)
    NewaudioClip = CompositeAudioClip([audioClip, backgroundMusic]).set_duration(audioClip.duration)
    print('Audio has been processed....')
    print('Processing video...')

    clip1 = random.choice(os.listdir("./Assets/clips"))
    clip2 = random.choice(os.listdir("./Assets/clips"))
    while clip2 == clip1:
        clip2 = random.choice(os.listdir("./Assets/clips"))
    clip3 = random.choice(os.listdir("./Assets/clips"))
    while clip3 == clip2 or clip3 == clip1:
        clip3 = random.choice(os.listdir("./Assets/clips"))

    clip1 = VideoFileClip("Assets/clips/" + clip1)
    clip2 = VideoFileClip("Assets/clips/" + clip2)
    clip3 = VideoFileClip("Assets/clips/" + clip3)

    # backgroundMusic = volumex(backgroundMusic, 0.1)
    final_clip = concatenate_videoclips([clip1, clip2, clip3])
    final_clip = final_clip.subclip(0, audioClip.duration)
    
    # final_clip = CompositeVideoClip([final_clip, subtitles.set_pos(('center','bottom'))])
    
    # subtitles.set_duration(final_clip.duration)
  
    # final_clip.set_audio(subtitles)
    # final_clip = concatenate([final_clip, subtitles])
    
    duration = audioClip.duration # define duration to be used later
    # final_clip = CompositeVideoClip([final_clip, text_clip])
    final_clip.duration = duration

    def Process(final_clip, ID, NewaudioClip):
        try:
            final_clip.set_audio(NewaudioClip).write_videofile("Temp-Files/apology" + ID + ".mov", codec="libx264",
                                                               audio_codec='aac', audio=True,
                                                               temp_audiofile='Temp-Files/temp-audio.m4a',
                                                               fps=30, remove_temp=True)
        except IndexError:
            print(Exception)
            final_clip.subclip(t_end=(final_clip.duration - 1.0 / final_clip.fps)).write_videofile(
                "Temp-Files/apology" + ID + ".mov", codec="libx264", audio_codec='aac',
                audio=True, temp_audiofile='Temp-Files/temp-audio.m4a', fps=30,
                remove_temp=True)
        except Exception as e:
            print(e)
            Process(final_clip, ID, NewaudioClip)
    try:
        Process(final_clip, ID, NewaudioClip)
    except Exception as e:
        print(e)
        clutter()
        return False

    print('Video processed...')
    print('Compressing video...')
    try:
        compression("Temp-Files/apology" + ID + ".mov", "Finished/apology" + ID + ".mp4")
    except Exception as e:
        print(e)
        return False
    os.remove("Temp-Files/apology" + ID + ".mov")
    print('Video compressed...')

    final_clip.close()
    os.remove('Assets/audio.aac')
    os.remove('Assets/audio.srt')
    try:
      os.remove('Assets/music/.DS_Store')
    except:
      pass
    clutter()
    return True


if __name__ == '__main__':
    ID = gen_ID(4)
    asyncio.run(create_video(False,ID))
