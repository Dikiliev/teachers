const workerCards = document.getElementsByClassName('worker-card');
const cardPrefix = 'worker-card-';

initSTeachers();

function initSTeachers(){
    for (const card of workerCards) {
        card.querySelector('.worker').addEventListener('click', () => {
            selectTeacher(+card.id.replace(cardPrefix, ''));
        });

        const subjectButtons = card.getElementsByClassName('subject')
        for (const subjectButton of subjectButtons){
            const subject_id = subjectButton.dataset.id;
            subjectButton.addEventListener('click', () => {
                selectSubject(card.id.replace(cardPrefix, ''), subject_id)
            })
        }
    }

    const selectElement = document.getElementById(cardPrefix + selectedTeacherId);
    selectElement?.classList.toggle('selected', true);
}

function selectTeacher(id, force=false){
    console.log(`select teacher ${id} (previous: ${selectedTeacherId}) (force: ${force})`)

    if (!force && id == selectedTeacherId){
        selectedTeacherId = 0;
        selectedSubjectId = 0
    }
    else{
         selectedTeacherId = id;
    }

    unselectAll();

    const selectElement = document.getElementById(cardPrefix + selectedTeacherId);
    selectElement?.classList.toggle('selected', true);

    // refreshNextButton();
}

function selectSubject(teacher_id, subject_id){
    console.log(`select subject ${subject_id} (previous: ${selectedSubjectId})`)

    if (teacher_id === selectedTeacherId && selectedSubjectId === subject_id){
        selectedSubjectId = 0
    }
    else{
        selectedTeacherId = teacher_id;
        selectedSubjectId = subject_id
    }

    unselectAll();

    const selectElement = document.getElementById(cardPrefix + selectedTeacherId);
    if (selectElement){
        selectElement.classList.toggle('selected', true);

        const subjectButton = selectElement.querySelector(`[data-id="${selectedSubjectId}"]`)

        if (subjectButton){
            subjectButton.classList.toggle('selected', true)
        }
    }

    // refreshNextButton();
}

function unselectAll(){
    for (const card of workerCards) {
        card.classList.toggle('selected', false)

        const subjectButtons = card.getElementsByClassName('subject')
        for (const subjectButton of subjectButtons){
            subjectButton.classList.toggle('selected', false)
        }
    }
}


function toggleDescription(event, workerId) {
    event.stopPropagation()
    const descriptionElement = document.getElementById(`description-${workerId}`);
    const buttonElement = descriptionElement.nextElementSibling;
    const arrowElement = buttonElement.querySelector('.arrow');

    if (descriptionElement.classList.contains('expanded')) {
        descriptionElement.classList.remove('expanded');
        buttonElement.textContent = 'Показать больше';
        arrowElement.textContent = '⮟';
    } else {
        descriptionElement.classList.add('expanded');
        buttonElement.textContent = 'Скрыть';
        arrowElement.textContent = '⮝';
    }

    buttonElement.appendChild(arrowElement);
}



