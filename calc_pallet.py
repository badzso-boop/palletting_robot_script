import math

def calculate_layout(p_w_inch, p_h_inch, b_w_inch, b_h_inch, margin_mm):
    # Átváltás mm-be
    pallet_w = p_w_inch * 25.4
    pallet_h = p_h_inch * 25.4
    box_w = b_w_inch * 25.4
    box_h = b_h_inch * 25.4
    
    eff_box_w = box_w + margin_mm
    eff_box_h = box_h + margin_mm
    
    count_x = math.floor(pallet_w / eff_box_w)
    count_y = math.floor(pallet_h / eff_box_h)
    
    points = []
    for y in range(count_y):
        for x in range(count_x):
            # Kiszámoljuk a doboz közepét a raklap sarkához képest
            pos_x = (x * eff_box_w) + (box_w / 2)
            pos_y = (y * eff_box_h) + (box_h / 2)
            points.append((pos_x, pos_y))
            
    return count_x, count_y, points

if __name__ == "__main__":
    # Paraméterek: Raklap W, Raklap H, Doboz W, Doboz H, Margó
    nx, ny, pts = calculate_layout(48, 48, 12, 10, 10)
    
    print(f"Kiosztás: {nx} oszlop x {ny} sor")
    print(f"Összesen: {len(pts)} doboz fér el egy szinten.")
    print("-" * 30)
    for i, p in enumerate(pts):
        print(f"Doboz {i+1:02}: X={p[0]:5.1f}, Y={p[1]:5.1f}")
