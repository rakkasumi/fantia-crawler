import argparse
import os
from crawler import FantiaCrawler

def main():
    parser = argparse.ArgumentParser(description="Fantia Metadata Crawler")
    parser.add_argument('-e', '--email', 
                        default='', 
                        help='Fantia account email')
    parser.add_argument('-p', '--password', 
                        default='', 
                        help='Fantia account password')
    parser.add_argument('-b', '--browser', 
                        default='chrome', 
                        help='The browser driver to use')
    parser.add_argument('-d', '--directory', 
                        default=os.getcwd(), 
                        help='Directory to process videos (default: current directory)')
    
    parser.add_argument('-x', '--prefix',
                        default='',
                        help='Prefix to add to organized files. e.g., "FANTIA-" result "FANTIA-[ID]" in  (default: empty)')

    args = parser.parse_args()

    try:
        crawler = FantiaCrawler(email=args.email, password=args.password, working_directory=args.directory,
                                driver=args.browser, prefix=args.prefix)
        crawler.process_videos()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
