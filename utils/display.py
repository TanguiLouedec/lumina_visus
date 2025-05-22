import subprocess
import os
from PIL import Image

def allowed_file(filename, allowed_extensions):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def display_image(filepath, method='tiv'):
    """Display an image using the specified method"""
    
    if not os.path.exists(filepath):
        return False, "File does not exist"
    
    try:
        if method == 'tiv':
            # Terminal Image Viewer
            result = subprocess.run(['tiv', filepath], 
                                   capture_output=True, 
                                   text=True)
            return True, result.stdout

        elif method == 'fbi':
            # Framebuffer Imageviewer
            result = subprocess.run(['sudo', 'fbi', '-d', '/dev/fb0', 
                                    '-T', '1', '--nonverbose', '--notitle', '-a', filepath],
                                   capture_output=True,
                                   text=True)
            return True, "Image displayed using FBI"
            
        elif method == 'ascii':
            # Use Python to create ASCII art (basic implementation)
            img = Image.open(filepath)
            img = img.resize((80, 40))
            img = img.convert('L')  # Convert to grayscale
            
            pixels = list(img.getdata())
            chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
            
            ascii_img = ""
            for i, pixel in enumerate(pixels):
                ascii_img += chars[pixel//25]
                if (i+1) % 80 == 0:
                    ascii_img += "\n"
                    
            print(ascii_img)
            return True, ascii_img
            
        elif method == 'dev':
            print(f"Would display: {filepath}")
            import webbrowser
            webbrowser.open(filepath)
            return True, "Image would be displayed (dev mode)"

        else:
            return False, "Unknown display method: {method}"
            
    except Exception as e:
        return False, str(e)

def get_image_list(upload_folder):
    """Get list of all images in the upload folder"""
    images = []
    for filename in os.listdir(upload_folder):
        if allowed_file(filename, {'png', 'jpg', 'jpeg', 'gif'}):
            # Get file creation time for sorting
            filepath = os.path.join(upload_folder, filename)
            ctime = os.path.getctime(filepath)
            images.append({
                'filename': filename,
                'path': filepath,
                'ctime': ctime
            })
    
    # Sort by creation time (newest first)
    return sorted(images, key=lambda x: x['ctime'], reverse=True)