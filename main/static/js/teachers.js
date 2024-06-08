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
                    
                    ${worker.skills.map(skill => `<span class="title-skill">${skill}</span>`).join('')}
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

        groupCardsElement.innerHTML = groups.map(group => `
        
            <div class="group-card">
                    <h1>${group.name}</h1>
                    ${ group.schedules.map(schedule => `<p>${schedule.day_of_week} <span class="primary-text">${schedule.start_time} - ${schedule.end_time}</span></p>`).join('\n') }
            </div>
        
        `).join('\n')

        document.getElementById('modal').style.display = 'block';
    })
}

async function getGroups(teacher_id, subject_id){
    try {
        const response = await fetchData(`get_groups/${teacher_id}/${subject_id}`);
        return response.groups;
    }
    catch (error){
        console.error(error);
        return [];
    }
}

document.querySelector('.close-button').addEventListener('click', function() {
  document.getElementById('modal').style.display = 'none';
});

window.onclick = function(event) {
  if (event.target == document.getElementById('modal')) {
    document.getElementById('modal').style.display = 'none';
  }
}
