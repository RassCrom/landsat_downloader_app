# Landsat Explorer GUI Application

This project is a PySide6-based GUI application designed to interact with the Landsat Explorer API. It allows users to search for Landsat satellite scenes based on specified parameters, download them, and save metadata to a PostgreSQL database.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)

## Requirements

Before running the application, make sure you have the following installed:

- Python 3.8+
- Landsat API credentials (username and password)

## Installation

1. Clone the Repository1:

    
    git clone [<your-repo-url>](https://github.com/RassCrom/landsat_downloader_app.git)
    cd <your-repo-directory>
    

    Or download it as a zip file.

2. Install the required Python packages:

    You can install the required dependencies using pip. It's recommended to create a virtual environment first:

    
    python -m venv venv
    venv\Scripts\activate  # On Mac use `source venv/bin/activate`
    pip install -r requirements.txt
    

    
    aiohappyeyeballs==2.4.0
    aiohttp==3.10.5
    aiosignal==1.3.1
    attrs==24.2.0
    branca==0.7.2
    certifi==2024.7.4
    charset-normalizer==3.3.2
    click==7.1.2
    colorama==0.4.6
    contourpy==1.2.1
    cycler==0.12.1
    fonttools==4.53.1
    frozenlist==1.4.1
    idna==3.8
    Jinja2==3.1.4
    kiwisolver==1.4.5
    landsatxplore==0.15.0
    MarkupSafe==2.1.5
    multidict==6.0.5
    packaging==24.1
    pandas==2.2.2
    pillow==10.4.0
    psycopg2==2.9.9
    pyparsing==3.1.4
    PySide6==6.7.2
    PySide6_Addons==6.7.2
    PySide6_Essentials==6.7.2
    python-dateutil==2.9.0.post0
    pytz==2024.1
    requests==2.32.3
    Shapely==1.8.5.post1
    shiboken6==6.7.2
    six==1.16.0
    tifffile==2024.8.24
    tqdm==4.66.5
    tzdata==2024.1
    urllib3==2.2.2
    xyzservices==2024.6.0
    yarl==1.9.4
    

## Running the Application

1. Run the Application:

    
    python app.py
    

    The main GUI window will prompt you to enter your Landsat API credentials. After successful authentication, you can search for Landsat scenes based on various parameters like coordinates, cloud cover, and acquisition dates.

2. Interacting with the Application:

    - Search for Scenes: Enter your search parameters and click "Submit Parameters."
    - Download Scenes: After displaying search results, select a scene and specify the directory to save the downloaded scene.
    - Save Metadata: Metadata for the downloaded scenes will be saved to your PostgreSQL database.