import os
from algorithms import process_pipeline, display_images

def get_image_files(directory):
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    return [f for f in os.listdir(directory) if f.lower().endswith(supported_formats)]

def choose_image(images):
    print("Available images:")
    for i, image in enumerate(images):
        print(f"{i + 1}. {image}")
    
    while True:
        try:
            choice = int(input("Enter the number of the image you want to process: "))
            if 1 <= choice <= len(images):
                return images[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def validate_image_path(image_path):
    if os.path.isfile(image_path) and image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        return True
    else:
        return False

def get_user_image_path():
    while True:
        image_path = input("Please enter the path to an image: ")
        if validate_image_path(image_path):
            return image_path
        else:
            print("Invalid image path or unsupported file format. Please try again.")

def user_exit():
    close = input("Press enter to continue, or press 'x' and hit enter to exit ")
    return close != ""

        

def main():
    while True:
        app_directory = os.getcwd()
        images = get_image_files(app_directory)
        if not images:
            image_path = get_user_image_path()
        else:
            chosen_image = choose_image(images)
            image_path = os.path.join(app_directory, chosen_image)
        
        images , titles = process_pipeline(image_path)
        
        display_images(images, titles)
        
        if user_exit():
            break

if __name__ == "__main__":
    main() 