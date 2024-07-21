document.addEventListener('DOMContentLoaded', (event) => {
    const questionsList = document.getElementById('question-numbers-list');
    const questionTitle = document.getElementById('question-title');
    const questionText = document.getElementById('question-text');
    const answersList = document.getElementById('answers-list');
    const nextButton = document.getElementById('next-button');

    let currentQuestionIndex = 0;
    let selectedAnswerIndex = -1;
    const userAnswers = {};

    console.log(questions);

    function renderQuestion(index) {
        selectedAnswerIndex = -1;

        const question = questions[index];
        questionTitle.textContent = `Задание ${index + 1}`;
        questionText.textContent = question.text;



        answersList.innerHTML = '';
        question.answers.forEach((answer, i) => {
            const button = document.createElement('button');
            button.className = 'button answer';
            button.textContent = `${i + 1}. ${answer.text}`;
            button.addEventListener('click', () => selectAnswer(index, i, question.id));
            answersList.appendChild(button);
        });

        nextButton.classList.toggle('inactive', true);

        updateQuestionNumbers(index);
    }

    function selectAnswer(questionIndex, answerIndex, questionId) {
        selectedAnswerIndex = answerIndex;
        nextButton.classList.toggle('inactive', false);

        const buttons = answersList.getElementsByClassName('answer');

        for (let i = 0; i < buttons.length; i++) {
            buttons[i].classList.toggle('selected', selectedAnswerIndex === i);
        }

        userAnswers[questionId] = answerIndex;
    }

    function updateQuestionNumbers(currentIndex) {
        const questionNumbers = questionsList.children;
        for (let i = 0; i < questionNumbers.length; i++) {
            questionNumbers[i].classList.remove('current');
            if (i < currentIndex) {
                questionNumbers[i].classList.add('passed');
            } else if (i === currentIndex) {
                questionNumbers[i].classList.add('current');
            }
        }
    }

    function sendResults(email, results) {
        fetch('/send_results/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: JSON.stringify({
                email: email,
                results: results,
                test_id: testId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Результаты успешно отправлены на вашу почту!');
            } else {
                alert('Ошибка при отправке результатов.');
            }
        });
    }

    nextButton.addEventListener('click', () => {
        if (selectedAnswerIndex === -1) {
            return;
        }

        console.log(userAnswers);

        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            renderQuestion(currentQuestionIndex);
        } else {
            let correctCount = 0;
            let results = {

            };

            questions.forEach((question, index) => {
                const userAnswerIndex = userAnswers[question.id];
                results[question.id] = question.answers[userAnswerIndex].id
            });

            const resultDiv = document.createElement('div');
            resultDiv.className = 'result';
            resultDiv.innerHTML = `<h2>Результаты</h2><p></p>`;

            document.querySelector('.strap').innerHTML = '';
            document.querySelector('.strap').appendChild(resultDiv);
            resultDiv.style.display = 'block';

            const userEmail = prompt("Введите ваш email для получения результатов:");
            if (userEmail) {
                sendResults(userEmail, results);
            }
        }
    });

    renderQuestion(currentQuestionIndex);
});
