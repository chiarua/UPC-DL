import cv2
import os
import numpy as np


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


folder = "D:\\UPC DL\\UPC-DL\\imgs"  # 你的图片文件夹路径
images = load_images_from_folder(folder)


def concatenate_images(images, axis):
    return cv2.vconcat(images) if axis == 0 else cv2.hconcat(images)


def resize_images(images, width, height):
    resized_images = []
    for img in images:
        new_img = cv2.resize(img, (width, height))
        resized_images.append(new_img)
    return resized_images


def create_blank(width, height, color=(0, 0, 0)):
    """创建一个指定大小和颜色的空白图像"""
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:] = color
    return blank_image


def add_image_to_blank(blank_image, img, start_x, start_y):
    """将图片添加到空白图像的指定位置"""
    end_y, end_x = start_y + img.shape[0], start_x + img.shape[1]
    blank_image[start_y:end_y, start_x:end_x] = img
    return blank_image


# 设定你想要的宽度和高度
desired_width = 128
desired_height = 128

# 调整图片尺寸
resized_images = resize_images(images, desired_width, desired_height)

# 创建一个空白图像
blank_image = create_blank(1000, 1000, color=(255, 255, 255))

# 按垂直方向拼接
# img_vconcat = concatenate_images(resized_images, 0)
# cv2.imshow('Vertical Concatenation', img_vconcat)

# 按水平方向拼接
# img_hconcat = concatenate_images(resized_images, 1)
# cv2.imshow('Horizontal Concatenation', img_hconcat)

def add_image_to_blank_with_transparency(blank_image, img, start_x, start_y, alpha, beta):
    """将图片添加到空白图像的指定位置，并改变它的透明度"""
    # 创建一个和空白画布同样大小的全透明图像
    overlay = np.zeros_like(blank_image)

    # 在全透明图像上添加新的图片
    end_y, end_x = start_y + img.shape[0], start_x + img.shape[1]
    overlay[start_y:end_y, start_x:end_x] = img

    # 将全透明图像叠加到空白画布上
    output = cv2.addWeighted(overlay, alpha, blank_image, beta, 1)
    return output


display_img = add_image_to_blank(blank_image, resized_images[1], 372, 500)
display_img = add_image_to_blank(display_img, resized_images[2], 500, 500)
display_img = add_image_to_blank(display_img, resized_images[3], 500, 372)
display_img = add_image_to_blank(display_img, resized_images[4], 372, 372)
display_img = add_image_to_blank_with_transparency(display_img, cv2.resize(resized_images[0], (256, 256)), 372, 372, 0.5, 0.5)

cv2.imshow("display", display_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
