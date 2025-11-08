#!/usr/bin/env python3

import os
import subprocess
import sys

def deploy_to_production(branch='main'):
    try:
        # Assume git is initialized
        subprocess.run(['git', 'checkout', branch], check=True)
        subprocess.run(['git', 'pull'], check=True)
        # Example: run build script if exists
        if os.path.exists('build.sh'):
            subprocess.run(['bash', 'build.sh'], check=True)
        # Push to production (customize as needed)
        subprocess.run(['git', 'push', 'origin', branch], check=True)
        print(f"Successfully deployed branch {branch} to production.")
    except subprocess.CalledProcessError as e:
        print(f"Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    branch = sys.argv[1] if len(sys.argv) > 1 else 'main'
    deploy_to_production(branch)