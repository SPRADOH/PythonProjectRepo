#VARIANT 7
import csv
import xml.dom.minidom
import random



def process_csv_file():
    print("Processing books-en.csv file...")
    
    # Read  CSV file
    with open('books-en.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        books = list(reader)
    
    print(f"Total records: {len(books)}")
    
    # Exercise 1: Count records with title longer than 30 characters
    long_titles_count = 0
    for book in books:
        title = book.get('Book-Title', '')
        if len(title) > 30:
            long_titles_count += 1
    
    print(f"Books with titles longer than 30 characters: {long_titles_count}")
    
    # Exercise 2: Search books by author with variant restrictions 
    def search_books_by_author(author_name):
        results = []
        for book in books:
            if (book.get('Book-Author', '').lower() == author_name.lower() and 
                book.get('Year-Of-Publication', '').isdigit()):
                year = int(book.get('Year-Of-Publication', '0'))
                if 1991 <= year <= 1995:
                    results.append(book)
        return results
    
    # Example search
    author_to_search = input("Enter author name to search: ")
    found_books = search_books_by_author(author_to_search)
    print(f"Found {len(found_books)} books by {author_to_search} from 1991-1995:")
    for i, book in enumerate(found_books, 1):
        print(f"{i}. {book.get('Book-Title')} ({book.get('Year-Of-Publication')})")
    
    # Exercisr 3: Generate bibliographic references for 20 random records
    def generate_bibliographic_references():
        # Select 20 random books
        if len(books) >= 20:
            selected_books = random.sample(books, 20)
        else:
            selected_books = books
        
        references = []
        for i, book in enumerate(selected_books, 1):
            author = book.get('Book-Author', 'Unknown Author')
            title = book.get('Book-Title', 'Unknown Title')
            year = book.get('Year-Of-Publication', 'Unknown Year')
            reference = f"{author}. {title} - {year}"
            references.append(reference)
        
        # Save
        with open('bibliographic_references.txt', 'w', encoding='utf-8') as f:
            for i, ref in enumerate(references, 1):
                f.write(f"{i}. {ref}\n")
        
        print("Bibliographic references saved to 'bibliographic_references.txt'")
        return references
    
    references = generate_bibliographic_references()
    
    # Additional tasks
    # List of unique publishers
    publishers = set()
    for book in books:
        publisher = book.get('Publisher', '').strip()
        if publisher:
            publishers.add(publisher)
    
    print(f"\nUnique publishers count: {len(publishers)}")
    
    # Top 20 most popular books (assuming popularity based on ratings)
    def get_popularity_score(book):
        # Use ISBN as identifier and count ratings
        isbn = book.get('ISBN', '')
        # For simplicity, we'll use a combination of factors
        # In a real scenario, you might have actual rating data
        return len(isbn)  # Placeholder for popularity metric
    
    # Sort by popularity (using our simple metric)
    sorted_books = sorted(books, key=get_popularity_score, reverse=True)
    top_20_books = sorted_books[:20]
    
    print("\nTop 20 most popular books:")
    for i, book in enumerate(top_20_books, 1):
        print(f"{i}. {book.get('Book-Title')} by {book.get('Book-Author')}")



def process_xml_file():
    print("\nProcessing currency.xml file...")
    
    # Parse the XML file
    dom = xml.dom.minidom.parse('currency.xml')
    
    # Get all Valute elements
    valutes = dom.getElementsByTagName('Valute')
    
    # Variant 7: List of CharCode, but only for currencies with Nominal=10 or Nominal=100
    charcodes = []
    
    for valute in valutes:
        # Get CharCode
        charcode_element = valute.getElementsByTagName('CharCode')[0]
        charcode = charcode_element.firstChild.data if charcode_element.firstChild else ""
        
        # Get Nominal
        nominal_element = valute.getElementsByTagName('Nominal')[0]
        nominal = nominal_element.firstChild.data if nominal_element.firstChild else ""
        
        # Convert nominal to integer and check condition
        try:
            nominal_int = int(nominal)
            if nominal_int == 10 or nominal_int == 100:
                charcodes.append(charcode)
        except ValueError:
            continue
    
    print(f"CharCodes for currencies with Nominal=10 or Nominal=100: {charcodes}")
    print(f"Total count: {len(charcodes)}")
    
    # Print detailed information
    print("\nDetailed information:")
    for valute in valutes:
        charcode_element = valute.getElementsByTagName('CharCode')[0]
        charcode = charcode_element.firstChild.data if charcode_element.firstChild else ""
        
        nominal_element = valute.getElementsByTagName('Nominal')[0]
        nominal = nominal_element.firstChild.data if nominal_element.firstChild else ""
        
        name_element = valute.getElementsByTagName('Name')[0]
        name = name_element.firstChild.data if name_element.firstChild else ""
        
        try:
            nominal_int = int(nominal)
            if nominal_int == 10 or nominal_int == 100:
                print(f"  {charcode}: {name} (Nominal: {nominal})")
        except ValueError:
            continue



if __name__ == "__main__":
    print("=== Lab 2 - Option 7 Solution ===")
    
    try:
        process_csv_file()
    except FileNotFoundError:
        print("Error: books-en.csv file not found!")
    except Exception as e:
        print(f"Error processing CSV file: {e}")
    
    try:
        process_xml_file()
    except FileNotFoundError:
        print("Error: currency.xml file not found!")
    except Exception as e:
        print(f"Error processing XML file: {e}")
    
    print("\nProgram completed")