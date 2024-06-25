let data = {};

document.addEventListener('DOMContentLoaded', function () {
    manageGroupInit().then();
});

async function manageGroupInit(){
    data = await getGroupData(teacher_id, group_id);

    refreshData();
}

function refreshData(){
    const container = document.getElementById('groups-container');
    container.innerHTML = '';

    const group = data.group;
    const groupElement = generateGroupElement(group, data.available_subjects);
    container.appendChild(groupElement);

    group.schedules.forEach((schedule, scheduleIndex) => {
        const scheduleElement = generateScheduleElement(schedule, scheduleIndex, data.days_of_week);
        groupElement.querySelector('.schedules-list').appendChild(scheduleElement);
    });

    container.innerHTML +=
        `
        <div style="display: flex; flex-direction: column; gap: 1rem; width: 100%">
            <p id="log-p" class="log success hide">Сохранено.</p>
            <div class="group-fields">
                
                <button class="button" onclick="cancelChanges()">Отменить</button>
                <button class="button" onclick="saveChanges()">Сохранить</button>
            </div>
            <a class="href danger" style="text-align: center; margin-top: 10px;" onclick="deleteGroup()">Удалить группу</a>
        </div>
        `;
}

async function getGroupData(teacher_id, group_id){
    try {
        const response = await fetch(`/get_group/${teacher_id}/${group_id}`);
        return await response.json();
    }
    catch (error){
        console.error(error);
        return [];
    }
}

function generateGroupElement(group, available_subjects){
    const groupDiv = document.createElement('div');
    groupDiv.classList.add('group');
    groupDiv.innerHTML = `
        <div class="group-fields">
            <div class="input-group">
                <label for="name">Название&nbsp;группы:</label>
                <input type="text" id="name" name="name" value="${group.name}" required>
            </div>

            <div class="input-group">
                <label for="category">Предмет:</label>
                <select name="category" id="category" required>
                    <option value="0"> -- Не выбрано -- </option>
                    ${available_subjects.map(subject => `
                        <option value="${subject.id}" ${group.subject && subject.id == group.subject.id ? 'selected' : ''}>${subject.name}</option>
                    `).join('')}
                </select>
            </div>
        </div>
        <div class="schedules-list"></div>
        <div class="container row" style="width: 100%">
            <div class="group-fields">
                <button onclick="addSchedule()" class="button add-schedule"><span style="color: inherit; font-size: 2rem;">+</span>&ensp;Добавить урок</button>
            </div>
        </div>
    `;
    return groupDiv;
}

function generateScheduleElement(schedule, scheduleIndex, days_of_week){
    const scheduleDiv = document.createElement('div');
    scheduleDiv.classList.add('schedule');
    scheduleDiv.innerHTML = `
        <h3>Урок ${scheduleIndex + 1}</h3>
        <div class="schedule-fields">
            <div class="input-group">
                <label for="day_of_week_${scheduleIndex}">День&nbsp;недели:</label>
                <select id="day_of_week_${scheduleIndex}" name="day_of_week_${scheduleIndex}" required>
                    <option value="0"> -- Не выбрано -- </option>
                    ${days_of_week.map(day => `
                        <option value="${day[0]}" ${day[0] == schedule.day_of_week ? 'selected' : ''}>${day[1]}</option>
                    `).join('')}
                </select>
            </div>
            <div class="input-group">
                <label for="start_time_${scheduleIndex}">Время&nbsp;начала:</label>
                <input type="time" id="start_time_${scheduleIndex}" name="start_time_${scheduleIndex}" value="${schedule.start_time}" required>
            </div>
            <div class="input-group">
                <label for="duration_${scheduleIndex}">Длительность&nbsp;(в&nbsp;минутах):</label>
                <input type="number" id="duration_${scheduleIndex}" name="duration_${scheduleIndex}" value="${schedule.duration_minutes ? Math.round(schedule.duration_minutes) : 120}" required>
            </div>
            <button onclick="deleteSchedule(${scheduleIndex})" class="button danger delete-schedule">Удалить урок</button>
        </div>
        <div class="container row" style="width: 100%"></div>
    `;
    return scheduleDiv;
}

function addSchedule(){
    updateGroupData();

    data.group.schedules.push({})
    refreshData();
}

function deleteSchedule(scheduleIndex){
    updateGroupData();

    data.group.schedules.splice(scheduleIndex, 1);
    refreshData();
}

function validateForm() {
    let isValid = true;
    const name = document.getElementById('name').value.trim();
    const category = document.getElementById('category').value;

    if (!name) {
        isValid = false;
        logInfo('Название группы обязательно.', true);
    }

    if (category === "0") {
        isValid = false;
        logInfo('Предмет обязателен.', true);
    }

    data.group.schedules.forEach((_, scheduleIndex) => {
        const dayOfWeek = document.getElementById(`day_of_week_${scheduleIndex}`).value;
        const startTime = document.getElementById(`start_time_${scheduleIndex}`).value;
        const duration = document.getElementById(`duration_${scheduleIndex}`).value;

        if (dayOfWeek === "0" || !startTime || !duration) {
            isValid = false;
            logInfo(`Все поля для Урока ${scheduleIndex + 1} обязательны.`, true);
        }
    });

    return isValid;
}

function updateGroupData(){
    const group = data.group;
    group.name = document.getElementById('name').value;
    group.subject.id = document.getElementById('category').value;

    group.schedules.forEach((schedule, scheduleIndex) => {
        schedule.day_of_week = document.getElementById(`day_of_week_${scheduleIndex}`).value;
        schedule.start_time = document.getElementById(`start_time_${scheduleIndex}`).value;
        schedule.duration_minutes = document.getElementById(`duration_${scheduleIndex}`).value;
    });

    return group;
}

function saveChanges() {
    if (!validateForm()) {
        return;
    }

    const group = updateGroupData();

    fetch(`/save_group/${group_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(group)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);

        if ('error' in data){
            logInfo('Ошибка при сохранении данных.', true);
        }
        else{
            logInfo('Данные успешно сохранены.');
        }

    })
    .catch((error) => {
        console.error('Error:', error);
        logInfo('Ошибка при сохранении данных.', true);
    });
}

function logInfo(text, isError = false){
    const logElement = document.getElementById('log-p');
    logElement.innerHTML = text;
    logElement.classList.toggle('error', isError);
    logElement.classList.toggle('hide', false);
}

function cancelChanges() {
    manageGroupInit();
}

function deleteGroup(){
        fetch(`/delete_group/${group_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);

        if (!data.ok){
            logInfo('Ошибка при удалении группы.', true);

            return
        }

        logInfo('Группа удалена');
        window.location.replace('/manage_groups')

    })
    .catch((error) => {
        console.error('Error:', error);
        logInfo('Ошибка при удалении группы.', true);
    });
}