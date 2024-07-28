const DEBUG = true;


const BASE_URL = DEBUG ? 'http://localhost:8000/' : 'https://xexarxo.ru/';


async function fetchData(endpoint) {
    const url = BASE_URL + endpoint;
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

async function postData(endpoint, data) {
    const url = BASE_URL + endpoint;
    const csrfToken = getCsrfToken();
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}


function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}

let logTimeout;

function logInfo(text, isError = false, duration = null) {
    const logElement = document.getElementById('log-p');

    if (logTimeout) {
        clearTimeout(logTimeout);
        logTimeout = null;
    }

    logElement.classList.add('hide');

    setTimeout(() => {
        logElement.innerHTML = text;
        logElement.classList.toggle('error', isError);
        logElement.classList.remove('hide');

        if (duration !== null) {
            logTimeout = setTimeout(() => {
                logElement.classList.add('hide');
            }, duration);
        }
    }, 200);
}

