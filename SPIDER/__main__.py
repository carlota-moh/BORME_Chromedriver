if __name__ == '__main__':
    import sys
    import os
    import logging
    from utils import dir_maker
    from spider import run_spider

    arguments = sys.argv

    if "MAIN" in arguments:
        input_date = str(arguments[-1])
    
        # Reformat date appropriately
        YYYY = input_date[:4]
        MM = input_date[4:6]
        DD = input_date[-2:]
        date = MM+DD+YYYY

        # Create downloads directory
        download_name = 'downloads'
        dir_maker(download_name)
        download_dir = os.getcwd()+'/'+download_name+'/'

        # url
        url = 'https://www.boe.es/diario_borme/'

        # run spider
        run_spider(default_download_dir=download_dir, date=date, url=url)
        logger = logging.getLogger("spider.spider")
        logger.info("Successfully run spider for %s" % input_date)

    if "EXTRA" in arguments:
        from XMLparser import run_parser

        desired_file = input("Please enter name of XML file to parse: ")
        run_parser(desired_file=desired_file)
        logger = logging.getLogger("parser.parser")
        logger.info("Successfully run parser")