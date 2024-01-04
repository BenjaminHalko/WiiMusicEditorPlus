import platform


def choose_from_os(array):
    if currentSystem == "Windows":
        return array[0]
    elif currentSystem == "Mac":
        return array[1]
    else:
        return array[2]


currentSystem = platform.system()
if currentSystem == "Darwin":
    currentSystem = "Mac"
