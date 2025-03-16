import cv2 as cv
import numpy as np
from tkinter import Tk, filedialog

# جلوگیری از نمایش پنجره اصلی Tkinter
Tk().withdraw()

# Choose image file
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.webp")],
)

if file_path:
    img = cv.imread(file_path)

    if img is None:
        print("Error: Failed to read the image.")
    else:
        # تبدیل تصویر به فضای رنگی HSV
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # محدوده‌های رنگ قرمز در HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        # ایجاد دو ماسک برای تشخیص رنگ قرمز
        mask1 = cv.inRange(hsv_img, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv_img, lower_red2, upper_red2)

        # ترکیب دو ماسک برای پوشش کامل رنگ قرمز
        red_mask = cv.bitwise_or(mask1, mask2)

        # پیدا کردن کانتورهای قسمت‌های قرمز
        contours, _ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # کشیدن کادر دور هر بخش قرمز
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # رنگ سبز با ضخامت ۲ پیکسل

        # نمایش نتایج
        cv.imshow("Original Image with Bounding Boxes", img)
        cv.imshow("Red Mask", red_mask)

        cv.waitKey(0)
        cv.destroyAllWindows()
else:
    print("No file selected.")
