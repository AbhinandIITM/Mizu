# Plivo-chan 🤖

A powerful AI-powered web application that provides intelligent analysis for images, PDF documents, and audio files using Google's Gemini AI model.

## Features

- **🖼️ Image Analysis**: Upload images and get detailed descriptions including scene analysis, object detection, and contextual information
- **📄 PDF Document Analysis**: Extract and summarize content from PDF documents with intelligent analysis
- **🎵 Audio Transcription**: Convert audio files to text using speech recognition technology
- **🎨 Modern UI**: Clean, responsive web interface with intuitive navigation
- **⚡ Fast Processing**: Built with FastAPI for high-performance async processing

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini 2.5 Flash
- **Frontend**: HTML5, CSS3, JavaScript
- **Template Engine**: Jinja2
- **Image Processing**: Pillow (PIL)
- **PDF Processing**: PyMuPDF
- **Speech Recognition**: SpeechRecognition with Google Speech API
- **Deployment**: Render.com ready

## Prerequisites

- Python 3.8+
- Google Gemini API key
- Internet connection for AI processing and speech recognition

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhinandIITM/Plivo-chan.git
   cd Plivo-chan
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file or set the environment variable:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```
   
   Or on Windows:
   ```cmd
   set GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and use it in your environment variables

## Usage

### Running Locally

1. **Start the development server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

### Using the Application

#### Image Analysis
1. Click on "Image Summariser" in the navigation
2. Upload an image file (JPEG, PNG, etc.)
3. Click "Describe" to get AI-powered analysis
4. View detailed descriptions including objects, scenes, and context

#### PDF Document Analysis
1. Click on "Doc Analysis" in the navigation
2. Upload a PDF document
3. Click "Summarize" to get intelligent document analysis
4. View structured summaries with key insights and document purpose

#### Audio Transcription
1. Click on "Audio Analysis" in the navigation.
2. Upload an audio file (WAV, MP3, etc.).
3. Click "Transcribe" to initiate the transcription process using Google Gemini, which includes speaker diarization.
4. View the transcribed text output as JSON, structured with speaker information, start and end times.

## API Endpoints

### `GET /`
- **Description**: Serves the main web interface
- **Response**: HTML page

### `POST /describe`
- **Description**: Analyzes uploaded images
- **Parameters**: 
  - `file`: Image file (multipart/form-data)
- **Response**: JSON with image description or error

### `POST /analyze-pdf`
- **Description**: Analyzes and summarizes PDF documents
- **Parameters**: 
  - `file`: PDF file (multipart/form-data)
- **Response**: JSON with document summary or error

### `POST /analyze-audio`
- **Description**: Transcribes audio files to text using Google Gemini, including speaker diarization. Returns a JSON array of objects, each containing speaker, start time, end time, and transcribed text.
- **Parameters**: 
  - `file`: Audio file (multipart/form-data)
- **Response**: JSON array of transcription segments with speaker diarization.

## Deployment

### Deploy to Render.com

1. **Fork this repository** to your GitHub account

2. **Connect to Render**
   - Sign up at [Render.com](https://render.com)
   - Connect your GitHub account
   - Create a new Web Service from your forked repository

3. **Configure environment variables**
   - Add `GEMINI_API_KEY` with your actual API key value

4. **Deploy**
   - Render will automatically build and deploy using the `render.yaml` configuration

### Manual Deployment

For other platforms, ensure you:
- Install dependencies: `pip install -r requirements.txt`
- Set the `GEMINI_API_KEY` environment variable
- Run with: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## File Structure

```
Plivo-chan/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── render.yaml            # Render.com deployment config
├── templates/
│   └── index.html         # Web interface
├── README.md              # This file
├── LICENSE                # MIT License
└── .gitignore            # Git ignore rules
```

## Dependencies

- `fastapi==0.104.1` - Modern web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `python-multipart==0.0.6` - File upload support
- `aiofiles==23.2.1` - Async file operations
- `jinja2==3.1.2` - Template engine
- `requests==2.31.0` - HTTP library
- `pillow==10.1.0` - Image processing
- `google-generativeai==0.3.2` - Gemini AI integration
- `pymupdf==1.23.8` - PDF processing
- `speechrecognition==3.10.0` - Audio transcription

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Try it 
Try the project at https://mizuai-r1uh.onrender.com/

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini AI for powerful multimodal AI capabilities
- FastAPI for the excellent web framework
- The open-source community for the amazing libraries used

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/AbhinandIITM/Plivo-chan/issues) page
2. Create a new issue with detailed information
3. Provide error messages and steps to reproduce

---

Made with ❤️ by [AbhinandIITM](https://github.com/AbhinandIITM)
