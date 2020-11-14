"""
I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""

"""
bookrecs.py is the glorious program that'll make your wildest dreams come true. At least someone's dreams I guess. What it does it take
a list of books, and a list of how much an indiviual likes those books. It uses those to see how alike different people are, and then 
recommends books for others to read based off how the person most like them likes their novels.
"""

bookData = []
ratingsData = {}
affinityData = {}

with open("booklist.txt") as f:
    """
    Gets the book data loaded into the list
    """
    while True:
        line = f.readline().rstrip()
        if line == "":
            break
        bookData.append(tuple(line.split(",")))

with open("ratings.txt") as f:
    """
    Gets the ratings data and each reader put into the dictionary.
    """
    while True:
        reader = f.readline().rstrip()
        if reader == "":
            break
        rawRating = f.readline().split()
        rating = list(map(int, rawRating))
        ratingsData[reader.lower()] = rating

def docprod(rOne,rTwo):
    """
    Takes two readers, then accesses ratingsData and multiplies their ratings to return a similarity in tastes.
    """
    listOne = ratingsData[rOne]
    listTwo = ratingsData[rTwo]

    affinity = sum([lOne*lTwo for (lOne, lTwo) in zip(listOne, listTwo)])
    return affinity

def docProdItAllbb():
    """
    One docprod to rull them all, just kidding this is gonna docprod them all! Uses docprod on everyone and adds the results to
    affinityData.
    """
    for readerOne in ratingsData.keys():
        affinityList = []

        for readerTwo in ratingsData.keys():
            if readerTwo == readerOne:
                continue

            affinityList.append((docprod(readerOne, readerTwo), readerTwo))
            
        affinityList.sort(reverse=True)
        affinityData[readerOne] = affinityList

docProdItAllbb()

def friends(reader, numFriend = 2):
    """
    Takes a reader and finds their two best friends (or who they're most like) from affinityData and returns them in alphabetical order.
    :D
    """
    # Commented out to make friends take an input as to the amount of friends you want returned.
    # friendOne = affinityData[reader][0][1]
    # friendTwo = affinityData[reader][1][1]

    # listFriends = [friendTwo, friendOne]

    listFriends = []

    for i in range(numFriend):
        listFriends.append(affinityData[reader][i][1])

    return sorted(listFriends)

def recommend(reader, numFriend = 2):
    """
    Takes a reader and obtains their friends. This is then used to find the recommended books from those friends for the reader via
    finding their likes, then using the index from their rating to find the book! Then sorts the books by last name, first name, then 
    finally the book title.
    """
    listIndexes = []
    bookRecommended = []
    refinedBookRecommended = []
    theFriends = friends(reader, numFriend)

    for friend in theFriends:
        for i in range(len(ratingsData[reader])):
            if ratingsData[reader][i] == 0:
                if ratingsData[friend][i] == 3 or ratingsData[friend][i] == 5:
                    listIndexes.append(i)

    for index in listIndexes:
        bookRecommended.append(bookData[index])

    #this next part is necessary because with the way I have my previous function set up, it gets duplicates of the same book
    #this removes those duplicates prior to the sort
    for i in bookRecommended:
        if i not in refinedBookRecommended:
            refinedBookRecommended.append(i)

    titleSorted = sorted(refinedBookRecommended, key=lambda x: x[1])
    firNameSorted = sorted(titleSorted)
    lasNameSorted = sorted(firNameSorted, key=lambda x: x[0].split(" ")[-1])

    return lasNameSorted

def report():
    """
    Mini main. Apparently we aren't supposed to do anything except use main to print off one giant ass (pardon my French) string.
    That's why this is here. To assemble said giant string. Makes sure the docProd is done then starts assembling the list using friends()
    and recommend().
    """
    reportString = f""

    for reader in sorted(ratingsData.keys()):
        myFriends = friends(reader)
        leBooks = recommend(reader)

        reportString += f"{reader}: {myFriends}\n"
        for book in leBooks:
            reportString += f"\t{book}\n"
        
        reportString += "\n"

    return reportString



def main():
    """
    Only prints out one big effing string.
    """
    with open('recommendations.txt', 'w') as rec_file:
        print(report(), file=rec_file)
    print(recommend('albus dumbledore', 2))


if __name__ == "__main__":
    main()