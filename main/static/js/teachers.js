const subjectElements = document.getElementsByClassName('subject');
const teachersList = document.getElementById('teahcers')

// const workerCards = document.getElementsByClassName('worker-card');
const cardPrefix = 'worker-card-';

let selectedSubjectId = 0;
let teachers = [];

start();

function start(){
    loadTeachers();

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

            <button class="button" onclick="openModelWindow()">Записаться</button>
        </div>
    `;
    return teacherHTML;
}


function initSTeachers(){

}

function selectSubject(subject_id){
    console.log(`select subject ${subject_id} (previous: ${selectedSubjectId})`)

    selectedSubjectId = selectedSubjectId === subject_id ? 0 : subject_id;

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

function openModelWindow(){
    document.getElementById('modal').style.display = 'block';
}

document.querySelector('.close-button').addEventListener('click', function() {
  document.getElementById('modal').style.display = 'none';
});

window.onclick = function(event) {
  if (event.target == document.getElementById('modal')) {
    document.getElementById('modal').style.display = 'none';
  }
}
