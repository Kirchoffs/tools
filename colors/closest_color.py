import csv

def hex(hex_value):
    return int(hex_value, 16)

def get_euclidean_dist(target, current):
    return sum([(x - y) ** 2 for x, y in zip(target, current)])

def get_cielab(rgb):
    rgb = [e / 255.0 for e in rgb]
    
    # Apply a gamma correction to the RGB values
    rgb = [pow(((e + 0.055) / 1.055), 2.4) if (e > 0.04045) else (e / 12.92) for e in rgb]
    
    # Convert the RGB values to the XYZ color space
    xyz = [
        rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805,
        rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722,
        rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
    ]
    
    # Calculate the reference white point in the XYZ color space
    ref_xyz = [0.9505, 1.0, 1.0890]
    
    # Calculate the CIELAB values
    xyz = [xyz[i] / ref_xyz[i] for i in range(3)]
    xyz = [pow(e, 1.0 / 3.0) if e > 0.008856 else (7.787 * e + 16.0 / 116.0) for e in xyz]
    
    L = 116.0 * xyz[1] - 16.0
    a = 500.0 * (xyz[0] - xyz[1])
    b = 200.0 * (xyz[1] - xyz[2])
    
    return (L, a, b)

def get_cielab_diff(target, current):
    return get_euclidean_dist(get_cielab(target), get_cielab(current))

color_input = input('Input the color hex value with 6 digits: ')
color_input = color_input.replace('#', '')
input_rgb = [hex(color_input[i: i + 2]) for i in range(0, len(color_input), 2)]
color_map = {}

with open('colors.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        color_name = row['color_name']
        color_value = row['color_value']
        color_map[color_value] = color_name

candidate_color_name = ''
candidate_color_delta = float('inf')
for color_value, color_name in color_map.items():
    color_value = color_value.replace('#', '')
    color_rgb = [hex(color_value[i: i + 2]) for i in range(0, len(color_value), 2)]
    cur_color_delta = get_cielab_diff(input_rgb, color_rgb)
    if cur_color_delta < candidate_color_delta:
        candidate_color_delta = cur_color_delta
        candidate_color_name = color_name

print(candidate_color_name)
