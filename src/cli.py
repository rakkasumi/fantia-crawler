import argparse
import os
from crawler import FantiaCrawler

def main():
    parser = argparse.ArgumentParser(description="Fantia Metadata Crawler")
    parser.add_argument('-e', '--email',
                        default='',
                        help='Autofill Fantia account email, if empty you may need to enter it manually')
    parser.add_argument('-p', '--password',
                        default='',
                        help='Autofill Fantia account password, if empty you may need to enter it manually')
    parser.add_argument('-b', '--browser',
                        default='chrome',
                        help='The browser driver to use (default: chrome)')
    parser.add_argument('-d', '--directory',
                        default=os.getcwd(),
                        help='Directory to process videos (default: current directory). If you are using Windows, it is recommended to surround the path with double quotes.')
    parser.add_argument('-x', '--prefix',
                        default='',
                        help='Prefix to add to organized files. e.g., "FANTIA-" result "FANTIA-[ID]" in  (default: empty)')
    parser.add_argument('-r', '--replace-space',
                        default=False,
                        help='Replace spaces with hyphens (-) before file parts (default: false)')

    args = parser.parse_args()

    try:
        crawler = FantiaCrawler(email=args.email, password=args.password, working_directory=args.directory,
                                driver=args.browser, prefix=args.prefix, replace_space=args.replace_space)
        crawler.process_videos()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
