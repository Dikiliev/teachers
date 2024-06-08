//
// const sideMenu = document.getElementById('side-menu')
//
// if (sideMenu){
//   document.getElementById('profile-nav').addEventListener('mouseover', () => {
//     sideMenu.classList.toggle('active', true);
//   });
//
//   document.getElementById('profile-nav').addEventListener('mouseout', () => {
//     sideMenu.classList.toggle('active', false);
//   });
// }


const menuToggle = document.getElementById('mobile-menu');
menuToggle.addEventListener('click', function() {
    const navMenu = document.querySelector('.nav-menu');

    navMenu.classList.toggle('active');
    menuToggle.classList.toggle('active')
});
