import os
import re
import shutil
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from PIL import Image
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FantiaCrawler:

    def __init__(self,
                 email,
                 password,
                 working_directory=None,
                 driver='chrome'):
        """
        Initialize the Fantia Crawler
        
        :param email: Fantia account email
        :param password: Fantia account password
        :param working_directory: Directory to process videos (defaults to current directory)
        """
        self.email = email
        self.password = password
        self.working_directory = working_directory or os.getcwd()
        self.history_file = os.path.join(self.working_directory,
                                         'finished.log')
        # Init web driver
        if driver.lower() == 'edge':
            self.driver = webdriver.Edge()
        elif driver.lower() == 'firefox':
            self.driver = webdriver.Firefox()
        elif driver.lower() == 'safari':
            self.driver = webdriver.Safari()
        else:
            self.driver = webdriver.Chrome()
        # Ensure images directory exists
        os.makedirs(os.path.join(self.working_directory, 'images'),
                    exist_ok=True)

    def login(self):
        """
        Log in to Fantia website
        """
        self.driver.get("https://fantia.jp/?locale=zh-cn")
        self.driver.implicitly_wait(5)
        self.driver.get("https://fantia.jp/sessions/signin")
        # Wait for email input
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_email")))
        email_input.send_keys(self.email)

        # Wait for password input
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_password")))
        password_input.send_keys(self.password)

        # Find and click login button
        # login_button = WebDriverWait(self.driver, 20).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary[type='submit']"))
        # )
        input("When you log in successfully, press Enter to continue")

        # Wait for page change
        WebDriverWait(self.driver,
                      10).until(EC.url_changes("https://fantia.jp"))

    def get_history(self):
        """
        Retrieve processing history from log file
        
        :return: List of processed post IDs
        """
        try:
            with open(self.history_file, 'r') as f:
                history = f.readlines()
            return [e.strip() for e in history]
        except IOError:
            return []

    def find_matching_videos(self, history):
        """
        Find video files that haven't been processed
        
        :param history: List of previously processed post IDs
        :return: List of unprocessed video files
        """
        matching_files = []
        pattern = r"\d{4,}"

        for root, _, files in os.walk(self.working_directory):
            for file in files:
                # Match videos with 4+ digit numbers
                match = re.findall(pattern, file)
                if match and (file.endswith('.mp4') or file.endswith('.mov')):
                    # Check for multi-part videos
                    part_match = re.search(r'(CD\d+|part\d+)', file,
                                           re.IGNORECASE)

                    file_info = {
                        'id': match[0],
                        'path': os.path.join(root, file)
                    }

                    if part_match:
                        file_info['part'] = part_match.group(0)

                    if match[0] not in history:
                        matching_files.append(file_info)

        return matching_files

    def get_fantia_post_data(self, post_id, video_path):
        """
        Retrieve metadata for a Fantia post
        
        :param post_id: ID of the Fantia post
        :param video_path: Path to the source video file
        :return: Dictionary of post metadata
        """
        self.driver.implicitly_wait(10)
        self.driver.get(f"https://fantia.jp/posts/{post_id}")

        title = self._get_post_title()
        image = self._get_post_thumbnail(post_id,
                                         video_path)  # Pass video_path here
        author = self._get_post_club()
        post_date = self._get_post_date()
        tags = self._get_post_tags()
        content = self._get_post_description()

        return {
            'id': post_id,
            'title': title,
            'image': image,
            'author': author,
            'content': content,
            'post_date': post_date,
            'tags': tags
        }

    def _get_post_title(self):
        """Get the post title"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h1.post-title.mb-10")))
        print(element.text)
        return element.text

    def _get_post_thumbnail(self, post_id, video_path):
        """
        Download or use existing thumbnail image
        
        :param post_id: ID of the Fantia post
        :param video_path: Path to the source video file
        :return: Path to the saved thumbnail image
        """
        # Get video directory and base name
        video_dir = os.path.dirname(video_path)
        video_base_name = os.path.splitext(os.path.basename(video_path))[0]

        # Prepare save path for thumbnail
        save_path = f"./images/{post_id}.jpg"
        os.makedirs('images', exist_ok=True)

        # Check for existing matching image in video directory
        all_files = os.listdir(video_dir)
        matching_image = None

        for file_name in all_files:
            file_base, file_ext = os.path.splitext(file_name)
            # Check if filename contains video base name and is an image
            if (video_base_name in file_base and file_ext.lower()
                    in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']):
                matching_image = os.path.join(video_dir, file_name)
                break

        if matching_image:
            # If matching image found, copy it to the images directory
            print(f"Found matching image: {matching_image}")
            shutil.copy(matching_image, save_path)
            return save_path

        # If no matching image, download from Fantia
        img = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.post-thumbnail img")))
        img_url = img.get_attribute("src")

        # Use session to maintain cookies
        cookies = self.driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = session.get(img_url, headers=headers, stream=True)
        response.raise_for_status()

        try:
            image = Image.open(BytesIO(response.content))
            if image.format != 'JPEG':
                print(f"Converting {image.format} to JPEG")
                image = image.convert('RGB')
                image.save(save_path, 'JPEG', quality=90)
            else:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Failed to process the image: {e}")
            raise

        return save_path

    def _get_post_description(self):
        """Get post description based on sibling structure."""
        self.driver.implicitly_wait(1)
        try:
            thumbnail_div = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "post-thumbnail.bg-gray.mt-30.mb-30")))
            sibling_div = thumbnail_div.find_element(By.XPATH,
                                                     "following-sibling::div")

            try:
                description = sibling_div.find_element(By.CLASS_NAME,
                                                       "wysiwyg.mb-30")
                html_content = description.get_attribute("innerHTML")
            except Exception:
                description = sibling_div.find_element(
                    By.CSS_SELECTOR,
                    "div.ql-container.ql-snow.ql-disabled div.ql-editor")
                html_content = description.get_attribute("innerHTML")

            # 清理 HTML 并返回结果
            html_content = re.sub(r'(<br\s*/?>\s*){2,}', '<br>', html_content)
            return html_content.replace('<br>', os.linesep)

        except Exception as e:
            print(f"Failed to fetch post description: {e}")
            return ''

    def _get_post_club(self):
        """Get fanclub/author name"""
        h1_anchor = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h1.fanclub-name a")))
        return h1_anchor.text.strip()

    def _get_post_date(self):
        """Get post publication date"""
        date_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "small.post-date.text-muted span")))
        date_text = date_element.text.strip()
        return datetime.strptime(date_text, "%Y/%m/%d %H:%M")

    def _get_post_tags(self):
        """Get post tags"""
        anchor_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.btn.btn-xs.btn-default.mr-5.mb-5")))
        tags = []
        for anchor in anchor_elements:
            try:
                title = anchor.get_attribute("title")
                if title:
                    tags.append(title.strip())
            except Exception as e:
                print(f"Error extracting title attribute: {e}")
        return tags

    def generate_nfo(self, metadata):
        """
        Generate NFO file for the video
        
        :param metadata: Dictionary of post metadata
        :return: XML string for NFO file
        """
        movie = ET.Element("movie")

        # Add sub-elements
        plot = ET.SubElement(movie, "plot")
        plot.text = metadata['content']

        title_element = ET.SubElement(movie, "title")
        title_element.text = f"{metadata['id']} {metadata['title']}"

        originaltitle = ET.SubElement(movie, "originaltitle")
        originaltitle.text = metadata['title']

        year = ET.SubElement(movie, "year")
        year.text = metadata['post_date'].strftime("%Y")

        premiered = ET.SubElement(movie, "premiered")
        premiered.text = metadata['post_date'].strftime("%Y-%m-%d")

        releasedate = ET.SubElement(movie, "releasedate")
        releasedate.text = metadata['post_date'].strftime("%Y-%m-%d")

        # Add tags as genres
        for tag in metadata['tags']:
            genre = ET.SubElement(movie, "genre")
            genre.text = tag

        studio = ET.SubElement(movie, "studio")
        studio.text = metadata['author']

        return ET.tostring(movie, encoding="utf-8",
                           xml_declaration=True).decode("utf-8")

    def organize_video(self, video_file, metadata):
        """
        Organize video file with associated files
        
        :param video_file: Path to the video file
        :param metadata: Dictionary of post metadata
        """
        # Create post-specific directory
        movie_path = os.path.join(self.working_directory, metadata['id'])
        os.makedirs(movie_path, exist_ok=True)

        # Prepare file names
        file_base = metadata['id']
        if video_file.get('part'):
            file_base = f"{metadata['id']} {video_file['part']}"

        # Write NFO file
        nfo_content = self.generate_nfo(metadata)
        with open(os.path.join(movie_path, f"{file_base}.nfo"),
                  'w',
                  encoding='utf-8') as f:
            f.write(nfo_content)

        # Copy thumbnail
        shutil.copyfile(metadata['image'],
                        os.path.join(movie_path, f"{file_base}.jpg"))

        # Move video file
        try:
            os.rename(video_file['path'],
                      os.path.join(movie_path, f"{file_base}.mp4"))
        except FileExistsError:
            print(f"Skipping file {video_file['path']} as it already exists.")

    def update_history(self, processed_ids):
        """
        Update the processing history log
        
        :param processed_ids: List of processed post IDs
        """
        with open(self.history_file, 'a', newline='', encoding='utf-8') as f:
            for post_id in processed_ids:
                f.write(post_id + os.linesep)

    def process_videos(self):
        """
        Main method to process unprocessed videos
        """
        try:
            # Get processing history
            history = self.get_history()
            # Find unprocessed videos
            matching_files = self.find_matching_videos(history)

            if matching_files:
                print(
                    f"Ready to fetch metadata for {len(matching_files)} files ...")
                # Log in
                self.login()
                # Process each video
                processed_ids = []

                for video_file in matching_files:
                    try:
                        # Get post metadata, passing the video path
                        metadata = self.get_fantia_post_data(
                            video_file['id'], video_file['path'])

                        # Organize video and associated files
                        self.organize_video(video_file, metadata)

                        # Track processed IDs
                        processed_ids.append(video_file['id'])
                    except Exception as e:
                        print(f"Error processing video {video_file['path']}: {e}")

                # Update history log
                self.update_history(processed_ids)

        except Exception as e:
            print(f"An error occurred during video processing: {e}")
        finally:
            # Always close the browser
            self.teardown()

    def teardown(self):
        """
        Close the browser
        """
        if self.driver:
            self.driver.quit()
