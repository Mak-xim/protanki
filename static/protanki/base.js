// Автоматически скрыть уведомления через 5 секунд
  setTimeout(function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      alert.classList.add('hide');  // если используете .hide с CSS
      setTimeout(() => alert.remove(), 500);  // удалить после анимации
    });
  }, 5000);