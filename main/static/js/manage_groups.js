document.addEventListener('DOMContentLoaded', function () {
    manageGroupsInit().then();
});

async function manageGroupsInit(){
    const data = await getData(user_id);

    const container = document.getElementById('groups-container');
    container.innerHTML = '';

    data.groups.forEach((group, groupIndex) => {
        const groupElement = generateGroupElement(group, groupIndex, data.available_subjects);
        container.appendChild(groupElement);

        group.schedules.forEach((schedule, scheduleIndex) => {
            const scheduleElement = generateScheduleElement(schedule, scheduleIndex, groupIndex, data.days_of_week);
            groupElement.querySelector('.schedules-list').appendChild(scheduleElement);
        });
    });

    container.innerHTML +=
        `<div class="group-fields">
            <button class="button">Добавить новую группу</button>
            <button class="button">Сохранить</button>
        </div>`
}

async function getData(teacherId){
    try {
        const response = await fetch(`/get_groups/${teacherId}`);
        return await response.json();
    }
    catch (error){
        console.error(error);
        return [];
    }
}

function generateGroupElement(group, groupIndex, available_subjects){
    const groupDiv = document.createElement('div');
    groupDiv.classList.add('group');
    groupDiv.innerHTML = `
        <h2>Группа ${groupIndex + 1}</h2>
        <div class="group-fields">
            <div class="input-group">
                <label for="name_${groupIndex}">Название группы:</label>
                <input type="text" id="name_${groupIndex}" name="name_${groupIndex}" value="${group.name}" required>
            </div>
            <div class="input-group">
                <label for="price_${groupIndex}">Цена в месяц:</label>
                <input type="number" id="price_${groupIndex}" name="price_${groupIndex}" value="${group.price}" required>
            </div>
            <div class="input-group">
                <label for="category_${groupIndex}">Предмет:</label>
                <select name="category_${groupIndex}" id="category_${groupIndex}" required>
                    <option value="0"> -- Не выбрано -- </option>
                    ${available_subjects.map(subject => `
                        <option value="${subject.id}" ${subject.id === group.subject.id ? 'selected' : ''}>${subject.name}</option>
                    `).join('')}
                </select>
            </div>
        </div>
        <div class="schedules-list"></div>
        <button class="button add-schedule">Добавить новый урок</button>
    `;
    return groupDiv;
}

function generateScheduleElement(schedule, scheduleIndex, groupIndex, days_of_week){
    const scheduleDiv = document.createElement('div');
    scheduleDiv.classList.add('schedule');
    scheduleDiv.innerHTML = `
        <h3>Урок ${scheduleIndex + 1}</h3>
        <div class="schedule-fields">
            <div class="input-group">
                <label for="day_of_week_${groupIndex}_${scheduleIndex}">День недели:</label>
                <select id="day_of_week_${groupIndex}_${scheduleIndex}" name="day_of_week_${groupIndex}_${scheduleIndex}" required>
                    <option value="0"> -- Не выбрано -- </option>
                    ${days_of_week.map(day => `
                        <option value="${day[0]}" ${day[0] === schedule.day_of_week ? 'selected' : ''}>${day[1]}</option>
                    `).join('')}
                </select>
            </div>
            <div class="input-group">
                <label for="start_time_${groupIndex}_${scheduleIndex}">Время начала:</label>
                <input type="time" id="start_time_${groupIndex}_${scheduleIndex}" name="start_time_${groupIndex}_${scheduleIndex}" value="${schedule.start_time}" required>
            </div>
            <div class="input-group">
                <label for="duration_${groupIndex}_${scheduleIndex}">Длительность (в минутах):</label>
                <input type="number" id="duration_${groupIndex}_${scheduleIndex}" name="duration_${groupIndex}_${scheduleIndex}" value="${Math.round(schedule.duration_minutes)}" required>
            </div>
        </div>
    `;
    return scheduleDiv;
}
