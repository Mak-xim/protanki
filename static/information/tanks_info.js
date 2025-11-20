document.addEventListener("DOMContentLoaded", () => {
document.querySelectorAll(".favorite-toggle").forEach(button => {
  updateFavoriteButton(button);

  button.addEventListener("click", (e) => {
    e.preventDefault();

    if (button.classList.contains("not-authenticated")) {
      showAlert("Сначала войдите в аккаунт, чтобы добавить в избранное.");
      return;
    }

    const type = button.dataset.type;
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
        // Меняем действие на противоположное
        button.dataset.action = (action === "add") ? "remove" : "add";

        // Обновляем кнопку и title
        updateFavoriteButton(button);
      }
    })
    .catch(error => console.error("Ошибка:", error));
  });
});

function updateFavoriteButton(button) {
  if (button.classList.contains("not-authenticated")) {
    // Для неавторизованных - всегда пустая звезда и title "Войдите в аккаунт"
    button.title = "Добавить в избранное";
    button.innerHTML = '<i class="bi bi-star" style="font-size: 50px"></i>';
  } else {
    if (button.dataset.action === "add") {
      button.title = "Добавить в избранное";
      button.innerHTML = '<i class="bi bi-star" style="font-size: 50px"></i>';
    } else {
      button.title = "Удалить из избранного";
      button.innerHTML = '<i class="bi bi-star-fill text-warning" style="font-size: 50px"></i>';
    }
  }
}
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