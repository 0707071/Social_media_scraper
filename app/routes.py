import os
import pandas as pd
from flask import Blueprint, request, render_template, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

from .csv_processing import process_file  # Updated function to handle CSV & Excel

main = Blueprint("main", __name__)

# Define upload and processed file directories
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@main.route("/", methods=["GET", "POST"])
def index():
    broken_links = []
    output_file = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")
        output_format = request.form.get("format", "csv")  # Default CSV

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            file_ext = filename.rsplit(".", 1)[-1].lower()
            
            if file_ext in ["csv", "xls", "xlsx"]:
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                uploaded_file.save(file_path)

                # Process the file (supports both CSV & Excel)
                output_file, broken_links = process_file(file_path, output_format)
                
                processed_filename = os.path.basename(output_file)
                processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)
                
                if os.path.exists(output_file):
                    os.rename(output_file, processed_file_path)
                else:
                    flash(f"Processed file not found at {output_file}! Please try again.", "danger")
                    return redirect(url_for("main.index"))

                flash("Processing successful! Download your file below.", "success")
                return render_template("home.html", output_file=processed_filename, broken_links=broken_links)
            else:
                flash("Invalid file format! Please upload a CSV or Excel file.", "danger")
                return redirect(url_for("main.index"))

    return render_template("home.html", broken_links=broken_links)

@main.route("/download")
def download():
    filename = request.args.get("filename")
    if not filename:
        return "No file specified!", 400
    
    file_path = os.path.abspath(os.path.join(PROCESSED_FOLDER, filename))
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("Error: File not found!", "danger")
        return redirect(url_for("main.index"))
