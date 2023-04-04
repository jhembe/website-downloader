import os
import subprocess
import sys
import getpass

from tqdm import tqdm

def download_website(url, max_size=None):
    file_name = None
    # Get current user's username
    user_name = getpass.getuser()
    # Create the output directory if it doesn't exist
    output_dir = f'/home/{user_name}/localWebSites'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Determine the output file to use for resuming the download
    resume_file = os.path.join(output_dir, '.wget-resume')

    # Set up the wget command with the appropriate options
    command = ['wget', '--recursive', '--page-requisites', '--html-extension',
               '--convert-links', '--no-parent', '-P', output_dir]

    if max_size is not None:
        command += ['--quota', max_size]

    if os.path.exists(resume_file):
        # If the resume file exists, try to resume the download
        command += ['--continue', '--progress=dot:mega', '-c', '-T', '10', '-t', '0', '-i', resume_file, url]
    else:
        # Otherwise, start a new download
        command += ['--progress=dot:mega', url]

    total_size = 0

    try:
        # Execute the wget command, displaying a progress bar
        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              bufsize=1, universal_newlines=True) as process:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for line in process.stdout or []:
                    # Parse the output of wget to update the progress bar
                    if line.startswith('Length:'):
                        total_size = int(line.split()[1])
                        pbar.total = total_size
                    elif line.startswith('Saving to:'):
                        file_name = line.split()[2]
                    elif line.startswith('Progress:'):
                        progress = int(line.split()[1][:-1])
                        if total_size > 0:
                            pbar.update(progress - pbar.n)

                # Write the resume file if the download was successful
                if process.returncode == 0:
                    if os.path.exists(resume_file):
                        os.remove(resume_file)
                    pbar.close()
                    print(f"Website downloaded successfully to {output_dir}")

    except subprocess.CalledProcessError as e:
        print("Website download failed. Error:", e)
        if os.path.exists(resume_file):
            os.remove(resume_file)

if __name__ == '__main__':
    url = input("Enter website URL: ")
    max_size = input("Enter maximum size (in MB) to download (optional): ")

    if max_size is not None:
        max_size = f"{int(max_size) * 1024 * 1024}"

    download_website(url, max_size)
