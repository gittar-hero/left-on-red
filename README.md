# Left On Red: PDF Red Pixel Converter

This repository provides two ways to process PDF files by converting all red-tinted pixels into white. This is useful for removing red annotations, highlights, or stamps from documents.

---

## Included Tools

### 1. Web Interface (`app.py`)
A user-friendly [Streamlit]([https://left-on-red.streamlit.app/]) application that allows you to upload PDFs via a browser, adjust red-detection sensitivity in real-time using sliders, and download the processed result.

* **Features:**
    * Interactive threshold adjustment (Red, Green, and Blue offsets).
    * Visual progress tracking.
    * Easy file management.

### 2. Command Line Interface (`leftonred.py`)
A lightweight, scriptable version for quick conversions directly from your terminal.

* **Features:**
    * Automated processing.
    * Ideal for batch processing or integrating into larger workflows.

---


## Installation

Ensure you have Python 3.8+ installed, then clone this repository and install the necessary dependencies:

```bash
# Clone the repository
git clone [https://github.com/gittar-hero/left-on-red.git](https://github.com/gittar-hero/left-on-red.git)
cd left-on-red

# Install requirements

pip install -r requirements.txt

