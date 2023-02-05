def search_file(name, logger):
    import os
    import os.path

    matches = []
    for dirpath, dirnames, filenames in os.walk('.'):
        if name in filenames:
            matches.append(os.path.join(dirpath, name))
    if len(matches) > 1:
        logger.info("More than one file matches specified name,\
               only returning first match")
    return matches[0]

def read_XML(file_path):
    from bs4 import BeautifulSoup

    content = []
    # Read the XML file
    with open(file_path, "r") as f:
        # Read each line in the file, readlines() returns a list of lines
        content = f.readlines()
        # Combine the lines in the list into a string
        content = "".join(content)
        soup = BeautifulSoup(content, features="xml")
        return soup

def run_parser(desired_file):
    import logging 

    # Initialize logger
    logger = logging.getLogger("parser")
    logger.setLevel(logging.DEBUG)
    # Create a file handler to log the messages.
    log_file = "./logs/parser.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    # Create a console handler with a higher log level.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    # Modify the handlers log format to your convenience.
    handler_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(handler_format)
    console_handler.setFormatter(handler_format)
    # Finally, add the handlers to the logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Search for file
    try:
        file_path = search_file(desired_file, logger)

    except IndexError:
        logger.error("Filename does not exist")
        desired_file = input("Please enter valid filename: ")
        return run_parser(desired_file)
    
    # Parse file to soup object
    soup = read_XML(file_path)
    print(soup)

if __name__ == '__main__':
    import sys

    arguments = sys.argv
    desired_file = str(arguments[-1])
    run_parser(desired_file=desired_file)
