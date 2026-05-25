self.addEventListener('push', function(event) {
  const data = event.data.text();
  event.waitUntil(
    self.registration.showNotification('GURU Alert', {
      body: data,
      icon: '/static/icon.png'
    })
  );
});