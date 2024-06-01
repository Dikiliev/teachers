const specialistButton = document.getElementById('teacher-button');
const serviceButton = document.getElementById('subject-button');
const dateButton = document.getElementById('group-button');

class Page{
    constructor(url, buttonText) {
        this.url = url;
        this.buttonText = buttonText;
    }
}


const pages = {
    0: new Page('select_teacher', 'Выбрать преподователя'),
    1: new Page('select_subject', 'Выбрать предмет'),
    2: new Page('select_group', 'Выбрать расписание'),
    3: new Page('completion_appointment', 'Перейти к оформлению'),
}

if (current_page === 0){
    specialistButton.classList.toggle('active', true);
}
else if (current_page === 1){
    serviceButton.classList.toggle('active', true);
}
else{
    dateButton.classList.toggle('active', true);
}

specialistButton.addEventListener('click', () =>{
    redirect_url('select_teacher');
});

serviceButton.addEventListener('click', () =>{
    redirect_url('select_subject');
});

dateButton.addEventListener('click', () =>{
    redirect_url('select_group');
});




function redirect_url(url){
    let resultUrl = `/${url}/${getUrlString()}`
    window.location.assign(resultUrl);
}


function getUrlString(){
    return `w${selectedTeacherId}s${selectedSubjectId}d${selectedGroupId}`
}