import os

from core.models import Hostel

hostel_names = [
    "Blessed Arena Hostel",
    "Divine Peace Lodge",
    "Golden View Hostel",
    "Royal Crown Hostel",
    "Victory Home Hostel",
    "Sunrise Student Lodge",
    "Pearl Garden Hostel",
    "Silver Line Hostel",
    "Emerald Hostel",
    "Crystal Lodge",
    "Harmony Hostel",
    "Kings Court Hostel",
    "Peace Villa Hostel",
    "City View Lodge",
    "Prime Hostel",
    "Elite Student Lodge",
    "Comfort Palace Hostel",
    "Dream Home Hostel",
    "Evergreen Lodge",
    "Modern Living Hostel",
    "Blue Roof Hostel",
    "Hilltop Student Lodge",
    "Urban Nest Hostel",
    "Smart Choice Hostel",
    "Platinum Hostel",
    "Fresh Air Lodge",
    "Future Stars Hostel",
    "Unity Hostel",
    "White House Lodge",
    "Hostel Close To Jobitech Obosi",
]

locations = [
    "Behind Jobitech Obosi",
    "Obosi Junction",
    "Near Federal Road",
    "Close To Campus",
    "Behind Obosi Plaza",
    "Near Market Square",
    "Obosi Main Road",
    "Near Health Centre",
]

descriptions = [
    "Affordable and secure hostel with modern facilities.",
    "Comfortable student hostel close to school.",
    "Clean environment with steady water and electricity.",
    "Perfect hostel for students seeking convenience.",
    "Modern rooms with good security and peaceful environment.",
]

prices = [
    120000,
    150000,
    170000,
    180000,
    200000,
    220000,
]

media_path = "media/hostels"

all_images = os.listdir(media_path)

image_files = []

for file in all_images:
    if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".jfif")):
        image_files.append(file)

image_files.sort()

for i, image in enumerate(image_files):

    Hostel.objects.create(
        name=hostel_names[i % len(hostel_names)],
        location=locations[i % len(locations)],
        price=prices[i % len(prices)],
        description=descriptions[i % len(descriptions)],
        image=f"hostels/{image}",
    )

print("All hostels added successfully!")