import os


def pkg_install(package):
    import pip

    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def test_playsound():
    try:
        import playsound
    except ImportError as e:
        pkg_install('playsound')
        import playsound
    print('play temp.mp3...')
    playsound.playsound('temp.mp3')
    print('play 한글.mp3...')
    playsound.playsound('한글.mp3')


def test_simpleaudio():
    try:
        import simpleaudio as sa
    except ImportError as e:
        pkg_install('simpleaudio')
        import simpleaudio as sa

    filename = '한글.mp3'
    mp3_obj = sa.WaveObject.from_mp3_file(filename)
    play_obj = mp3_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


def test_winsound():
    import winsound

    print(os.getcwd())
    filename = './temp.wav'
    # with open(filename,'rb') as f:
    #     winsound.PlaySound(f.read(),winsound.SND_MEMORY)
    winsound.PlaySound(filename, winsound.SND_FILENAME)


def test_sounddevice():
    import sounddevice as sd
    import soundfile as sf

    filename = '한글.mp3'
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    status = sd.wait()
    print(status)


def test_pydub():
    from pydub import AudioSegment
    from pydub.playback import play

    sound = AudioSegment.from_mp3('한글.mp3')
    play(sound)


if __name__ == '__main__':
    # test_playsound()
    # test_simpleaudio()
    # test_winsound()
    test_sounddevice()
    # test_pydub()
