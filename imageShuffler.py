import hashlib
import os
import random
import shutil

image_dir = "./images"
metadata_dir = "./metadata"

image_dir_shuffled = "./images_shuffled"
metadata_dir_shuffled = "./metadata_shuffled"

pre_shuffle_hashes = []
post_shuffle_hashes = []

# Calculate the sha256 hash of this script and prepend to the image hashes
def generate_shuffler_hash():
    with open("./imageShuffler.py", "rb") as f:
        bytes = f.read()
        pre_shuffle_hashes.append(hashlib.sha256(bytes).hexdigest())

# Calculate the provance hash for the pre-shuffled images
def provance_images(img_dir, hash_list):
    for file in os.listdir(img_dir):
        f = os.path.join(img_dir, file)
        
        if os.path.isfile(f):
            with open(f,"rb") as img:
                bytes = img.read()
                image_hash = hashlib.sha256(bytes).hexdigest();
                hash_list.append(image_hash)
    
    full_hashes = ''.join([str(item) for item in hash_list])
    
    return hashlib.sha256(full_hashes.encode('utf-8')).hexdigest()

# Shuffle the order of the files and rename them appropriately
def shuffle_files(SEED):
    # Use the input seed for the random number generation
    random.seed(a=SEED, version=2)

    shuffled_order = list(range(1, 5001))

    # Shuffle the list using our input seed
    random.shuffle(shuffled_order)

    for i in range(1, 5001):
        orig_img = image_dir + "/" + str(i) + ".png"
        new_img = image_dir_shuffled + "/" + str(shuffled_order[i - 1]) + ".png"

        # Copy and rename the image files
        shutil.copy(orig_img, new_img)

        orig_metadata = metadata_dir + "/" + str(i) + ".json"
        new_metadata = metadata_dir_shuffled + "/" + str(shuffled_order[i - 1]) + ".json"

        # Copy and rename the image files
        shutil.copy(orig_metadata, new_metadata)

def update_metadata():
    for i in range(1, 5001):
        with open(metadata_dir_shuffled + "/" + str(i) + ".json", 'r') as file:
            data = file.readlines()

        data[1] = "    \"image\": \"./images/" + str(i) + ".png\","
        data[2] = "    \"tokenId\": " + str(i) + ","
        data[3] = "    \"name\": \"significant other #" + str(i) + "\","

        with open(metadata_dir_shuffled + "/" + str(i) + ".json", 'w') as file:
            file.writelines(data)

def main():
    generate_shuffler_hash()

    pre_provance_hash = provance_images(image_dir, pre_shuffle_hashes)
    print("The provance hash of the pre-shuffled images (and shuffler code) is: " + pre_provance_hash)

    # Don't forget to edit the seed here
    # In this example, I'm using the block difficulty of 14674950
    # Read this thread for more info:
    # https://twitter.com/NftDoyler/status/1519773448129720321
    shuffle_files(13339078252959038)

    update_metadata()

    post_provance_hash = provance_images(image_dir_shuffled, post_shuffle_hashes)
    print("The provance hash after shuffling is: " + post_provance_hash)

if __name__ == "__main__":
   main()