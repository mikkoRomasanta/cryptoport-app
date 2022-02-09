import token_api
import googlesheet


def main():
    '''Main application'''
    quotes = token_api.get_quotes()
    res = googlesheet.send_to_sheet(quotes)
    
    return res
    
if __name__ == '__main__':
    main()