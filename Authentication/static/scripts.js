
// document.getElementById('loginForm').addEventListener('submit', function (e) {
//     e.preventDefault();
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;

//     if (username && password) {
//         alert('Login successful! Welcome to Artistry.');
//     }
// });

// // Add subtle parallax effect to floating icons
// document.addEventListener('mousemove', function (e) {
//     const icons = document.querySelectorAll('.art-icons');
//     const x = e.clientX / window.innerWidth;
//     const y = e.clientY / window.innerHeight;

//     icons.forEach((icon, index) => {
//         const speed = (index + 1) * 20;
//         icon.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
//     });
// });


// // Add hover effect to input fields<script>
// // Signup form validation and enhancements


// const form = document.getElementById('signupForm');
// const password = document.getElementById('password');
// const confirmPassword = document.getElementById('confirmPassword');
// const strengthBar = document.getElementById('strengthBar');

// // Password strength indicator
// password.addEventListener('input', function () {
//     const value = this.value;
//     const strength = calculatePasswordStrength(value);

//     strengthBar.className = 'password-strength';
//     if (value.length > 0) {
//         if (strength < 3) {
//             strengthBar.classList.add('strength-weak');
//         } else if (strength < 5) {
//             strengthBar.classList.add('strength-medium');
//         } else {
//             strengthBar.classList.add('strength-strong');
//         }
//     }
// });

// function calculatePasswordStrength(password) {
//     let strength = 0;
//     if (password.length >= 8) strength++;
//     if (password.length >= 12) strength++;
//     if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
//     if (/\d/.test(password)) strength++;
//     if (/[^a-zA-Z\d]/.test(password)) strength++;
//     return strength;
// }



// // Parallax effect for floating icons
// document.addEventListener('mousemove', function (e) {
//     const icons = document.querySelectorAll('.art-icons');
//     const x = e.clientX / window.innerWidth;
//     const y = e.clientY / window.innerHeight;

//     icons.forEach((icon, index) => {
//         const speed = (index + 1) * 20;
//         icon.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
//     });
// });