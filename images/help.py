from PIL import Image
import matplotlib.pyplot as plt

# 이미지 열기
image_path = "Background.png"
img = Image.open(image_path)

# 출력용 설정
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(img)
ax.set_title("Click on each red dot (12 total) to get coordinates")
coords = []

# 클릭 시 좌표 저장
def onclick(event):
    if event.xdata and event.ydata:
        coords.append((round(event.xdata), round(event.ydata)))
        ax.plot(event.xdata, event.ydata, 'go')  # 클릭 표시 (녹색 점)
        fig.canvas.draw()
        if len(coords) == 12:
            plt.close()

# 이벤트 리스너 등록
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

coords
