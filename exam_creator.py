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

        question_variations = []
        for i in range(variations_count):
            options = []

            options = [variation[i] for variation in variations]
            question_variations.append(question.format(*options))

        questions.append(question_variations)

    return questions

def generate_test_paper(exam1, exam2):
    with open("header.txt") as f:
        header = f.read()

    test_papers = []

    student_size = 60
    part2_size = 2
    for i in range(student_size):
        test_paper = str(header)
        test_paper += "\n---\nFilename: Part1.py\n"
        random_questions = random.choice(exam2)
        test_paper += random.choice(random_questions)

        random_questions = random.sample(exam1, part2_size)
        for question_no, question_variations in enumerate(random_questions):
            question = random.choice(question_variations)

            filename = "Part2_{}.py"
            filename = filename.format(string.ascii_uppercase[question_no])
            test_paper += "\n---\nFilename: {}\n".format(filename)
            test_paper += question

        test_papers.append(test_paper)
    return test_papers

exam1 = extract_questions("exam.txt")
exam2 = extract_questions("exam2.txt")

questions = exam1 + exam2

test_papers = generate_test_paper(exam1, exam2)

# save the questions for future reference
with open("questions.txt", "w") as f:
    question_variations = ["\n=========\n".join(question) for question in questions] 
    output = "\n=========\n".join(question_variations)
    f.write(output)

print("{} questions saved".format(len(questions)))

with open("test papers.txt", "w") as f:
    f.write("\n\n\n\n\n".join(test_papers))