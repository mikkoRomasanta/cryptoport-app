import token_api
import googlesheet
import schedule
import time


def main():
    '''Main application'''
    quotes = token_api.get_quotes()
    res = googlesheet.send_to_sheet(quotes)
    
    return res

def scheduler():
    '''Runs the app in set intervals'''
    schedule.every(290).seconds.do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(10)
    
if __name__ == '__main__':
    main()
    # scheduler()
    
    
