# Project Hyrcania: Automated Olive Oil Quality Control

A machine learning system that classifies the quality and age of extra virgin olive oil using fluorescence and UV absorption spectroscopy.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Option 1: Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd hyrcania
   ```

2. **Build and start the container:**
   ```bash
   docker-compose up --build
   ```

3. **Access Jupyter Lab:**
   - Open your browser and go to: `http://localhost:8888`
   - The notebook `visu.ipynb` will be available in the file browser

### Option 2: Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t hyrcania .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8888:8888 -v $(pwd)/data:/app/data -v $(pwd)/visu.ipynb:/app/visu.ipynb -v $(pwd)/output:/app/output hyrcania jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
   ```

3. **Access Jupyter Lab:**
   - Open your browser and go to: `http://localhost:8888`

## 📁 Project Structure

```
hyrcania/
├── data/                          # Data directory (mounted as volume)
│   └── extracted/                 # Extracted spectroscopy data
├── src/                           # Source code
│   └── hyrcania/                 # Main package
├── visu.ipynb                    # Main analysis notebook
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── pyproject.toml               # Poetry dependencies
└── README.md                    # This file
```

## 🔧 Data Setup

### Option 1: Use your existing data
Place your spectroscopy data in the `data/extracted/` directory with the following structure:
```
data/extracted/
├── Aging Step 0/
│   └── Fluorescence/
│       ├── 20210512_0752_AS0_Q1K2V1U0.csv
│       └── ...
├── Aging Step 1/
│   └── Fluorescence/
│       └── ...
└── ...
```

### Option 2: Generate mock data
The notebook includes a function to generate mock data for testing:
```python
generate_mock_data()
```

## 🐳 Docker Commands

### Build the image
```bash
docker build -t hyrcania .
```

### Run Jupyter Lab
```bash
docker run -p 8888:8888 -v $(pwd)/data:/app/data hyrcania jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

### Run Jupyter Notebook
```bash
docker run -p 8888:8888 -v $(pwd)/data:/app/data hyrcania jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

### Interactive shell
```bash
docker run -it hyrcania /bin/bash
```

### Check installed packages
```bash
docker run hyrcania python -c "import ramanspy; print('RamanSPy version:', ramanspy.__version__)"
```

## 📊 Features

- **Advanced Data Loading**: Robust CSV loading with encoding detection
- **Preprocessing Pipeline**: Quality control and spectral preprocessing
- **Multiple Visualization Types**: 2D, 3D, heatmaps, interactive plots
- **Statistical Analysis**: Comprehensive spectral statistics
- **Peak Analysis**: Peak detection and evolution tracking
- **Machine Learning Integration**: PCA and classification
- **Interactive Dashboard**: Multi-panel Plotly dashboard
- **Data Export**: Save results and visualizations

## 🔬 Scientific Applications

- Olive oil quality assessment
- Aging progression monitoring
- Spectral fingerprint analysis
- Machine learning-based classification
- Quality control automation

## 🛠️ Development

### Local Development (without Docker)
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Start Jupyter
jupyter lab
```

### Adding new dependencies
```bash
poetry add package-name
```

### Updating Docker image after dependency changes
```bash
docker-compose build --no-cache
docker-compose up
```

## 📝 Usage Notes

1. **Memory Management**: The notebook includes memory optimization for large datasets
2. **Data Persistence**: All data and outputs are saved in mounted volumes
3. **Port Configuration**: Jupyter runs on port 8888 by default
4. **Security**: No authentication is enabled for local development

## 🚀 Deployment

### Production Deployment
For production use, consider:
- Adding authentication to Jupyter
- Using HTTPS
- Setting up proper logging
- Configuring resource limits

### Cloud Deployment
The Docker setup makes it easy to deploy on:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Kubernetes clusters

## 📄 License

[Add your license information here]

## 👥 Contributing

[Add contribution guidelines here]

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Contact: marouan.boulahtouf@protonmail.ch
