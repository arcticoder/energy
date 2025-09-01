#!/usr/bin/env python3
"""
Upload HTS coil simulation data to Zenodo
"""

import json
import os
import requests
import tarfile
from pathlib import Path
from datetime import datetime
import shutil

def create_data_package(output_dir: Path):
    """Create comprehensive data package for upload"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all artifacts
    artifacts_dir = Path("artifacts")
    if artifacts_dir.exists():
        for file in artifacts_dir.glob("*.json"):
            shutil.copy2(file, output_dir / file.name)
        for file in artifacts_dir.glob("*.png"):
            shutil.copy2(file, output_dir / file.name)
        for file in artifacts_dir.glob("*.csv"):
            shutil.copy2(file, output_dir / file.name)
    
    # Copy simulation figures
    figures_dir = Path("papers/figures")
    if figures_dir.exists():
        figures_output = output_dir / "figures"
        figures_output.mkdir(exist_ok=True)
        for file in figures_dir.glob("*.png"):
            shutil.copy2(file, figures_output / file.name)
    
    # Copy example configurations
    examples_dir = Path("examples")
    if examples_dir.exists():
        examples_output = output_dir / "examples"
        examples_output.mkdir(exist_ok=True)
        for file in examples_dir.glob("*.json"):
            shutil.copy2(file, examples_output / file.name)
    
    # Create metadata file
    metadata = {
        "title": "REBCO HTS Coil Optimization Raw Simulation Data",
        "description": "Raw simulation data for REBCO high-temperature superconducting coil optimization including field maps, stress tensors, optimization results, and sensitivity analysis for fusion and antimatter applications.",
        "version": "1.0.0",
        "authors": [
            {
                "name": "Your name here",
                "affiliation": "Your affiliation"
            }
        ],
        "keywords": [
            "superconducting magnets",
            "REBCO",
            "high-temperature superconductors", 
            "fusion energy",
            "antimatter physics",
            "electromagnetic optimization",
            "finite element analysis",
            "stress analysis"
        ],
        "license": "MIT",
        "upload_type": "dataset",
        "generated_date": datetime.now().isoformat(),
        "file_description": {
            "optimization_results.json": "Grid search optimization results for Helmholtz pair configurations",
            "fea_results.json": "Finite element analysis results including stress tensor data",
            "field_validation.json": "Magnetic field validation against analytical solutions",
            "tolerance_analysis.json": "Monte Carlo sensitivity analysis with manufacturing tolerances",
            "energy_efficiency_metrics.json": "Energy efficiency and performance metrics",
            "figures/": "High-resolution field maps and stress distribution visualizations",
            "examples/": "Configuration files for reproducible simulations"
        }
    }
    
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Create README
    readme_content = """# REBCO HTS Coil Optimization Simulation Data

This dataset contains raw simulation data supporting the paper "Optimization of REBCO High-Temperature Superconducting Coils for High-Field Applications in Fusion and Antimatter Trapping".

## Contents

### Core Results
- `optimization_results.json`: Grid search optimization results for Helmholtz pair configurations
- `fea_results.json`: Finite element analysis stress tensor results  
- `field_validation.json`: Magnetic field validation against analytical solutions
- `tolerance_analysis.json`: Monte Carlo sensitivity analysis with manufacturing tolerances
- `energy_efficiency_metrics.json`: Energy efficiency and performance metrics

### Visualizations  
- `figures/field_map.png`: Magnetic field distribution visualization
- `figures/stress_map.png`: Maxwell stress distribution analysis
- `figures/prototype.png`: Engineering schematic of reinforced design

### Configuration Files
- `examples/`: JSON configuration files for reproducible simulations

## Data Description

The optimization framework couples electromagnetic, thermal, and mechanical analysis for REBCO coils:

- **Magnetic Field**: 2.1 T central field with 0.01% ripple  
- **Operating Current**: 1171 A at 146 A/mm² current density
- **Stress Analysis**: Hoop stress reduced from 175 MPa to 28 MPa via reinforcement
- **Monte Carlo**: 1000-sample sensitivity analysis showing 0.2% feasibility

## License

MIT License - see metadata.json for details
"""
    
    with open(output_dir / "README.md", "w") as f:
        f.write(readme_content)

def create_tarball(data_dir: Path, output_file: Path):
    """Create compressed tarball of data"""
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(data_dir, arcname="hts_coil_simulation_data")
    return output_file

def upload_to_zenodo(token: str, email: str, data_file: Path, metadata_file: Path):
    """Upload data package to Zenodo"""
    
    # Zenodo API endpoints
    base_url = "https://zenodo.org/api"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create new deposition
    print("Creating new Zenodo deposition...")
    create_response = requests.post(f"{base_url}/deposit/depositions", 
                                  headers=headers, json={})
    
    if create_response.status_code != 201:
        raise Exception(f"Failed to create deposition: {create_response.text}")
    
    deposition = create_response.json()
    deposition_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    
    print(f"Created deposition ID: {deposition_id}")
    
    # Upload data file
    print(f"Uploading {data_file.name}...")
    with open(data_file, "rb") as f:
        files_response = requests.put(
            f"{bucket_url}/{data_file.name}",
            data=f,
            headers=headers
        )
    
    if files_response.status_code not in [200, 201]:
        raise Exception(f"Failed to upload file: {files_response.text}")
    
    print(f"✅ File uploaded successfully ({files_response.json().get('size', 'unknown')} bytes)")
    
    # Load and update metadata
    with open(metadata_file) as f:
        metadata = json.load(f)
    
    # Prepare Zenodo metadata format
    zenodo_metadata = {
        "metadata": {
            "title": metadata["title"],
            "description": metadata["description"],
            "upload_type": metadata["upload_type"],
            "creators": [
                {
                    "name": author["name"],
                    "affiliation": author.get("affiliation", "")
                } for author in metadata["authors"]
            ],
            "keywords": metadata["keywords"],
            "license": metadata["license"],
            "version": metadata["version"]
        }
    }
    
    # Update deposition metadata
    print("Updating deposition metadata...")
    metadata_response = requests.put(
        f"{base_url}/deposit/depositions/{deposition_id}",
        headers=headers,
        json=zenodo_metadata
    )
    
    if metadata_response.status_code != 200:
        raise Exception(f"Failed to update metadata: {metadata_response.text}")
    
    # Publish deposition
    print("Publishing deposition...")
    publish_response = requests.post(
        f"{base_url}/deposit/depositions/{deposition_id}/actions/publish",
        headers=headers
    )
    
    if publish_response.status_code != 202:
        raise Exception(f"Failed to publish: {publish_response.text}")
    
    published = publish_response.json()
    doi = published["doi"]
    zenodo_url = published["links"]["record_html"]
    
    print(f"✅ Successfully published to Zenodo!")
    print(f"DOI: {doi}")
    print(f"URL: {zenodo_url}")
    
    return doi, zenodo_url

def main():
    """Main upload workflow"""
    # Load environment from .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    
    token = os.getenv("ZENODO_PAT_TOKEN")
    email = "yourname@email.com"
    
    if not token:
        raise ValueError("ZENODO_PAT_TOKEN not found in environment")
    
    print("🚀 HTS Coil Data Upload to Zenodo")
    print("=" * 50)
    
    # Create data package
    data_dir = Path("zenodo_upload_data")
    print("📦 Creating data package...")
    create_data_package(data_dir)
    
    # Create tarball
    tarball_path = Path("hts_coil_simulation_data.tar.gz")
    print("🗜️  Creating compressed archive...")
    create_tarball(data_dir, tarball_path)
    
    # Upload to Zenodo
    metadata_path = data_dir / "metadata.json"
    print("☁️  Uploading to Zenodo...")
    try:
        doi, url = upload_to_zenodo(token, email, tarball_path, metadata_path)
        
        # Save results
        result = {
            "doi": doi,
            "url": url,
            "upload_date": datetime.now().isoformat(),
            "files_included": list(f.name for f in data_dir.rglob("*") if f.is_file())
        }
        
        with open("zenodo_upload_result.json", "w") as f:
            json.dump(result, f, indent=2)
            
        return doi
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        raise
    finally:
        # Clean up temporary files
        if data_dir.exists():
            shutil.rmtree(data_dir)
        if tarball_path.exists():
            tarball_path.unlink()

if __name__ == "__main__":
    doi = main()
    print(f"\nFinal DOI: {doi}")