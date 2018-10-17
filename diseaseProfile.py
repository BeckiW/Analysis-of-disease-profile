import csv
import sys

# This script compares users based the similarity of their disease profile.

# You should run this script with the name of the CSV file containing the data.
# Example: "python diseaseProfile.py UserData01.csv"

# The name of the CSV file containing the 'disease similarity' data.
kSimilarityDataFile = 'DiseaseSimilarity.csv'

# The number of data columns in the provided user data and non-header rows/columns in DiseaseSimilarity.csv
kNumberOfDiseases = 5


# Load the disease similarity data into a global variable for use later.
with open(kSimilarityDataFile, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    similarityData = list(reader)


# Calculate the similarity score between two users (rows in the CSV file)
def calculateSimilarityScore(rowA, rowB):
    diseaseCountA = 0
    similarity = 0

    for x in xrange(1,1+kNumberOfDiseases):
        diseaseCountB = 0
        diseaseScore = 0

        if int(rowA[x]) == 1:
            diseaseCountA += 1

            for y in xrange(1,1+kNumberOfDiseases):
                if int(rowB[y]) == 1:
                    diseaseCountB += 1
                    diseaseScore += float(similarityData[x][y])

            diseaseScore /= diseaseCountB
            similarity += diseaseScore

    similarity /= diseaseCountA
    return similarity


# Calculate the diseaseProfile for a dataset.
# Takes two parameters:
#  filepath is a CSV file containing the user data,
#  outputFilePath is an optional output filename to save the data in.
def diseaseProfile(filePath, outputFilePath=None):
    srcData = []

    try:
        csvFile = open(filePath, 'rU')
        reader = csv.reader(csvFile)
        srcData = list(reader)
    except (IOError, OSError) as e:
        print("Could not read source data - does the file exist?")
        return

    numberOfRows = len(srcData)
    outputData = []

    if numberOfRows < 2:
        print ("No data in provided CSV file.")
        return

    # Go over each user (rowA) and compare with each other user (rowB).
    for rowNumA in range(1, numberOfRows):
        rowA = srcData[rowNumA]

        for rowNumB in xrange(rowNumA+1, numberOfRows):
            rowB = srcData[rowNumB]
            similarityScore = calculateSimilarityScore(rowA, rowB)

            output = (rowA[0], rowB[0], similarityScore)
            outputData.append( output )

        # Debug Output: Uncomment for extra debug info
        # print( row[0], rowB[0], similarity )

    # Print out the results first
    sortedData = sorted(outputData, key = lambda element : element[2], reverse=True)
    	
    for row in sortedData:
    	print( "%4s - %4s: %f" % row )


    # Output to CSV File if we have provided outputFilePath
    if outputFilePath is not None:
        outputFile = open(outputFilePath, 'wb')
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow( ["User 1", "User 2", "Similarity"] )

        for row in sortedData:
            outputWriter.writerow(row)


# Main script

if len(sys.argv) < 2:
    print "Error occured: please enter name of script and name of file"
    exit()

inputFile = sys.argv[1]
diseaseProfile(inputFile, "output.csv")
