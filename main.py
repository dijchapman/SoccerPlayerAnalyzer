import fbrefscraper
import wyscoutanalyser


def main():
    analyser_type = input('Select analysing type (wyscout or fbref): ')
    if analyser_type == 'wyscout':
        wyscoutanalyser.main()
    elif analyser_type == 'fbref':
        fbrefscraper.main()


if __name__ == "__main__":
    # calling main function
    main()
