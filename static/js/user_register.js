
  const firstName = document.querySelector('#id_first_name');
  const lastName = document.querySelector('#id_last_name');
  const emailInput = document.getElementById("id_email_id");
  const mobileInput = document.getElementById('id_mobile_no');
  const usernameInput = document.getElementById('username');
  const submitButton = document.querySelector('button[type="submit"]');
  const usernameError = document.getElementById('usernameError');
  const mobileError = document.getElementById('mobileError');

  const nameRegex = /^[a-zA-Z\s]*$/;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const mobileRegex = /^[0-9]{10}$/;

  // Initially disable submit button until the mobile number is valid
  submitButton.disabled = true;

  // Event listeners for name inputs
  firstName.addEventListener('input', function () {
      restrictNameInput(firstName);
  });
  lastName.addEventListener('input', function () {
      restrictNameInput(lastName);
  });

  // Event listener for email input
  emailInput.addEventListener('input', function () {
      validateInput(emailInput, emailRegex, 'emailError');
  });

  // Event listener for mobile input
  mobileInput.addEventListener('input', function () {
      restrictMobileInput(mobileInput);

      // Check if the mobile number has exactly 10 digits
      if (mobileInput.value.length === 10) {
          validateMobileExistence(mobileInput.value);  // Check with backend if valid
      } else {
          // If not exactly 10 digits, disable the submit button and show error
          mobileError.textContent = 'Mobile number must be 10 digits';
          mobileError.style.display = 'block';
          submitButton.disabled = true;
      }
  });

  // Event listener for username input
  usernameInput.addEventListener('input', function () {
      validateInput(usernameInput, /^[a-zA-Z0-9_]*$/, 'usernameError');
      if (usernameInput.value.length > 0) {
          checkUsernameExistence(usernameInput.value);
      }
  });

  // Function to restrict name input
  function restrictNameInput(inputElement) {
      const value = inputElement.value;
      if (!nameRegex.test(value)) {
          inputElement.value = value.replace(/[^a-zA-Z\s]/g, ''); 
      }
  }

  // Function to restrict mobile input to only numbers and exactly 10 digits
  function restrictMobileInput(inputElement) {
      const value = inputElement.value;

      // Remove any non-numeric characters
      inputElement.value = value.replace(/[^0-9]/g, '');

      // If more than 10 digits are entered, truncate the value
      if (inputElement.value.length > 10) {
          inputElement.value = inputElement.value.slice(0, 10);
      }
  }

  // Function to validate inputs
  function validateInput(inputElement, regex, errorId) {
      const value = inputElement.value;
      const errorMessage = document.getElementById(errorId);

      if (!regex.test(value) && value.trim() !== '') {
          inputElement.classList.add('is-invalid');
          errorMessage.style.display = 'block';
      } else {
          inputElement.classList.remove('is-invalid');
          errorMessage.style.display = 'none';
      }
  }

  // Function to validate mobile number with the backend
  function validateMobileExistence(mobileNumber) {
      fetch(`/valid_mob/${mobileNumber}/`)
          .then(response => response.json())
          .then(data => {
              if (!data.is_valid) {
                  mobileInput.classList.add('is-invalid');
                  mobileError.style.display = 'block';
                  mobileError.textContent = 'Mobile number already registered';
                  submitButton.disabled = true;  // Disable submit button if mobile is already registered
              } else {
                  mobileInput.classList.remove('is-invalid');
                  mobileError.style.display = 'none';
                  submitButton.disabled = false;  // Enable submit button if mobile is valid
              }
          })
          .catch(error => {
              console.error('Error:', error);
          });
  }

  // Function to check if username already exists
  function checkUsernameExistence(username) {
      fetch(`/valid_user/${username}/`)
          .then(response => response.json())
          .then(data => {
              if (!data.is_valid) {
                  usernameInput.classList.add('is-invalid');
                  usernameError.style.display = 'block';
              } else {
                  usernameInput.classList.remove('is-invalid');
                  usernameError.style.display = 'none';
              }
          })
          .catch(error => {
              console.error('Error:', error);
          });
  }

  const passwordInput = document.getElementById("id_password");
  const confirmPasswordInput = document.getElementById("id_confirm_password");
  const password = passwordInput.value;
  const requirements = validatePassword(password);
 //Function to validate password requirements
       function validatePassword(password) {
          const lengthRe = /.{8,}/;
          const uppercaseRe = /[A-Z]/;
           const lowercaseRe = /[a-z]/;
            const numberRe = /\d/;
            const specialRe = /[!@#$%^&*]/;

            return {
                length: lengthRe.test(password),
                uppercase: uppercaseRe.test(password),
                lowercase: lowercaseRe.test(password),
                number: numberRe.test(password),
                special: specialRe.test(password),
            };
        }
        function updatePasswordRequirements() {
                       const password = passwordInput.value;
                       const requirements = validatePassword(password);
          
                       // Update password requirement checks
                       document.getElementById("password-length").classList.toggle("valid", requirements.length);
                       document.getElementById("password-uppercase").classList.toggle("valid", requirements.uppercase);
                       document.getElementById("password-lowercase").classList.toggle("valid", requirements.lowercase);
                       document.getElementById("password-number").classList.toggle("valid", requirements.number);
                       document.getElementById("password-special").classList.toggle("valid", requirements.special);
          
                       document.getElementById("password-length").classList.toggle("invalid", !requirements.length);
                       document.getElementById("password-uppercase").classList.toggle("invalid", !requirements.uppercase);
                       document.getElementById("password-lowercase").classList.toggle("invalid", !requirements.lowercase);
                       document.getElementById("password-number").classList.toggle("invalid", !requirements.number);
                       document.getElementById("password-special").classList.toggle("invalid", !requirements.special);
          
                       // Enable/Disable confirm password input based on validation
                       const allRequirementsMet = requirements.length && requirements.uppercase && requirements.lowercase && requirements.number && requirements.special;
                       confirmPasswordInput.disabled = !allRequirementsMet;
                   }
       
     // Validate confirm password match
     let confirmPasswordStarted = false;
     function validateConfirmPassword() {
         if (confirmPasswordStarted) {
             const password = passwordInput.value;
             const confirmPassword = confirmPasswordInput.value;

             if (confirmPassword === password) {
                 confirmPasswordInput.classList.remove("is-invalid");
                 confirmPasswordInput.classList.add("is-valid");
                 document.getElementById("confirm-password-match").style.display = "block";
                 document.getElementById("confirm-password-error").style.display = "none";
             } else {
                 confirmPasswordInput.classList.add("is-invalid");
                 confirmPasswordInput.classList.remove("is-valid");
                 document.getElementById("confirm-password-match").style.display = "none";
                 document.getElementById("confirm-password-error").style.display = "block";
             }
         }
     }
     passwordInput.addEventListener("input", function () {
      updatePasswordRequirements();
      validateConfirmPassword();
      checkFormValidity();
  });
     confirmPasswordInput.addEventListener("input", function () {
      confirmPasswordStarted = true;
      validateConfirmPassword();
      checkFormValidity();
  });