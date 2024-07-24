document.addEventListener('DOMContentLoaded', (event) => {
    const questionsList = document.getElementById('question-numbers-list');
    const questionTitle = document.getElementById('question-title');
    const questionText = document.getElementById('question-text');
    const answersList = document.getElementById('answers-list');
    const nextButton = document.getElementById('next-button');

    const testFinishForm = document.getElementById('test-finish-form');
    const testFinished = document.getElementById('test-finished');

    let currentQuestionIndex = 0;
    let selectedAnswerIndex = -1;
    const userAnswers = {};

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
        if (document.getElementById('test-finish-button').classList.contains('inactive')){
            return
        }

        document.getElementById('test-finish-button').classList.toggle('inactive', true);

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
                testFinishForm.classList.toggle('active', false);
                testFinished.classList.toggle('active', true);
                testFinished.querySelector('.icon-strap').classList.add('visible');
            } else {
                document.getElementById('email').classList.toggle('inactive', false);
            }
        });
    }

    nextButton.addEventListener('click', () => {
        if (selectedAnswerIndex === -1) {
            return;
        }

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



            // const resultDiv = document.createElement('div');
            // resultDiv.className = 'result';
            // resultDiv.innerHTML = `<h2>Результаты</h2><p></p>`;
            //
            // document.querySelector('.strap').innerHTML = '';
            // document.querySelector('.strap').appendChild(resultDiv);
            // resultDiv.style.display = 'block';

            document.querySelector('.test').classList.toggle('active', false);
            testFinishForm.classList.toggle('active', true);

            testFinishForm.querySelector('.icon-strap').classList.add('visible');

            document.getElementById('test-finish-button').onclick = () => {
                sendResults(document.getElementById('email').value, results);
            }
        }
    });

    renderQuestion(currentQuestionIndex);
});
