
import os
from flask import Blueprint, request, render_template, send_file, redirect, url_for, flash

from .csv_processing import process_csv

main = Blueprint("main", __name__)

# Define upload and processed file directories
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@main.route("/", methods=["GET", "POST"])
def index():
    """
    Home page where users can upload a CSV file for processing.
    - If a valid CSV file is uploaded, it is saved to the 'uploads' directory.
    - The file is then processed using the `process_csv` function.
    - The processed file is moved to the 'processed' directory.
    - Displays success or error messages.
    """
    broken_links = []
    output_file = None  # Default: No output file

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename.endswith(".csv"):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Process the CSV file
            output_file, broken_links = process_csv(file_path)

            # Ensure the processed file is moved to 'processed/' directory
            processed_filename = os.path.basename(output_file)
            processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)

            # Add debug prints to verify paths
            print(f"Processing completed. Expected processed file: {output_file}")
            print(f"Moving to: {processed_file_path}")

            if os.path.exists(output_file):  # Check if the processed file exists
                os.rename(output_file, processed_file_path)  # Move to processed folder
            else:
                flash(f"Processed file not found at {output_file}! Please try again.", "danger")
                return redirect(url_for("main.index"))  # Redirect to home on failure

            flash("Processing successful! Download your file below.", "success")
            return render_template("home.html", output_file=processed_filename, broken_links=broken_links)

    return render_template("home.html", broken_links=broken_links)

@main.route("/download")
def download():
    """
    Allows users to download the processed CSV file.
    - The filename is retrieved from the request query parameters.
    - If the file exists in the 'processed' directory, it is sent for download.
    - If the file is not found, an error message is displayed.
    """
    filename = request.args.get("filename")
    if not filename:
        return "No file specified!", 400
    
    file_path = os.path.abspath(os.path.join(PROCESSED_FOLDER, filename))
    
    print(f"Download requested for: {file_path} (Exists: {os.path.exists(file_path)})")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("Error: File not found!", "danger")
        return redirect(url_for("main.index"))  # Redirect to home
