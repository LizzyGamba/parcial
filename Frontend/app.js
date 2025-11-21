
const API_URL = 'http://127.0.0.1:8000';

function showAlert(containerId, message, type) {
  const container = document.getElementById(containerId);
  if (container) {
    container.innerHTML = `<div class="alert ${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = "", 5000);
  }
}


async function handleRegister(e) {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const password2 = document.getElementById("password2").value.trim();

  if (!email || !password || !password2) {
    showAlert("register-alert", "Todos los campos son obligatorios", "error");
    return;
  }

  if (password !== password2) {
    showAlert("register-alert", "Las contraseñas no coinciden", "error");
    return;
  }


  const userData = {
    email,
    password,
    confirm_password: password2
  };

  try {
    const res = await fetch(`${API_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });

    const data = await res.json();

    if (res.ok) {
      showAlert("register-alert", "Registro exitoso. Redirigiendo...", "success");
      setTimeout(() => (window.location.href = "login.html"), 1500);
    } else {
      showAlert("register-alert", data.detail || "Error al registrarse", "error");
    }

  } catch (err) {
    showAlert("register-alert", "Error de conexión con el servidor", "error");
  }
}




async function handleLogin(e) {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);

    const res = await fetch(`${API_URL}/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", email);

      showAlert("login-alert", "Inicio de sesión exitoso.", "success");
      setTimeout(() => (window.location.href = "index.html"), 1500);

    } else {
      showAlert("login-alert", data.detail || "Credenciales incorrectas", "error");
    }

  } catch (err) {
    showAlert("login-alert", "Error de conexión", "error");
  }
}


async function handleReviewSubmit(e) {
  e.preventDefault();

  const product = document.getElementById("product-name").value;
  const text = document.getElementById("review-text").value;

  const token = localStorage.getItem("token");

  if (!token) {
    showAlert("review-alert", "Debes iniciar sesión", "error");
    return;
  }

  const reviewData = {
    product,
    texto_reseña: text
  };

  try {
    const res = await fetch(`${API_URL}/reviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(reviewData)
    });

    const data = await res.json();

    if (res.ok) {
      showAlert("review-alert", "Reseña enviada ✔", "success");
    } else {
      showAlert("review-alert", data.detail || "Error al enviar reseña", "error");
    }

  } catch (err) {
    showAlert("review-alert", "Error de conexión", "error");
  }
}



async function loadReviewsByProduct(product) {
  const container = document.getElementById("reviews-list");
  if (!container) return;

  container.innerHTML = `<div class="loading">Cargando...</div>`;

  try {
    const res = await fetch(`${API_URL}/reviews/${product}`);
    const data = await res.json();

    container.innerHTML = data.length
      ? data.map(r => `
        <div class="review-card">
          <h3>${r.product}</h3>
          <p>${r.text}</p>
          <span class="sentiment ${r.sentiment}">
            ${r.sentiment.toUpperCase()}
          </span>
        </div>
      `).join("")
      : `<p>No hay reseñas aún.</p>`;

  } catch (err) {
    container.innerHTML = `<p>Error al cargar reseñas.</p>`;
  }
}


document.addEventListener("DOMContentLoaded", () => {
  const reg = document.getElementById("register-form");
  if (reg) reg.addEventListener("submit", handleRegister);

  const log = document.getElementById("login-form");
  if (log) log.addEventListener("submit", handleLogin);

  const rev = document.getElementById("review-form");
  if (rev) rev.addEventListener("submit", handleReviewSubmit);
});


document.querySelectorAll(".toggle-pass").forEach(btn => {
  btn.addEventListener("click", () => {
    
    const input = btn.parentElement.querySelector("input");
    const eyeOpen = btn.querySelector(".eye-open");
    const eyeClosed = btn.querySelector(".eye-closed");

    if (input.type === "password") {
      input.type = "text";         
      eyeClosed.classList.add("hidden");
      eyeOpen.classList.remove("hidden");
    } else {
      input.type = "password";    
      eyeOpen.classList.add("hidden");
      eyeClosed.classList.remove("hidden");
    }
  });
});
