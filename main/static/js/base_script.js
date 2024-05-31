BASE_URL = 'http://localhost:8000/'


async function fetchData(url) {
    url = BASE_URL + url;
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