document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".favorite-toggle").forEach(button => {
    button.addEventListener("click", (e) => {
      e.preventDefault();

      // Если пользователь не авторизован
      if (button.classList.contains("not-authenticated")) {
        showAlert("Сначала войдите в аккаунт, чтобы добавить в избранное.");
        return;
      }

      const type = button.dataset.type; // 'gun' или 'body'
      const id = button.dataset.id;
      const action = button.dataset.action;
      const url = `/favorite/${type}/${action}/${id}/`;

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "ok") {
          if (action === "add") {
            button.textContent = "Удалить из избранного";
            button.dataset.action = "remove";
          } else {
            button.textContent = "В избранное";
            button.dataset.action = "add";
          }
        }
      })
      .catch(error => console.error("Ошибка:", error));
    });
  });
});

function showAlert(message) {
  const container = document.getElementById('alert-container');

  if (!container) {
    console.error("Alert container not found!");
    return;
  }

  const alert = document.createElement('div');
  alert.className = 'alert';
  alert.textContent = message;

  container.appendChild(alert);

  setTimeout(() => {
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 500);
  }, 5000);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}