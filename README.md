# Skew Correction

This project is made for skew correction of images with text on it. Mainly it was tested on rotated invoices from -10 to 10 degrees. It uses `tesseract` engine to generate hOCR output in html format which contains class `ocr_line` which has `baseline` attribute. This attribute bassicaly contains information of line of words skew in radians.

## Example

User interface is made with `grabio` package, which is very usefull tool for image changing visualizations.
![image](https://github.com/ArtOliinyk/invoices_skew_correction/assets/55375811/30da32da-7b6d-40ed-9bfa-db5c544d3db5)

## Usage

To run this on Docker fork and pull this repository and run following Docker commands:

`docker biuld -t <name-of-container>:<tag>`

`docker run -p 7860:7860 -e GRADIO_SERVER_NAME=0.0.0.0 <username>/<name-of-container>:<tag>`

## Notes

Also you may check `research` directory for some ideas of different ways of solving this task.
