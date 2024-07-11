import os
from github import Github

def upload_data(df, file_path):
    owner = 'laytonprend'
    access_token = os.getenv('GITHUB_PAT')
    branch_name = 'main'  # Replace with your desired branch name
    repo = 'POS-Solution'
    repo_name = f'{owner}/{repo}'
    
    # Initialize PyGithub with your access token
    g = Github(access_token)
    
    # Get the repository
    repo = g.get_repo(repo_name)
    
    # Convert DataFrame to CSV string
    df_content = df.to_csv(index=False)
    
    # Fetch existing file if it exists
    try:
        existing_file = repo.get_contents(file_path, ref=branch_name)
        existing_sha = existing_file.sha
    except Exception as e:
        existing_sha = None
        print(f"File {file_path} does not exist yet in branch {branch_name}. Creating new file...")
    
    # Commit message
    commit_message = f"Updating {file_path} data"
    
    # Update or create the file
    try:
        if existing_sha:
            repo.update_file(file_path, commit_message, df_content, sha=existing_sha, branch=branch_name)
            print(f'File "{file_path}" updated in the repository')
        else:
            repo.create_file(file_path, commit_message, df_content, branch=branch_name)
            print(f'File "{file_path}" created in the repository')
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# df is your DataFrame containing data to upload
# file_path is the path to the file in your repository, e.g., 'data/transactions.csv'
# upload_data(df, 'data/transactions.csv')

