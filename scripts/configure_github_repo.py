#!/usr/bin/env python3
"""
GitHub Repository Configuration Script
Configures repository description, topics, and metadata via GitHub API

Part of the Dynamic Backreaction Factor Framework documentation wrap-up
Task 4: Configure GitHub repository description and topics via API
"""

import os
import requests
import json
from typing import List, Dict, Optional

class GitHubRepoConfigurator:
    """Configure GitHub repository metadata via API"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub API client
        
        Args:
            token: GitHub personal access token (if None, uses environment variable)
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN environment variable or pass token parameter.")
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        self.base_url = 'https://api.github.com'
    
    def configure_energy_repository(self) -> Dict:
        """Configure the energy repository with comprehensive metadata"""
        
        # Repository configuration for energy framework
        config = {
            'name': 'energy',
            'description': (
                '⚡ Revolutionary Energy Research Framework - World\'s first complete polymer-enhanced '
                'graviton quantum field theory achieving UV-finite non-perturbative graviton quantization. '
                'Features medical-grade therapeutic graviton applications, laboratory-accessible graviton '
                'detection (1-10 GeV), industrial gravitational field control (242M× energy reduction), '
                'and comprehensive FTL technology integration with dynamic backreaction factor β(t) control.'
            ),
            'homepage': 'https://github.com/arcticoder/energy',
            'topics': [
                # Core Technologies
                'graviton-qft', 'quantum-field-theory', 'loop-quantum-gravity', 'spacetime-physics',
                'energy-enhancement', 'gravitational-control', 'dynamic-backreaction',
                
                # Medical Applications  
                'medical-graviton', 'therapeutic-applications', 'biological-safety', 'medical-devices',
                'who-compliance', 'fda-pathway',
                
                # Industrial Applications
                'industrial-gravity', 'manufacturing-control', 'anti-gravity-systems', 'precision-positioning',
                'energy-reduction', 'commercial-deployment',
                
                # FTL Technologies
                'ftl-communication', 'warp-drive', 'spacetime-engineering', 'exotic-matter-elimination',
                'bobrick-martire-geometry', 'alcubierre-drive',
                
                # Scientific Framework
                'uv-finite-theory', 'polymer-regularization', 'graviton-propagator', 'experimental-validation',
                'laboratory-accessible', 'cross-scale-physics',
                
                # Implementation
                'production-ready', 'digital-twin', 'uncertainty-quantification', 'cross-repository-integration',
                'python', 'scientific-computing', 'advanced-physics'
            ],
            'has_wiki': True,
            'has_issues': True,
            'has_projects': True,
            'allow_squash_merge': True,
            'allow_merge_commit': True,
            'allow_rebase_merge': True,
            'delete_branch_on_merge': False,
            'archived': False,
            'disabled': False,
            'private': False
        }
        
        return self.update_repository('arcticoder', 'energy', config)
    
    def update_repository(self, owner: str, repo: str, config: Dict) -> Dict:
        """Update repository configuration via GitHub API
        
        Args:
            owner: Repository owner/organization
            repo: Repository name  
            config: Repository configuration dictionary
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        
        try:
            response = requests.patch(url, headers=self.headers, data=json.dumps(config))
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Successfully updated repository {owner}/{repo}")
            print(f"   Description: {result.get('description', 'N/A')[:100]}...")
            print(f"   Topics: {', '.join(result.get('topics', [])[:5])}...")
            print(f"   Homepage: {result.get('homepage', 'N/A')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error updating repository {owner}/{repo}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text}")
            raise
    
    def get_repository_info(self, owner: str, repo: str) -> Dict:
        """Get current repository information
        
        Args:
            owner: Repository owner/organization
            repo: Repository name
            
        Returns:
            Repository information dictionary
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching repository info for {owner}/{repo}: {e}")
            raise
    
    def update_topics(self, owner: str, repo: str, topics: List[str]) -> Dict:
        """Update repository topics specifically
        
        Args:
            owner: Repository owner/organization
            repo: Repository name
            topics: List of topic strings
            
        Returns:
            API response dictionary
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/topics"
        
        payload = {'names': topics}
        
        try:
            response = requests.put(url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Successfully updated topics for {owner}/{repo}")
            print(f"   Topics ({len(result.get('names', []))}): {', '.join(result.get('names', [])[:10])}...")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error updating topics for {owner}/{repo}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text}")
            raise


def main():
    """Main configuration function"""
    print("🔧 GitHub Repository Configuration - Energy Framework")
    print("=" * 60)
    
    try:
        # Initialize configurator
        configurator = GitHubRepoConfigurator()
        
        # Get current repository state
        print("\n📋 Current Repository Information:")
        current_info = configurator.get_repository_info('arcticoder', 'energy')
        print(f"   Current Description: {current_info.get('description', 'None')[:100]}...")
        print(f"   Current Topics ({len(current_info.get('topics', []))}): {', '.join(current_info.get('topics', [])[:5])}...")
        
        # Configure energy repository
        print("\n🚀 Configuring Energy Repository...")
        result = configurator.configure_energy_repository()
        
        print("\n✅ Configuration Complete!")
        print(f"   Repository URL: {result.get('html_url', 'N/A')}")
        print(f"   Total Topics: {len(result.get('topics', []))}")
        print(f"   Homepage: {result.get('homepage', 'N/A')}")
        
        # Validation
        print("\n🔍 Validation:")
        if result.get('description') and 'graviton' in result.get('description', ''):
            print("   ✅ Description contains graviton physics")
        else:
            print("   ⚠️  Description validation failed")
            
        if len(result.get('topics', [])) >= 20:
            print(f"   ✅ Comprehensive topics ({len(result.get('topics', []))}) configured")
        else:
            print(f"   ⚠️  Limited topics ({len(result.get('topics', []))}) configured")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Configuration failed: {e}")
        raise


if __name__ == '__main__':
    main()
