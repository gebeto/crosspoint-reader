import requests
import os
import zipfile
import io

def download_bun_release(asset_name_filter, download_path='.'):
    """
    Downloads the latest Bun release asset matching the filter from GitHub.
    
    Args:
        asset_name_filter (str): Substring to filter the asset name (e.g., 'linux-x64').
        download_path (str): Directory where the file will be saved.
    """
    api_url = f"https://api.github.com/repos/oven-sh/bun/releases/latest"
    
    # Use requests to fetch the latest release info
    response = requests.get(api_url)
    # response.raise_for_status() # Raise an exception for bad status codes
    release_info = response.json()
    
    # Find the asset that matches the filter
    asset_url = None
    asset_name = None
    for asset in release_info['assets']:
        if asset_name_filter + ".zip" == asset['name']:
            asset_url = asset['url']
            asset_name = asset['name']
            break
    
    if not asset_url:
        print(f"Could not find a matching asset for filter: {asset_name_filter}")
        return

    # Define the local file path
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    local_path = os.path.join(download_path, asset_name)
    
    print(f"Downloading {asset_name} to {local_path}...")

    # Download the asset with proper headers for GitHub API binary download
    # The 'Accept: application/octet-stream' header is crucial for direct binary downloads
    headers = {'Accept': 'application/octet-stream'}
    asset_response = requests.get(asset_url, headers=headers)
    file = io.BytesIO(asset_response.content)
    # asset_response.raise_for_status()
    z = zipfile.ZipFile(file, mode="r")
    print(z.namelist())
    z.extract(f"{asset_name_filter}/bun", path="./.pio")
    
    with open(local_path, 'wb') as f:
        f.write(asset_response.content)
    #     for chunk in asset_response.iter_content(chunk_size=8192):
    #         f.write(chunk)
            
    print("Download complete!")
    print(f"File saved at: {os.path.abspath(local_path)}")

# --- Example Usage ---
# For Linux x64:
# download_bun_release(asset_name_filter='linux-x64', download_path='./bun_downloads')

# For macOS (Darwin) x64 (Intel):
# download_bun_release(asset_name_filter='darwin-x64', download_path='./bun_downloads')

# For Windows (adjust filter based on exact asset names in releases):
# download_bun_release(asset_name_filter='windows-x64', download_path='./bun_downloads')

# Example for the current system (you might need to refine the filter)
# This example uses a common filter for musl-based Linux distributions
download_bun_release(asset_name_filter='bun-darwin-aarch64', download_path='./.pio')
