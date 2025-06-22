# 🚀 Hyrcania Project - Portable Setup Guide

## Quick Start (5 minutes)

### 1. Copy to USB/Cloud
Copy the entire project folder to your USB drive or cloud storage.

### 2. On Any Machine with Docker

```bash
# Navigate to project folder
cd hyrcania

# Start the project (one command!)
./run.sh start

# Open browser and go to: http://localhost:8888
```

### 3. Stop when done
```bash
./run.sh stop
```

## 📦 What's Included

Your portable package contains:
- ✅ **Dockerfile** - Complete environment setup
- ✅ **docker-compose.yml** - Easy service management
- ✅ **run.sh** - One-command startup script
- ✅ **backup.sh** - Data backup/restore utility
- ✅ **visu.ipynb** - Main analysis notebook
- ✅ **All dependencies** - Poetry lock file included
- ✅ **Documentation** - Complete setup guides

## 🔧 Requirements

**Minimum:**
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- 4GB RAM
- 10GB free disk space

**Recommended:**
- 8GB RAM
- 20GB free disk space
- Modern web browser

## 🚀 Usage Commands

### Start the project
```bash
./run.sh start
```

### Stop the project
```bash
./run.sh stop
```

### Check status
```bash
./run.sh status
```

### View logs
```bash
./run.sh logs
```

### Restart
```bash
./run.sh restart
```

### Clean up (removes everything)
```bash
./run.sh cleanup
```

## 💾 Data Management

### Create backup
```bash
./backup.sh backup
```

### Restore backup
```bash
./backup.sh restore hyrcania_backup_20241201_143022.tar.gz
```

### List backups
```bash
./backup.sh list
```

## 🌐 Access Points

- **Jupyter Lab**: http://localhost:8888
- **Jupyter Notebook**: http://localhost:8889 (alternative)

## 📁 Data Structure

```
hyrcania/
├── data/                    # Your spectroscopy data
│   └── extracted/
│       ├── Aging Step 0/
│       ├── Aging Step 1/
│       └── ...
├── output/                  # Analysis results
├── visu.ipynb              # Main notebook
└── [configuration files]
```

## 🔍 Troubleshooting

### Docker not running
```bash
# Start Docker Desktop (Windows/Mac)
# Or on Linux:
sudo systemctl start docker
```

### Port already in use
```bash
# Stop existing containers
./run.sh stop

# Or change port in docker-compose.yml
```

### Out of memory
```bash
# Stop other applications
# Or increase Docker memory limit in Docker Desktop settings
```

### Permission denied
```bash
# Make scripts executable
chmod +x run.sh backup.sh
```

## 📞 Support

- Check the main README.md for detailed documentation
- All scripts include help: `./run.sh help` or `./backup.sh help`
- Contact: marouan.boulahtouf@protonmail.ch

## 🎯 Next Steps

1. **First run**: Use mock data to test the system
2. **Add your data**: Place spectroscopy files in `data/extracted/`
3. **Run analysis**: Open `visu.ipynb` in Jupyter Lab
4. **Export results**: Check the `output/` directory
5. **Create backup**: Use `./backup.sh backup` before moving

---

**That's it!** Your project is now completely portable and can run on any machine with Docker. 🎉 