
let data = {};

document.addEventListener('DOMContentLoaded', function () {
    manageGroupInit().then();
});

async function manageGroupInit(){
    data = await getGroupData(group_id);

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
        `<div class="group-fields">
            <button onclick="addGroup()" class="button">Добавить новую группу</button>
            <button class="button" type="submit">Сохранить</button>
        </div>
        `
}

async function getGroupData(group_id){
    try {
        const response = await fetch(`/get_group/${group_id}`);
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
                <label for="price">Цена&nbsp;в&nbsp;месяц:</label>
                <input type="number" id="price" name="price" value="${group.price}" required>
            </div>
            <div class="input-group">
                <label for="category">Предмет:</label>
                <select name="category" id="category" required>
                    <option value="0"> -- Не выбрано -- </option>
                    ${available_subjects.map(subject => `
                        <option value="${subject.id}" ${subject.id === group.subject.id ? 'selected' : ''}>${subject.name}</option>
                    `).join('')}
                </select>
            </div>
        </div>
        <div class="schedules-list"></div>
        
        <div class="container row" style="width: 100%">
            <div class="group-fields">
                <button onclick="addSchedule()" class="button add-schedule">Добавить урок</button>
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
                        <option value="${day[0]}" ${day[1] === schedule.day_of_week ? 'selected' : ''}>${day[1]}</option>
                    `).join('')}
                </select>
            </div>
            <div class="input-group">
                <label for="start_time_${scheduleIndex}">Время&nbsp;начала:</label>
                <input type="time" id="start_time_${scheduleIndex}" name="start_time_${scheduleIndex}" value="${schedule.start_time}" required>
            </div>
            <div class="input-group">
                <label for="duration_${scheduleIndex}">Длительность&nbsp;(в&nbsp;минутах):</label>
                <input type="number" id="duration_${scheduleIndex}" name="duration_${scheduleIndex}" value="${Math.round(schedule.duration_minutes)}" required>
            </div>
            <button onclick="deleteSchedule(${scheduleIndex})" class="button danger delete-schedule">Удалить урок</button>
        </div>
        
        <div class="container row" style="width: 100%"></div>
    `;
    return scheduleDiv;
}

function addGroup(){
    const group = {
        'schedules': [{},],
        'subject': {}
    }

    refreshData();
}

function deleteGroup(){

    refreshData();
}

function addSchedule(){
    data.group.schedules.push({})
    refreshData();
}

function deleteSchedule(scheduleIndex){
    data.group.schedules.splice(scheduleIndex, 1);
    refreshData();
}