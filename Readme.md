# AIQ ML Engineer Assignment

This repository contains the solutions for both Challenge 1 and Challenge 2 as part of the AIQ ML Engineer assignment.

## Table of Contents
- [Project Overview](#project-overview)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Running the Applications](#running-the-applications)
- [Running Tests](#running-tests)
- [Containerization](#containerization)
- [Assumptions Made](#assumptions-made)
- [Future Improvements](#future-improvements)

## Project Overview
This project consists of two challenges:

1. Challenge 1: Circular segmentation of objects in an image. The goal is to segment and identify circular objects in an image, assign unique identifiers, and provide information about each object.
2. Challenge 2: Resizing image data represented in a CSV file. The task involves resizing image width, storing the data in a database, and applying a custom color map.

The solutions are implemented in Python using Flask for the API and containerized with Docker.

## Folder Structure
```
project-root/
├── Dockerfile-circular                # Dockerfile for containerizing the Circular Segmentation API
├── Dockerfile-resizer                 # Dockerfile for containerizing the Image Resizer API
├── requirements.txt                   # File listing all Python dependencies for both APIs
├── uploads/                           # Directory to store uploaded images and annotation files
│   ├── test_image.jpg                 # Example image file for circular segmentation
│   └── _annotations.coco              # Annotation file for Challenge 1 (from Challenge1.zip)
├── csv_files/                         # Directory to store CSV files for the Image Resizer API
│   └── Challenge2.csv                 # CSV file for image resizing
├── circular_segmentation/             # Directory for the Circular Segmentation application
│   ├── circular_segmentation.py       # Main Python script for the Circular Segmentation API
│   ├── circular_segmentation_tests.py # Unit tests for the Circular Segmentation API
└── image_resizer_api/                 # Directory for the Image Resizer application
    ├── image_resizer_api.py           # Main Python script for the Image Resizer API
    ├── image_resizer_api_tests.py     # Unit tests for the Image Resizer API
```

## Requirements
- Python 3.9+
- Docker (if running containerized versions)
- Flask, OpenCV, Pandas, Matplotlib, Numpy (listed in `requirements.txt`)

## Setup Instructions
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/aiq_ml_engineer_assignment.git
   ```
2. Navigate to the project directory:
   ```sh
   cd aiq_ml_engineer_assignment
   ```
3. Set up a virtual environment:
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```
4. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Applications
### Circular Segmentation Application
1. Start the API:
   ```sh
   cd circular_segmentation
   python circular_segmentation.py
   ```
   The application will start on `http://localhost:5000`.

2. Upload an Image:
   Use a tool like Postman or Curl to upload an image.

### Image Resizer API
1. Start the API:
   ```sh
   cd image_resizer_api
   python image_resizer_api.py
   ```
   The application will start on `http://localhost:5001`.

## Running Tests
Tests are included for both applications. To run the tests:

1. Circular Segmentation Tests:
   ```sh
   cd circular_segmentation
   python circular_segmentation_tests.py
   ```

2. Image Resizer API Tests:
   ```sh
   cd ../image_resizer_api
   python image_resizer_api_tests.py
   ```

## Containerization
Dockerfiles are included for both applications.

### Building Docker Images
1. Circular Segmentation:
   ```sh
   docker build -t circular-segmentation -f Dockerfile-circular .
   ```

2. Image Resizer:
   ```sh
   docker build -t image-resizer -f Dockerfile-resizer .
   ```

### Running Docker Containers
1. Circular Segmentation:
   ```sh
   docker run -p 5000:5000 circular-segmentation
   ```

2. Image Resizer:
   ```sh
   docker run -p 5001:5001 image-resizer
   ```

## Assumptions Made
- The circular objects in Challenge 1 have a certain radius threshold to filter out small noise.
- The `depth` column in the CSV file is always present as the first column for Challenge 2.
- The uploaded images are stored in the `uploads/` directory.
- The `_annotations.coco` file follows the standard COCO format for annotations.

## Future Improvements
- Scalability: Implement caching mechanisms and database indexing to improve API response times.
- Error Handling: Add more detailed error messages for different failure scenarios.
- Automation: Set up GitHub Actions to automatically run tests on new commits.
- User Interface: Create a simple web-based interface for users to upload images and interact with the APIs easily.
- Modular Design: Further