# bug: duplicates on same question (with different variations) can appear in the same test paper

import random
import string

def extract_questions(file):
    with open(file) as f:
        file = f.read()

    file = file.split("----")
    file = [question.split("....") for question in file]

    questions = []
    for question, variations in file:
        lines = [variation.strip('"').strip().replace('\\n', '\n')
                 for variation in variations.split("\n") 
                 if variation.strip() != '']
        variations = [line.split('", "') for line in lines]
        if not len(variations):
            continue

        variations_count = len(variations[0])

        for i in range(variations_count):
            options = []

            options = [variation[i] for variation in variations]
            questions.append(question.format(*options))

    return questions

exam1 = extract_questions("exam.txt")
exam2 = extract_questions("exam2.txt")

questions = exam1 + exam2

# save the questions for future reference
with open("questions.txt", "w") as f:
    output = "\n=========\n".join(questions)
    f.write(output)

print("{} questions saved".format(len(questions)))

#### generate the test papers
with open("header.txt") as f:
    header = f.read()

test_papers = []

# randomize the questions
exam1_indexes = list(range(len(exam1)))
random.shuffle(exam1_indexes)

student_size = 60
part2_size = 2
for i in range(student_size):
    test_paper = str(header)
    test_paper += "\n---\nFilename: Part1.py\n"
    test_paper += random.choice(exam2)

    random_questions = random.sample(exam1_indexes, part2_size)
    for question_no in range(part2_size):
        filename = "Part2_{}.py"
        filename = filename.format(string.ascii_uppercase[question_no])
        test_paper += "\n---\nFilename: {}\n".format(filename)
        test_paper += exam1[random_questions[question_no]]

    test_papers.append(test_paper)

with open("test papers.txt", "w") as f:
    f.write("\n\n\n\n\n".join(test_papers))