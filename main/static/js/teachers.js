const subjectElements = document.getElementsByClassName('subject');
const teachersList = document.getElementById('teahcers')

// const workerCards = document.getElementsByClassName('worker-card');
const cardPrefix = 'worker-card-';

let theFirstLoadTeachers = true;
let teachers = [];

start();

function start(){
    // loadTeachers();

    selectSubject(selectedSubjectId);
}

function loadTeachers(){
    const response = fetchData(`get_teachers/${selectedSubjectId}`);
    response.then(result => {
        teachers = result.teachers;

        generateTeacher();
    }).catch(error => {
        console.error(error);
    });

}

function generateTeacher(){
    teachersList.innerHTML = '';

    teachers.forEach(worker => {
        const teacherCardHTML = generateTeacherCard(worker);
        teachersList.innerHTML += teacherCardHTML;
    });

    initSTeachers()
}

function generateTeacherCard(worker){
    let teacherHTML = `
        <div id="worker-card-${worker.id}" class="worker-card">
            <div class="worker">
                <img src="${worker.avatar}">
                <div class="worker-info">
                    <span class="work-title">${worker.name}</span>
                    
                    ${worker.description.map(row => `<span class="title-skill">${row}</span>`).join('')}

                </div>
            </div>

            <button class="button" onclick="openModelWindow(${worker.id})">Записаться</button>
        </div>
    `;
    return teacherHTML;
}


function initSTeachers(){

}

function selectSubject(subject_id){
    console.log(`select subject ${subject_id} (previous: ${selectedSubjectId})`)

    if (!theFirstLoadTeachers && selectedSubjectId === subject_id) return;

    theFirstLoadTeachers = false
    selectedSubjectId = subject_id;

    unselectAll();

    if (selectedSubjectId !== 0){
        const selectElement = document.getElementById(`subject_${selectedSubjectId}`);
        selectElement.classList.toggle('selected', true);
    }

    loadTeachers();
}

function unselectAll(){
    for (const element of subjectElements){
        element.classList.toggle('selected', false);
    }
}

function openModelWindow(teacher_id){
    const groupCardsElement = document.getElementById('group-cards');
    groupCardsElement.innerHTML = '';

    getGroups(teacher_id, selectedSubjectId).then(groups => {
        console.log(groups);
        groupCardsElement.innerHTML = groups.map(group =>
            `
            <div class="group-card" onclick="setGroup(event)" data-id="${group.id}">
                <div class="group-card-top-section">
                    <h1>${group.name}</h1>
                    ${ group.schedules.map(schedule => `<p>${schedule.day_of_week_display} <span class="primary-text">${schedule.start_time} - ${schedule.end_time}</span></p>`).join('\n') }
                </div>
                
                ${/*`<p>В месяц <span class="primary-text success">${group.price}₽</span></p>`*/ ''}
            </div>
            `)
            .join('\n')

        document.getElementById('modal').style.display = 'block';
    })
}

async function getGroups(teacher_id, subject_id){
    try {
        const response = await fetchData(`get_groups/${teacher_id}`);
        return response.groups;
    }
    catch (error){
        console.error(error);
        return [];
    }
}

function setGroup(event){
    selectedGroupId = +event.currentTarget.dataset.id;

    const groupCardsElement = document.getElementById('group-cards');
    const groupCards = groupCardsElement.getElementsByClassName('group-card');

    for (const card of groupCards){
        card.classList.toggle('selected', false);
    }

    event.currentTarget.classList.toggle('selected', true);

    const selectGroupButton = document.getElementById('select-group-button');
    selectGroupButton.classList.toggle('inactive', false);
}

function closeModalWindow(){
    selectedGroupId = 0;

    const selectGroupButton = document.getElementById('select-group-button');
    selectGroupButton.classList.toggle('inactive', true);
    document.getElementById('modal').style.display = 'none';
}

document.querySelector('.close-button').addEventListener('click', function() {
    closeModalWindow();
});

window.onclick = function(event) {
    if (event.target == document.getElementById('modal')) {
        closeModalWindow();
    }
}


function selectGroup(){
    if (!Number.isInteger(selectedGroupId) || selectedGroupId <= 0){
        console.error(`Группа не выбрана! (${selectedGroupId})`)
        return
    }

    window.location.assign(`/confirm_appointment/${selectedGroupId}`);
}