import argparse
import os
try:
    from importlib.metadata import version
except ImportError:
    # Python < 3.8
    from importlib_metadata import version
from crawler import FantiaCrawler

def get_version():
    """Get version using importlib.metadata"""
    try:
        return version('fantia-crawler')
    except Exception:
        return 'unknown'

def main():
    parser = argparse.ArgumentParser(description="Fantia Metadata Crawler")
    parser.add_argument('-v', '--version', action='version', 
                        version=f"Fantia Crawler {get_version()}")
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
    parser.add_argument('-D', '--dash',
                        default='-', dest='dash',
                        help='Define the default hypen between prefix, id and parts, default `-`')
    parser.add_argument('--emby-jellyfin-support', 
                        action='store_true',
                        default=False,
                        help='Enable Emby/Jellyfin support (creating backdrop.jpg, landscape.jpg, folder.jpg, movie.nfo)')

    args = parser.parse_args()

    try:
        crawler = FantiaCrawler(email=args.email, password=args.password, working_directory=args.directory,
                                driver=args.browser, prefix=args.prefix, dash=args.dash,
                                emby_jellyfin_support=args.emby_jellyfin_support)
        crawler.process_videos()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()