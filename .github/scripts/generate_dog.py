import os
from PIL import Image, ImageDraw, ImageSequence
from datetime import date, timedelta
import random

# Kích thước mỗi ô contribution
CELL_SIZE = 12
GAP = 2
GRID_COLS = 53  # số tuần trong năm
GRID_ROWS = 7   # các ngày trong tuần
WIDTH = GRID_COLS * (CELL_SIZE + GAP) + 40
HEIGHT = GRID_ROWS * (CELL_SIZE + GAP) + 40

# Màu sắc cho ô contribution (dùng tông xanh lá thiên nhiên)
COLORS = {
    0: (235, 237, 240),      # không đóng góp
    1: (155, 233, 168),      # thấp
    2: (64, 196, 99),        # vừa
    3: (48, 161, 78),        # cao
    4: (33, 110, 57)         # rất cao
}

def draw_grid(draw, day_offset):
    """Vẽ lưới contribution giả lập (hoặc bạn có thể lấy dữ liệu thật từ GitHub API)"""
    # Vẽ các ô
    for week in range(GRID_COLS):
        for day in range(GRID_ROWS):
            x = 20 + week * (CELL_SIZE + GAP)
            y = 20 + day * (CELL_SIZE + GAP)
            # Tô màu ngẫu nhiên để đẹp mắt (hoặc dùng dữ liệu thật)
            intensity = random.choices([0,1,2,3,4], weights=[20,40,30,8,2])[0]
            color = COLORS[intensity]
            draw.rectangle([x, y, x+CELL_SIZE-1, y+CELL_SIZE-1], fill=color, outline=(200,200,200,100))

def draw_dog(draw, dog_img, week, day):
    """Đặt sprite chó vào vị trí ô (week, day)"""
    x = 20 + week * (CELL_SIZE + GAP) + (CELL_SIZE - dog_img.width) // 2
    y = 20 + day * (CELL_SIZE + GAP) + (CELL_SIZE - dog_img.height) // 2
    draw.bitmap((x, y), dog_img, fill=None)

def create_frame(dog_img, week, day):
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255,255,255,0))
    draw = ImageDraw.Draw(img)
    draw_grid(draw, 0)
    draw_dog(draw, dog_img, week, day)
    return img

def main():
    # Đọc sprite chó
    dog_path = os.path.join('assets', 'dog.png')
    if not os.path.exists(dog_path):
        print(f"Không tìm thấy {dog_path}, tạo ảnh trống.")
        dog_img = Image.new('RGBA', (10, 10), (255,0,0,255))  # placeholder
    else:
        dog_img = Image.open(dog_path).convert('RGBA')
        # Resize nếu to quá
        dog_img.thumbnail((CELL_SIZE-2, CELL_SIZE-2), Image.LANCZOS)

    frames = []
    # Tổng số ô trên grid
    total_cells = GRID_COLS * GRID_ROWS

    # Tạo các frame: chó di chuyển zigzag từ trên xuống dưới, trái sang phải
    for step in range(total_cells):
        # Tính vị trí tuần và ngày trong tuần
        # Đường đi: cột tăng dần, mỗi cột đi từ row=0 đến row=6 theo chiều luân phiên
        week = step // GRID_ROWS
        pos_in_col = step % GRID_ROWS
        # Đi xuống nếu cột chẵn, đi lên nếu cột lẻ
        if week % 2 == 0:
            day = pos_in_col
        else:
            day = GRID_ROWS - 1 - pos_in_col

        frame = create_frame(dog_img, week, day)
        frames.append(frame)

    # Xuất GIF
    output = os.path.join('output', 'dog-run.gif')
    os.makedirs('output', exist_ok=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=80,      # thời gian mỗi frame (ms)
        loop=0,
        disposal=2
    )
    print(f"Đã tạo GIF: {output}")

if __name__ == '__main__':
    main()