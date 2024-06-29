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


function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}