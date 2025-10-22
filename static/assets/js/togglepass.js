function togglePassword(fieldId, iconElement) {
    const input = document.getElementById(fieldId);
    if (input.type === "password") {
      input.type = "text";
      iconElement.classList.remove("mdi-eye-off");
      iconElement.classList.add("mdi-eye");
    } else {
      input.type = "password";
      iconElement.classList.remove("mdi-eye");
      iconElement.classList.add("mdi-eye-off");
    }
  }
