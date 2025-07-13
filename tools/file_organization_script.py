#!/usr/bin/env python3
"""
Comprehensive File Organization Script for Energy Repository
Organizes all files according to the enhanced repository structure with proper categorization.
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class EnergyRepositoryOrganizer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.organization_log = []
        
    def create_directory_structure(self):
        """Create the enhanced directory structure for the energy repository."""
        directories = [
            # Core implementation directories
            "src/core",
            "src/frameworks",
            "src/integrations",
            "src/validation",
            "src/utils",
            
            # Documentation directories
            "docs/technical",
            "docs/api",
            "docs/tutorials",
            "docs/implementations",
            "docs/uq_resolutions",
            
            # Testing directories
            "tests/unit",
            "tests/integration",
            "tests/performance",
            "tests/validation",
            
            # Data and results directories
            "data/experiments",
            "data/simulations",
            "data/validation_results",
            "results/crew_vessel",
            "results/unmanned_probe",
            "results/hull_optimization",
            "results/uq_analysis",
            
            # Configuration directories
            "config/environments",
            "config/parameters",
            "config/validation",
            
            # Tools and utilities
            "tools/analysis",
            "tools/validation",
            "tools/documentation",
            
            # Examples and demos
            "examples/crew_vessel",
            "examples/unmanned_probe",
            "examples/integration",
            
            # Archives and legacy
            "archive/legacy_implementations",
            "archive/historical_data",
            
            # UQ and analysis
            "uq_framework/resolutions",
            "uq_framework/tracking",
            "uq_framework/analysis"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.organization_log.append(f"Created directory: {directory}")
    
    def organize_crew_vessel_files(self):
        """Organize all crew vessel related files."""
        crew_vessel_files = [
            ("src/crew_vessel_design_framework.py", "src/frameworks/crew_vessel_design_framework.py"),
            ("tests/test_crew_vessel_framework.py", "tests/integration/test_crew_vessel_framework.py"),
            ("crew_vessel_operations_demo.py", "examples/crew_vessel/crew_vessel_operations_demo.py"),
            ("test_crew_vessel_framework.py", "tests/validation/test_crew_vessel_complete.py"),
            ("crew_vessel_design_specifications_*.json", "results/crew_vessel/"),
            ("multi_crew_vessel_validation_results.json", "results/crew_vessel/validation_results.json"),
            ("docs/crew_vessel_implementation_complete.md", "docs/implementations/crew_vessel_implementation_complete.md"),
            ("crew_vessel_uq_resolution.ndjson", "uq_framework/resolutions/crew_vessel_uq_resolution.ndjson")
        ]
        
        self._organize_file_group(crew_vessel_files, "Crew Vessel")
    
    def organize_unmanned_probe_files(self):
        """Organize all unmanned probe related files."""
        unmanned_probe_files = [
            ("src/autonomous_probe_framework.py", "src/frameworks/autonomous_probe_framework.py"),
            ("demonstrate_480c_validation.py", "examples/unmanned_probe/demonstrate_480c_validation.py"),
            ("validate_480c_zero_exotic.py", "examples/unmanned_probe/validate_480c_zero_exotic.py"),
            ("unmanned_probe_design_*.json", "results/unmanned_probe/"),
            ("docs/480C_UNMANNED_PROBE_IMPLEMENTATION_COMPLETE.md", "docs/implementations/480c_unmanned_probe_complete.md")
        ]
        
        self._organize_file_group(unmanned_probe_files, "Unmanned Probe")
    
    def organize_hull_optimization_files(self):
        """Organize all hull optimization related files."""
        hull_files = [
            ("src/advanced_hull_optimization_framework.py", "src/frameworks/advanced_hull_optimization_framework.py"),
            ("src/naval_architecture_framework.py", "src/frameworks/naval_architecture_framework.py"),
            ("src/advanced_materials_integration.py", "src/core/advanced_materials_integration.py"),
            ("ftl_hull_*.json", "results/hull_optimization/"),
            ("docs/FTL_HULL_DESIGN_IMPLEMENTATION_COMPLETE.md", "docs/implementations/ftl_hull_design_complete.md")
        ]
        
        self._organize_file_group(hull_files, "Hull Optimization")
    
    def organize_uq_files(self):
        """Organize all UQ (Uncertainty Quantification) files."""
        uq_files = [
            ("UQ-TODO.ndjson", "uq_framework/tracking/UQ-TODO.ndjson"),
            ("UQ-TODO-RESOLVED.ndjson", "uq_framework/resolutions/UQ-TODO-RESOLVED.ndjson"),
            ("UQ-HOLODECK-INTEGRATION-COMPLETE.ndjson", "uq_framework/resolutions/UQ-HOLODECK-INTEGRATION-COMPLETE.ndjson"),
            ("UQ_FRAMEWORK_001_RESOLUTION_REPORT.json", "uq_framework/analysis/UQ_FRAMEWORK_001_RESOLUTION_REPORT.json"),
            ("uq_resolution/", "uq_framework/resolutions/"),
            ("casimir_uq_resolution.py", "src/validation/casimir_uq_resolution.py")
        ]
        
        self._organize_file_group(uq_files, "UQ Framework")
    
    def organize_documentation_files(self):
        """Organize all documentation files."""
        doc_files = [
            ("docs/technical-documentation.md", "docs/technical/technical-documentation.md"),
            ("docs/github_repository_settings.md", "docs/technical/github_repository_settings.md"),
            ("docs/index_file_updates_crew_vessel.md", "docs/technical/index_file_updates_crew_vessel.md"),
            ("REPOSITORY_ORGANIZATION_SUMMARY.md", "docs/technical/repository_organization_summary.md"),
            ("CHANGELOG.md", "docs/technical/CHANGELOG.md")
        ]
        
        self._organize_file_group(doc_files, "Documentation")
    
    def organize_test_files(self):
        """Organize all test files."""
        test_files = [
            ("run_tests.py", "tools/validation/run_tests.py"),
            ("tests/test_*.py", "tests/unit/"),
            ("test_results.json", "results/validation_results/test_results.json"),
            ("enhancement_test.log", "results/validation_results/enhancement_test.log")
        ]
        
        self._organize_file_group(test_files, "Testing")
    
    def organize_configuration_files(self):
        """Organize all configuration files."""
        config_files = [
            ("config.yaml", "config/environments/default_config.yaml"),
            ("config/", "config/parameters/"),
            ("requirements.txt", "config/requirements.txt"),
            ("setup.py", "config/setup.py"),
            ("VERSION", "config/VERSION")
        ]
        
        self._organize_file_group(config_files, "Configuration")
    
    def organize_results_and_data(self):
        """Organize all results and data files."""
        results_files = [
            ("advanced_hull_optimization_results.json", "results/hull_optimization/advanced_hull_optimization_results.json"),
            ("integrated_enhancement_results/", "results/enhancement_analysis/"),
            ("demo_output/", "results/demo_outputs/"),
            ("virtual_lab_results/", "results/virtual_lab/"),
            ("validation/", "results/validation_results/")
        ]
        
        self._organize_file_group(results_files, "Results and Data")
    
    def _organize_file_group(self, file_mappings, group_name):
        """Helper method to organize a group of files."""
        print(f"\nOrganizing {group_name} files...")
        
        for source_pattern, destination in file_mappings:
            source_path = self.base_path / source_pattern
            dest_path = self.base_path / destination
            
            try:
                if '*' in source_pattern:
                    # Handle wildcard patterns
                    pattern_path = self.base_path
                    for file_path in pattern_path.glob(source_pattern):
                        if file_path.is_file():
                            dest_file = dest_path / file_path.name
                            dest_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(file_path), str(dest_file))
                            self.organization_log.append(f"Moved: {file_path.name} -> {dest_file}")
                elif source_path.exists():
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    if source_path.is_file():
                        shutil.move(str(source_path), str(dest_path))
                        self.organization_log.append(f"Moved: {source_pattern} -> {destination}")
                    elif source_path.is_dir():
                        shutil.move(str(source_path), str(dest_path))
                        self.organization_log.append(f"Moved directory: {source_pattern} -> {destination}")
                else:
                    self.organization_log.append(f"File not found: {source_pattern}")
                    
            except Exception as e:
                self.organization_log.append(f"Error moving {source_pattern}: {str(e)}")
    
    def create_readme_files(self):
        """Create README files for major directories."""
        readme_content = {
            "src": "# Source Code\n\nCore implementation files for the energy research framework.\n\n## Structure\n- `core/`: Core functionality and base classes\n- `frameworks/`: Complete framework implementations\n- `integrations/`: Cross-repository integration modules\n- `validation/`: Validation and verification code\n- `utils/`: Utility functions and helpers",
            
            "docs": "# Documentation\n\nComprehensive documentation for the energy research framework.\n\n## Structure\n- `technical/`: Technical documentation and specifications\n- `api/`: API documentation and references\n- `tutorials/`: User guides and tutorials\n- `implementations/`: Implementation completion documentation\n- `uq_resolutions/`: Uncertainty quantification resolution docs",
            
            "results": "# Results and Analysis\n\nSimulation results, experimental data, and analysis outputs.\n\n## Structure\n- `crew_vessel/`: Crew vessel design results\n- `unmanned_probe/`: 480c unmanned probe results\n- `hull_optimization/`: Advanced hull optimization results\n- `uq_analysis/`: Uncertainty quantification analysis\n- `validation_results/`: Test and validation results",
            
            "uq_framework": "# Uncertainty Quantification Framework\n\nComprehensive UQ tracking, analysis, and resolution system.\n\n## Structure\n- `resolutions/`: Completed UQ issue resolutions\n- `tracking/`: Active UQ issue tracking\n- `analysis/`: UQ analysis tools and reports"
        }
        
        for directory, content in readme_content.items():
            readme_path = self.base_path / directory / "README.md"
            readme_path.parent.mkdir(parents=True, exist_ok=True)
            with open(readme_path, 'w') as f:
                f.write(content)
            self.organization_log.append(f"Created README: {directory}/README.md")
    
    def generate_organization_report(self):
        """Generate a comprehensive organization report."""
        report = {
            "organization_date": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "operations_performed": len(self.organization_log),
            "organization_log": self.organization_log,
            "directory_structure": self._get_directory_structure(),
            "summary": {
                "directories_created": len([log for log in self.organization_log if "Created directory" in log]),
                "files_moved": len([log for log in self.organization_log if "Moved:" in log]),
                "readmes_created": len([log for log in self.organization_log if "Created README" in log]),
                "errors": len([log for log in self.organization_log if "Error" in log or "not found" in log])
            }
        }
        
        report_path = self.base_path / "docs" / "technical" / "file_organization_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _get_directory_structure(self):
        """Get the current directory structure."""
        structure = {}
        for root, dirs, files in os.walk(self.base_path):
            rel_path = os.path.relpath(root, self.base_path)
            if rel_path == '.':
                rel_path = 'root'
            structure[rel_path] = {
                'directories': dirs,
                'files': files,
                'file_count': len(files)
            }
        return structure
    
    def organize_all(self):
        """Perform complete repository organization."""
        print("Starting comprehensive Energy repository organization...")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Organize file groups
        self.organize_crew_vessel_files()
        self.organize_unmanned_probe_files()
        self.organize_hull_optimization_files()
        self.organize_uq_files()
        self.organize_documentation_files()
        self.organize_test_files()
        self.organize_configuration_files()
        self.organize_results_and_data()
        
        # Create documentation
        self.create_readme_files()
        
        # Generate report
        report = self.generate_organization_report()
        
        print(f"\nOrganization complete! {report['summary']['files_moved']} files moved, {report['summary']['directories_created']} directories created.")
        print(f"Report saved to: docs/technical/file_organization_report.json")
        
        return report

if __name__ == "__main__":
    # Example usage
    organizer = EnergyRepositoryOrganizer("/path/to/energy/repository")
    report = organizer.organize_all()
    
    print("\nOrganization Summary:")
    print(f"Files moved: {report['summary']['files_moved']}")
    print(f"Directories created: {report['summary']['directories_created']}")
    print(f"READMEs created: {report['summary']['readmes_created']}")
    print(f"Errors: {report['summary']['errors']}")
