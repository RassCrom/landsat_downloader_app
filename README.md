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

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/RassCrom/landsat_downloader_app.git
    cd landsat_downloader_app
    ```

    Or download it as a zip file.

2. **Install the required Python packages:**

    You can install the required dependencies using pip. It's recommended to create a virtual environment first:

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Mac use `source venv/bin/activate`
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should include the following dependencies:

    ```text
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
    ```

## Running the Application

1. **Run the Application:**

    ```bash
    python app.py
    ```

    The main GUI window will prompt you to enter your Landsat API credentials. After successful authentication, you can search for Landsat scenes based on various parameters like coordinates, cloud cover, and acquisition dates.

2. **Interacting with the Application:**

    - **Search for Scenes:** Enter your search parameters and click "Submit Parameters."
    - **Download Scenes:** After displaying search results, select a scene and specify the directory to save the downloaded scene.
    - **Save Metadata:** Metadata for the downloaded scenes will be saved to your PostgreSQL database.

3. **Setup the PostgreSQL Database:**

   Ensure you have a PostgreSQL instance running. You can connect to a remote PostgreSQL instance using the credentials provided in the code snippet. Modify the connection parameters in the script if needed.

   The database and table for storing the metadata should be set up as follows:

    ```sql
    CREATE DATABASE [DATABASE NAME];

    \c landsat_scenes_metadata;

    CREATE TABLE scene_data (
        id SERIAL PRIMARY KEY,
        display_id TEXT,
        cloud_cover FLOAT,
        landsat_scene_id TEXT,
        acquisition_date TIMESTAMP,
        collection_number INTEGER,
        wrs_path INTEGER,
        wrs_row INTEGER,
        land_cloud_cover FLOAT,
        scene_cloud_cover FLOAT,
        sun_elevation_l0ra FLOAT,
        sun_azimuth_l0ra FLOAT,
        data_type TEXT,
        sensor_id TEXT,
        satellite TEXT,
        product_map_projection TEXT,
        utm_zone INTEGER,
        datum TEXT,
        ellipsoid TEXT,
        scene_center_latitude FLOAT,
        scene_center_longitude FLOAT,
        corner_upper_left_latitude FLOAT,
        corner_upper_left_longitude FLOAT,
        corner_upper_right_latitude FLOAT,
        corner_upper_right_longitude FLOAT,
        corner_lower_left_latitude FLOAT,
        corner_lower_left_longitude FLOAT,
        corner_lower_right_latitude FLOAT,
        corner_lower_right_longitude FLOAT,
        spatial_coverage FLOAT
    );
    ```
