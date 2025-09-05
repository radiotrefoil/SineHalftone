import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import gaussian_filter1d
import svgwrite

# Input parameters
input_file = "C:/path_to_file/Einstein.png"
output_file = "Einstein_wave.svg"
band_height = 5      # pixels
oversample = 50      # Sine wave SVG samples per pixel in x direction, keep this a pretty high number or it will be very jagged, 50 is a bit overkill
amp_scale = 2.5      # Increase to make waves higher in y direction
freq_scale = 300     # Increase to make waves closer together in x direction
sigma = 4            # Gaussian smoothing (not really needed but increasing it makes it less spiky, different effect)

##############
img = Image.open(input_file).convert("L")
arr = np.asarray(img) / 255.0  # normalize 0–1
height, width = arr.shape
x = np.linspace(0, width-1, width * oversample)
dwg = svgwrite.Drawing(output_file, size=(width, height))
plt.figure(figsize=(10, 10))

for y in range(0, height, band_height):
    band = arr[y:y+band_height, :].mean(axis=0)
    band_smooth = gaussian_filter1d(band, sigma=sigma)
    amplitude = (1 - band_smooth) * amp_scale
    freq = 1 + freq_scale * (1 - band_smooth)
    amp_interp = np.interp(x, np.arange(width), amplitude)
    freq_interp = np.interp(x, np.arange(width), freq)
    phase = np.cumsum(freq_interp) * (2*np.pi/(width*oversample))
    wave = y + np.sin(phase) * amp_interp
    plt.plot(x, wave, color="black", linewidth=0.8)
    points = [(float(xi), float(wi)) for xi, wi in zip(x, wave)]
    path = "M " + " L ".join(f"{px:.3f},{py:.3f}" for px, py in points)

    # Output SVG line style
    dwg.add(dwg.path(d=path, stroke="black", fill="none", stroke_width=0.2))

dwg.save()

plt.gca().invert_yaxis()
plt.axis("off")
plt.tight_layout()
plt.show()


print(f"Saved SVG to {output_file}")
