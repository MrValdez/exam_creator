import random
import string


def extract_questions(file):
    '''
    1. Open file
    2. Separate each question into list (one question per element)
    3. Expand each question into its variations
    4. Return the questions in the format:
        [
            [question1_variation1, question1_variation2, ..., question1_variationN],
            [question2_variation1, question2_variation2, ..., question2_variationN],
            [question3_variation1, question3_variation2, ..., question3_variationN],
            ...
        ]
    '''
    question_seperator = "----"
    variation_seperator = "...."

    with open(file) as f:
        file = f.read()

    file = file.split(question_seperator)
    file = [question.split(variation_seperator) for question in file]

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


def generate_test_paper(part1, part2, student_size=60, part2_size=2):
    '''
    1. Load the header file that is common on all test papers
    2. For each student,
        2.a. Choose a random question variation for Part 1
        2.b. Add the question to the test paper
        2.c. Choose 2 random question variations for Part 2
        2.d. Determine the filename identifier for each question variations
        2.e. Add the questions to the test paper
    3. Return all the test papers
    '''
    with open("header.txt") as f:
        header = f.read()

    Part1_seperator = "\n---\nFilename: Part1.py\n"
    Part2_seperator = "\n---\nFilename: Part2_{}.py\n"

    test_papers = []
    for i in range(student_size):
        question_variations = random.choice(part1)
        question = random.choice(question_variations)

        test_paper = str(header)
        test_paper += Part1_seperator
        test_paper += question

        random_questions = random.sample(part2, part2_size)
        for question_no, question_variations in enumerate(random_questions):
            question = random.choice(question_variations)
            filename_identifier = string.ascii_uppercase[question_no]
            test_paper += Part2_seperator.format(filename_identifier)
            test_paper += question

        test_papers.append(test_paper)

    return test_papers


def save_questions(questions, seperator="\n=========\n"):
    """
    save all the question variations for future reference
    """
    with open("questions.txt", "w") as f:
        question_variations = [seperator.join(question) for question in questions]
        output = seperator.join(question_variations)
        f.write(output)

    question_size = len(questions)
    question_variations = sum([len(question) for question in questions])

    template = "{} questions saved.\n{} total variations created."
    output = template.format(question_size, question_variations)
    print(output)


def save_test_papers(test_papers):
    with open("test papers.txt", "w") as f:
        f.write("\n\n\n\n\n".join(test_papers))


if __name__ == "__main__":
    part1 = extract_questions("exam2.txt")
    part2 = extract_questions("exam.txt")

    questions = part1 + part2
    save_questions(questions)

    test_papers = generate_test_paper(part1, part2)
    save_test_papers(test_papers)
