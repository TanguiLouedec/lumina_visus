from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from config import Config
from utils.display import display_image, get_image_list, allowed_file

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app()

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and display"""
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Display the image
        success, message = display_image(filepath, app.config['DISPLAY_METHOD'])
        
        if success:
            return redirect(url_for('gallery', displayed=filename))
        else:
            return f"Error displaying image: {message}", 500
    
    return redirect(url_for('index'))

@app.route('/gallery')
def gallery():
    """Show gallery of uploaded images"""
    images = get_image_list(app.config['UPLOAD_FOLDER'])
    displayed = request.args.get('displayed', None)
    return render_template('gallery.html', images=images, displayed=displayed)

@app.route('/display/<filename>')
def display(filename):
    """Display a specific image from gallery"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    success, message = display_image(filepath, app.config['DISPLAY_METHOD'])
    
    if success:
        return redirect(url_for('gallery', displayed=filename))
    else:
        return f"Error displaying image: {message}", 500

@app.route('/api/images')
def api_images():
    """API endpoint to get list of images"""
    images = get_image_list(app.config['UPLOAD_FOLDER'])
    return jsonify({
        'images': [{'filename': img['filename']} for img in images]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)