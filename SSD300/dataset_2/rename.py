import os


def rename():
    with os.scandir('./') as entries:
        for entry in entries:
            if not entry.is_file():
                continue
            split = entry.name.split("_")

            if len(split) == 2 and "png.rf" in split[1]:
                print(entry.name)
                os.rename(entry.name, f"{split[0]}.png")


def move():
    with os.scandir('./') as entries:
        for entry in entries:
            if not entry.is_file():
                continue
            print(entry.name)
            if entry.name.endswith(("png", "jpg", "webp", "jpeg")):
                os.rename(entry.name,  f"./images/{entry.name}")
            elif entry.name.endswith(("xml")):
                os.rename(entry.name,  f"./annotations/{entry.name}")


move()
