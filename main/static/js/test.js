document.addEventListener('DOMContentLoaded', (event) => {
    const questionsList = document.getElementById('question-numbers-list');
    const questionTitle = document.getElementById('question-title');
    const questionText = document.getElementById('question-text');
    const answersList = document.getElementById('answers-list');
    const nextButton = document.getElementById('next-button');

    let currentQuestionIndex = 0;
    let selectedAnswerIndex = -1;

    function renderQuestion(index) {
        selectedAnswerIndex = -1;

        const question = questions[index];
        questionTitle.textContent = `Задание ${index + 1}`;
        questionText.textContent = question.text;

        answersList.innerHTML = '';
        question.answers.forEach((answer, i) => {
            const button = document.createElement('button');
            button.className = 'button answer';
            button.textContent = `${i + 1}. ${answer}`;
            button.addEventListener('click', () => selectAnswer(index, i));
            answersList.appendChild(button);
        });

        nextButton.classList.toggle('inactive', true);

        updateQuestionNumbers(index);
    }

    function selectAnswer(questionIndex, answerIndex) {
        selectedAnswerIndex = answerIndex;
        nextButton.classList.toggle('inactive', false);

        const buttons = answersList.getElementsByClassName('answer');

        for (let i = 0; i < buttons.length; i++) {
            buttons[i].classList.toggle('selected', selectedAnswerIndex === i);
        }

        localStorage.setItem(`question_${questionIndex}_answer`, answerIndex);
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
                results: results
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
        if (selectedAnswerIndex === -1){
            return;
        }

        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            renderQuestion(currentQuestionIndex);
        } else {
            // Сбор результатов и отображение их пользователю
            let correctCount = 0;
            let resultDetails = '';

            questions.forEach((question, index) => {
                const userAnswerIndex = localStorage.getItem(`question_${index}_answer`);
                const userAnswer = question.answers[userAnswerIndex];
                const correctAnswer = question.answers[question.correctAnswer];

                if (userAnswerIndex !== null && question.correctAnswer == userAnswerIndex) {
                    correctCount++;
                }

                resultDetails += `
                    <div>
                        <h3>Вопрос ${index + 1}: ${question.text}</h3>
                        <p>Ваш ответ: ${userAnswer || 'Не отвечено'}</p>
                        <p>Правильный ответ: ${correctAnswer}</p>
                    </div>
                `;
            });

            const totalQuestions = questions.length;
            const resultMessage = `Вы правильно ответили на ${correctCount} из ${totalQuestions} вопросов.`;

            const resultDiv = document.createElement('div');
            resultDiv.className = 'result';
            resultDiv.innerHTML = `<h2>Результаты</h2><p>${resultMessage}</p>${resultDetails}`;

            document.querySelector('.strap').innerHTML = '';
            document.querySelector('.strap').appendChild(resultDiv);
            resultDiv.style.display = 'block';

            // Отправка результатов на сервер для отправки по почте
            const userEmail = prompt("Введите ваш email для получения результатов:");
            if (userEmail) {
                sendResults(userEmail, resultDetails);
            }
        }
    });

    renderQuestion(currentQuestionIndex);
});
