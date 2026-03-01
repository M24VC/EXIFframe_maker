from PIL import Image, ImageDraw, ImageFont, ImageOps
import pathlib
import pyexiv2
from fractions import Fraction
from nikon_lens import LensMapDict
import os

mytags = ["Make", "Model", "ExposureTime", "FNumber", "ISOSpeedRatings", "DateTimeOriginal", "LensModel", "FocalLength"]
default_exif_message = ""
color_black = (0, 0, 0)
color_gray = (100, 100, 100)
selected_logo = 'Nikon_yellow'
output_dir = '/output'
output_suffix = '_with_frame'

def convert_to_printable_date(string):
    string = string[:10]
    string = string.replace(':', '/')
    return string

def convert_to_hex(val):
    hexstr = str(hex(int(val))).replace('0x', '').upper()
    if len(hexstr) == 1:
        hexstr = f"0{hexstr}"
    return hexstr

def get_nikon_lensname(all_data):
    lensname = default_exif_message
    LensID = ""
    FStop = ""
    MinFocalLength = ""
    MaxFocalLength = ""
    MaxApertureAtMinFocal = ""
    MaxApertureAtMaxFocal = ""
    MCUVersion = ""
    LensType = ""
    for key, val in all_data.items():
        if "LensID" in key:
            LensID = convert_to_hex(val)
        if "FStop" in key:
            subs = val.split(' ')
            FStop = convert_to_hex(subs[0])
        if "MinFocalLength" in key:
            MinFocalLength = convert_to_hex(val)
        if "MaxFocalLength" in key:
            MaxFocalLength = convert_to_hex(val)
        if "MaxApertureAtMaxFocal" in key:
            MaxApertureAtMaxFocal = convert_to_hex(val)
        if "MaxApertureAtMinFocal" in key:
            MaxApertureAtMinFocal = convert_to_hex(val)
        if "MCUVersion" in key:
            MCUVersion = convert_to_hex(val)
        if "LensType" in key:
            LensType = convert_to_hex(val)

        querystr = f"{LensID} {FStop} {MinFocalLength} {MaxFocalLength} {MaxApertureAtMinFocal} {MaxApertureAtMaxFocal} {MCUVersion} {LensType}"
        if querystr in LensMapDict:
            lensname = LensMapDict[querystr]

    return lensname

def get_exif_data(image_path):
    exif_data = {}
    try:
        img = pyexiv2.Image(image_path, encoding='big5')
        all_data = img.read_exif()
        img.close()

        for key, val in all_data.items():
            if "Exif.Image.Make" in key:
                if val == "NIKON CORPORATION":
                    exif_data["LensModel"] = get_nikon_lensname(all_data)
                else:
                    exif_data["Make"] = val
            if "Exif.Image.Model" in key:
                exif_data["Model"] = val
            if "Exif.Photo.ExposureTime" in key:
                exif_data["ExposureTime"] = str(Fraction(val))
            if "Exif.Photo.FNumber" in key:
                exif_data["FNumber"] = float(Fraction(val))
            if "Exif.Photo.ISOSpeedRatings" in key:
                exif_data["ISO"] = val
            if "Exif.Photo.DateTimeOriginal" in key:
                exif_data["DateTimeOriginal"] = convert_to_printable_date(val)
            if "Exif.Photo.FocalLength" in key:
                exif_data["FocalLength"] = str(Fraction(val))
            if "Exif.Photo.LensModel" in key:
                exif_data["LensModel"] = val
    except Exception:
        return {}

    return exif_data

def draw_watermark_frame(image_path, input_logo, bool_output=False):
    try:
        exif_data = get_exif_data(image_path)
        mm, iso, f, exptime = (
            exif_data.get("FocalLength", default_exif_message),
            exif_data.get("ISO", default_exif_message),
            exif_data.get("FNumber", default_exif_message),
            exif_data.get("ExposureTime", default_exif_message)
        )
        text_shotinfo = (
            default_exif_message
            if default_exif_message in (mm, iso, f, exptime)
            else "{}mm  ISO{}  f{}  {}s".format(mm, iso, f, exptime)
        )
        text_model = "{}".format(exif_data.get("Model", default_exif_message))
        text_lens = "{}".format(exif_data.get("LensModel", default_exif_message))
        text_datetime = "{}".format(exif_data.get("DateTimeOriginal", default_exif_message))

        image_original = Image.open(image_path).convert("RGBA")
        image_original = ImageOps.exif_transpose(image_original)

        image_size = image_original.size
        blank_height = int(min(image_size[0], image_size[1])/10)
        padding = int(blank_height/5)
        padding_left = padding
        font_size = int(blank_height/4)

        font_dir = os.path.dirname(__file__)
        font_regular = os.path.join(font_dir, "Saira_Semi_Condensed", "SairaSemiCondensed-Regular.ttf")
        font_bold_path = os.path.join(font_dir, "Saira_Semi_Condensed", "SairaSemiCondensed-Bold.ttf")

        font_reualr = ImageFont.truetype(font_regular, size=font_size)
        font_bold = ImageFont.truetype(font_bold_path, size=font_size)
        logo_max_height = int(blank_height/1.5)

        img = Image.new("RGB", (image_size[0], image_size[1] + blank_height), (255, 255, 255))
        img.paste(image_original, (0, 0), image_original)

        draw = ImageDraw.Draw(img)
        padding_top = padding + image_size[1]

        draw.text((padding_left, padding_top), text_shotinfo, fill=color_black, font=font_bold)
        draw.text((padding_left, padding_top + padding + padding//3), text_datetime, fill=color_gray, font=font_reualr)
        max_len = max(font_bold.getlength(text_model), font_reualr.getlength(text_lens))
        position_make = (image_size[0] - padding - max_len, padding_top)
        position_lens = (image_size[0] - padding - max_len, padding_top + padding + padding//3)
        draw.text(position_make, text_model, fill=color_black, font=font_bold, align="left")
        draw.line(
            (
                (position_make[0] - padding//2, position_make[1]),
                (position_lens[0] - padding//2, padding_top + padding*3),
            ),
            fill=color_gray,
            width=int(font_size/8)
        )
        draw.text(position_lens, text_lens, fill=color_gray, font=font_reualr)

        logo_path = os.path.join(os.path.dirname(__file__), "logo", f"{input_logo}.png")
        logo = Image.open(logo_path)
        width, height = logo.size
        new_width = int((logo_max_height/height) * width)
        logo = logo.resize((new_width, logo_max_height), Image.Resampling.LANCZOS).convert("RGBA")

        img.paste(
            logo,
            (
                int(image_size[0] - max_len - padding - logo.size[0] - padding),
                image_size[1] + int((blank_height - logo_max_height)/2)
            ),
            logo
        )

        if bool_output == True:
            original_path = pathlib.Path(image_path)
            output_dir_path = pathlib.Path(output_dir)
            output_dir_path.mkdir(parents=True, exist_ok=True)
            output_path = output_dir_path / f"{original_path.stem}{output_suffix}{original_path.suffix}"
            try:
                img.save(str(output_path))
            except Exception:
                pass
        else:
            img_width, img_height = img.size
            canvas_max_width = 600
            canvas_max_height = 400
            ratio = min(canvas_max_width / img_width, canvas_max_height / img_height)
            new_img_width = int(img_width * ratio)
            new_img_height = int(img_height * ratio)
            img = img.resize((new_img_width, new_img_height), Image.Resampling.LANCZOS)
        return img
    except Exception:
        return None

def generate(img_path_list, logo, dir, suffix):
    global selected_logo
    global output_dir
    global output_suffix
    selected_logo = (logo)
    output_dir = dir
    output_suffix = suffix
    for current_path in img_path_list:
        try:
            draw_watermark_frame(current_path, input_logo=selected_logo, bool_output=True)
        except Exception:
            pass
    return 0
