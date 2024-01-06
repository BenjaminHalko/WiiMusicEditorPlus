def ConvertWav(wavPath, loopstart=-1, loopend=-1):
    with tempfile.TemporaryDirectory() as directory:
        if (load_setting("Settings", "ResampleSounds", True)):
            s_read = wave.open(wavPath, 'r')
            framerate = s_read.getframerate()

            if (framerate != 16000 and s_read.getnchannels() != 1):
                wavPath = directory + "converted.wav"
                s_write = wave.open(wavPath, 'w')
                s_write.setparams((1, 2, 16000, 0, 'NONE', 'Uncompressed'))
                data = s_read.readframes(s_read.getnframes())
                if (framerate != 16000):
                    data = audioop.ratecv(data, 2, s_read.getnchannels(), framerate, 16000, None)
                    if (loopstart != -1):
                        loopstart *= 16000 / framerate
                        loopend *= 16000 / framerate
                if (s_read.getnchannels() != 1): data = audioop.tomono(data[0], 2, 1, 0)
                s_write.writeframes(data)
                s_write.close()
            s_read.close()

        cmd = [HelperPath() + "/SoundConverter/rwavconvert", wavPath, directory + "converted.rwav"]
        if (loopstart != -1):
            cmd.append(str(round(loopstart)))
            cmd.append(str(round(loopend)))
        Run(cmd)
        file = open(directory + "converted.rwav", "rb")
        rwavInfo = file.read()
        file.close()
        rwavSize = os.stat(directory + "converted.rwav").st_size

    return rwavInfo, rwavSize


def ReplaceWave(startOffset, replaceNumber, rwavInfo, rwavSize):
    if (not os.path.exists(GetBrsarPath() + ".backup")): copyfile(GetBrsarPath(), GetBrsarPath() + ".backup")
    sizeDifference = 0
    brsar = open(GetBrsarPath(), "r+b")
    brsar.seek(startOffset)
    rwarSpot = int.from_bytes(brsar.read(4), 'big')
    brsar.seek(rwarSpot + 0x18)
    dataSection = rwarSpot + int.from_bytes(brsar.read(4), 'big')
    brsar.seek(rwarSpot + 0x10)
    table = rwarSpot + int.from_bytes(brsar.read(4), 'big')
    brsar.seek(table + 8)
    numberOfRwavs = int.from_bytes(brsar.read(4), 'big')
    if (numberOfRwavs == len(replaceNumber)): replaceNumber = -1
    if (replaceNumber == -1):
        for i in range(numberOfRwavs):
            brsar.seek(table + 0x10 + 0xC * i)
            tempdataSpot = int.from_bytes(brsar.read(4), 'big')
            if (i == 0): dataSpot = tempdataSpot
            dataSize = int.from_bytes(brsar.read(4), 'big')
            brsar.seek(table + 0x10 + 0xC * i)
            offset = int.from_bytes(brsar.read(4), 'big')
            brsar.seek(table + 0x10 + 0xC * i)
            brsar.write((offset + sizeDifference).to_bytes(4, 'big'))
            brsar.seek(table + 0x10 + 0xC * i)
            brsar.write((tempdataSpot + sizeDifference).to_bytes(4, 'big'))
            sizeDifference += rwavSize - dataSize
            brsar.seek(table + 0x10 + 0xC * i + 4)
            brsar.write(rwavSize.to_bytes(4, 'big'))
        brsar.seek(0)
        data1 = brsar.read(dataSection + dataSpot)
        brsar.seek(dataSection + dataSpot + rwavSize * numberOfRwavs - sizeDifference)
        data2 = brsar.read()
        brsar.seek(0)
        brsar.write(data1 + rwavInfo * numberOfRwavs + data2)
        brsar.truncate()
    else:
        for i in replaceNumber:
            brsar.seek(table + 0x10 + 0xC * i)
            dataSpot = int.from_bytes(brsar.read(4), 'big')
            dataSize = int.from_bytes(brsar.read(4), 'big')
            sizeDifference += rwavSize - dataSize
            brsar.seek(table + 0x10 + 0xC * i + 4)
            brsar.write(rwavSize.to_bytes(4, 'big'))
            brsar.seek(0)
            data1 = brsar.read(dataSection + dataSpot)
            brsar.seek(dataSection + dataSpot + dataSize)
            data2 = brsar.read()
            brsar.seek(0)
            brsar.write(data1 + rwavInfo + data2)
            brsar.truncate()
            for j in range(i + 1, numberOfRwavs):
                brsar.seek(table + 0x10 + 0xC * j)
                offset = int.from_bytes(brsar.read(4), 'big')
                brsar.seek(table + 0x10 + 0xC * j)
                brsar.write((offset + rwavSize - dataSize).to_bytes(4, 'big'))

    for offset in [8, startOffset + 4, rwarSpot + 8]:
        brsar.seek(offset)
        size = brsar.read(4)
        brsar.seek(offset)
        brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
    for offset in rseqList:
        if (offset > startOffset):
            brsar.seek(offset)
            size = brsar.read(4)
            brsar.seek(offset)
            brsar.write((int.from_bytes(size, "big") + sizeDifference).to_bytes(4, 'big'))
    brsar.close()


def PlayRwav(startOffset, replaceNumber):
    if (os.path.isdir(SavePath() + "/tmp")):
        try:
            rmtree(SavePath() + "/tmp")
        except Exception:
            tried = True

    if (not os.path.isdir(SavePath() + "/tmp")): os.mkdir(SavePath() + "/tmp")
    brsar = open(GetBrsarPath(), "r+b")
    brsar.seek(startOffset)
    rwarSpot = int.from_bytes(brsar.read(4), 'big')
    brsar.seek(rwarSpot + 0x18)
    dataSection = rwarSpot + int.from_bytes(brsar.read(4), 'big')
    brsar.seek(rwarSpot + 0x10)
    table = rwarSpot + int.from_bytes(brsar.read(4), 'big')
    for i in replaceNumber:
        brsar.seek(table + 0x10 + 0xC * i)
        dataSpot = int.from_bytes(brsar.read(4), 'big')
        dataSize = int.from_bytes(brsar.read(4), 'big')
        brsar.seek(dataSection + dataSpot)
        wav = open(SavePath() + "/tmp/sound" + str(i) + ".rwav", "wb")
        wav.write(brsar.read(dataSize))
        wav.close()
    brsar.close()
    try:
        args = [HelperPath() + "/SoundConverter/vgmstream", "-o", "?f.wav"]
        for i in replaceNumber:
            args.append(SavePath() + "/tmp/sound" + str(i) + ".rwav")
        if (currentSystem == "Mac"):
            command = "vgmstream-cli"
            for i in range(3, len(args)): command += ' "' + args[i] + '"'
            subprocess.run(command, shell=True)
        else:
            Run(args)
    except Exception as e:
        error = ""
        if (currentSystem == "Mac"): error = "Install vgmstream using 'brew install vgmstream'\n"
        error += str(e)
        ShowError("Could not play audio", error)