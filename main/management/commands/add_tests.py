from django.core.management.base import BaseCommand
from main.models import Test, Question, Answer, Subject

questions_data = [
    {
        "question": "В треугольнике ABC отрезок DE — средняя линия. Площадь треугольника CDE равна 24. Найдите площадь треугольника ABC.",
        "answers": ["12", "48", "24", "96"],
        "correct_answer": "96"
    },
    {
        "question": "Два угла треугольника равны 58° и 72°. Найдите тупой угол, который образуют высоты треугольника, выходящие из вершин этих углов. Ответ дайте в градусах.",
        "answers": ["130", "58", "150", "50"],
        "correct_answer": "130"
    },
    {
        "question": "Перед началом футбольного матча судья бросает монетку, чтобы определить, какая из команд начнёт игру с мячом. Команда «Труд» играет три матча с разными командами. Найдите вероятность того, что в этих играх «Труд» выиграет жребий ровно один раз.",
        "answers": ["0.375", "0.037", "0.75", "0.37"],
        "correct_answer": "0.375"
    },
    {
        "question": "Найдите корень уравнения",
        "answers": ["27", "-27", "-1", "1"],
        "correct_answer": "-27"
    },
    {
        "question": "Решите уравнение",
        "answers": ["10", "0", "-1", "1"],
        "correct_answer": "-1"
    },
    {
        "question": "Найдите корень уравнения",
        "answers": ["-3", "5", "3", "-5"],
        "correct_answer": "-5"
    },
    {
        "question": "Найдите корень уравнения:",
        "answers": ["-125", "0.125", "-0.25", "-125"],
        "correct_answer": "-1.25"
    },
    {
        "question": "Найдите значение выражения",
        "answers": ["-25", "0.25", "-1.25", "25"],
        "correct_answer": "-25"
    },
    {
        "question": "Найдите значение выражения при",
        "answers": ["1331", "121", "1", "11"],
        "correct_answer": "121"
    },
    {
        "question": "Найдите значение выражения:",
        "answers": ["500", "-425", "425", "450"],
        "correct_answer": "425"
    },
    {
        "question": "Найдите значение выражения если",
        "answers": ["1", "0.81", "3", "9"],
        "correct_answer": "9"
    },
    {
        "question": "Найдите значение выражения",
        "answers": ["-0.5", "-4", "4", "0.5"],
        "correct_answer": "4"
    }
]

class Command(BaseCommand):
    help = 'Добавляет тест по профильной математике в базу данных'

    def handle(self, *args, **options):
        self.create_test_and_questions()

    def create_test_and_questions(self):
        # Create or get the subject
        subject, _ = Subject.objects.get_or_create(name='Профильная математика')

        # Create the test
        test = Test.objects.create(name='Тест по профильной математике', subject=subject)

        # Create questions and answers
        for q_data in questions_data:
            # Create a question
            question = Question.objects.create(text=q_data['question'], test=test)

            # Create answers for the question
            for answer_text in q_data['answers']:
                is_correct = (answer_text == q_data['correct_answer'])
                Answer.objects.create(text=answer_text, question=question, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS(f"Тест '{test.name}' успешно добавлен в базу данных."))
