import math

def calculate_layout(p_w_inch, p_h_inch, b_w_inch, b_h_inch, margin_mm, rotated=True):
    pallet_w = p_w_inch * 25.4
    pallet_h = p_h_inch * 25.4
    
    if rotated:
        box_w = b_h_inch * 25.4
        box_h = b_w_inch * 25.4
    else:
        box_w = b_w_inch * 25.4
        box_h = b_h_inch * 25.4
    
    eff_box_w = box_w + margin_mm
    eff_box_h = box_h + margin_mm
    
    count_x = math.floor((pallet_w - margin_mm) / eff_box_w)
    count_y = math.floor((pallet_h - margin_mm) / eff_box_h)
    
    points = []
    for y in range(count_y):
        for x in range(count_x):
            pos_x = margin_mm + (x * eff_box_w) + (box_w / 2)
            pos_y = margin_mm + (y * eff_box_h) + (box_h / 2)
            points.append((pos_x, pos_y))
            
    return count_x, count_y, points

if __name__ == "__main__":
    nx, ny, pts = calculate_layout(48, 48, 12, 10, 10, rotated=True)
    print(f"Kiosztás: {nx}x{ny} = {len(pts)} doboz")
