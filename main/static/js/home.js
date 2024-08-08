// home.js

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("subjectModal");
    const btn = document.getElementById("openModalBtn");
    const span = document.getElementsByClassName("close")[0];
    const subjectList = document.getElementById("subjectList");

    // When the user clicks the button, open the modal
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Add click event listeners to list items
    // subjectList.addEventListener('click', function(event) {
    //     event.preventDefault(); // Prevent default anchor click behavior
    //     const target = event.target;
    //
    //     if (target.tagName.toLowerCase() === 'a') {
    //         const testUrl = target.getAttribute('data-test-url');
    //         if (testUrl && testUrl !== '/test/0') {
    //             window.location.href = testUrl;
    //         } else {
    //             alert('Пожалуйста, выберите предмет для прохождения теста.');
    //         }
    //     }
    // });
});
