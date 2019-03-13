import os
import DB_Insert as db

def searcharticles():
    print("Voer zoekterm in:")

    keyword = ' '

    keyword = input("Zoekterm...")

    conn = db.connect_to_db()
    results = db.selectsearch(conn, keyword)
    for row in results:
        print(str(row)+'\n')



def main():
    searcharticles()


if __name__ == '__main__':
    main()
