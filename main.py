import os
import subprocess
import sys

from tqdm import tqdm

def download_website(url, output_dir, max_size=None):
    file_name = None
    # Create the output directory if it doesn't exist
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
        command += ['--continue', '--progress=dot:mega', '-o', '/dev/null',
                    '-c', '-T', '10', '-t', '0', '-i', resume_file, url]
    else:
        # Otherwise, start a new download
        command += ['--progress=dot:mega', '-o', '/dev/null', url]

    # file_name = None

    try:
        # Execute the wget command, displaying a progress bar
        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              bufsize=1, universal_newlines=True) as process:
            total_size = 0
            for line in process.stdout or []:
                # Parse the output of wget to update the progress bar
                if line.startswith('Length:'):
                    total_size = int(line.split()[1])
                elif line.startswith('Saving to:'):
                    file_name = line.split()[2]
                elif line.startswith('Progress:'):
                    progress = int(line.split()[1][:-1])
                    if total_size > 0:
                        pbar.update(progress)

            # Write the resume file if the download was successful
            if process.returncode == 0:
                if os.path.exists(resume_file):
                    os.remove(resume_file)
                pbar.close()
                print(f"Website downloaded successfully to {output_dir}")
            else:
                if file_name is not None:
                    with open(resume_file, 'w') as f:
                        f.write(file_name)
                print("Website download failed. Use the same command to resume download from where it stopped")
    except subprocess.CalledProcessError as e:
        print("Website download failed. Error:", e)
        if os.path.exists(resume_file):
            os.remove(resume_file)


if __name__ == '__main__':
    url = input("Enter website URL: ")
    output_dir = '/home/jhembe/localWebSites'
    max_size = input("Enter maximum size (in MB) to download (optional): ")

    if max_size is not None:
        max_size = f"{int(max_size) * 1024 * 1024}"

    with tqdm(total=100) as pbar:
        download_website(url, output_dir, max_size)
